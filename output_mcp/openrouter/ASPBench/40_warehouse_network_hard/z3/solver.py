from z3 import *

# Data
hub_names = ['H1', 'H2']
regional_names = ['R1', 'R2', 'R3', 'R4']
customer_names = ['C1', 'C2', 'C3', 'C4', 'C5', 'C6']
time_slots = [1,2,3,4]

# Opening costs
hub_open_cost = [1000, 1200]
reg_open_cost = [200, 250, 220, 180]

# Capacities
hub_capacity = [400, 350]
reg_capacity = [70, 80, 60, 90]

# Trucks per hub per time slot (same each slot)
hub_trucks = [2, 1]

# Demands and time windows (inclusive)
customer_demand = [20, 30, 15, 25, 35, 10]
customer_window = [(2,3), (1,2), (3,4), (1,4), (2,4), (1,1)]

# Hub to regional unit costs (None if not allowed)
# rows: hubs, cols: regionals
hub_reg_cost = [
    [5, 6, None, None],  # H1 can supply R1,R2
    [None, None, 5, 6]   # H2 can supply R3,R4
]

# Regional to customer unit costs (None if not allowed)
# rows: regionals, cols: customers
reg_cust_cost = [
    [10, 12, None, None, None, None],   # R1 -> C1,C2
    [None, 13, 15, None, None, None],   # R2 -> C2,C3
    [None, None, None, 9, 11, None],    # R3 -> C4,C5
    [None, None, None, None, 14, 7]     # R4 -> C5,C6
]

# Connectivity constraints (already encoded via cost matrices)
# Maintenance schedules
# R2 unavailable at time slot 2, H1 unavailable at time slot 4

# Solver
opt = Optimize()

# Decision variables
open_hub = [Bool(f'open_hub_{h}') for h in range(2)]
open_reg = [Bool(f'open_reg_{r}') for r in range(4)]
# supply hub for each regional (0 for H1, 1 for H2)
supply = [Int(f'supply_{r}') for r in range(4)]
# assign each customer to a regional and a time slot
assign_reg = [Int(f'assign_reg_{c}') for c in range(6)]
assign_time = [Int(f'assign_time_{c}') for c in range(6)]

# Domain constraints
for r in range(4):
    opt.add(Or(supply[r] == 0, supply[r] == 1))
for c in range(6):
    opt.add(And(assign_reg[c] >= 0, assign_reg[c] <= 3))
    opt.add(And(assign_time[c] >= 1, assign_time[c] <= 4))

# Opening prerequisite: if regional open then its supplying hub must be open
for r in range(4):
    for h in range(2):
        opt.add(Implies(And(open_reg[r], supply[r] == h), open_hub[h]))
    # also enforce connectivity: only allowed hub-reg pairs
    allowed = []
    for h in range(2):
        if hub_reg_cost[h][r] is not None:
            allowed.append(supply[r] == h)
    opt.add(Or(*allowed))  # supply must be one of allowed hubs

# Customer assignment constraints
# Connectivity: allowed regionals per customer
allowed_reg_per_cust = [
    [0,1],   # C1: R1,R2? actually only R1 per data, but cost matrix shows R1 only. We'll enforce via cost matrix later.
    [0,1],   # C2: R1,R2
    [1],     # C3: R2
    [2],     # C4: R3
    [2,3],   # C5: R3,R4
    [3]      # C6: R4
]
# Adjust according to given connectivity: matches above.
for c in range(6):
    # enforce allowed regionals
    opt.add(Or([assign_reg[c] == r for r in allowed_reg_per_cust[c]]))
    # enforce that assigned regional is open
    for r in range(4):
        opt.add(Implies(assign_reg[c] == r, open_reg[r]))
    # time window
    lo, hi = customer_window[c]
    opt.add(assign_time[c] >= lo, assign_time[c] <= hi)
    # maintenance constraints
    # R2 (index1) unavailable at slot 2
    opt.add(Implies(assign_reg[c] == 1, assign_time[c] != 2))
    # H1 unavailable at slot 4: if regional supplied by H1 then no delivery at 4
    opt.add(Implies(And(assign_reg[c] == r, supply[r] == 0), assign_time[c] != 4) for r in range(4))

# Regional capacity constraints
for r in range(4):
    total_demand_r = Sum([If(assign_reg[c] == r, customer_demand[c], 0) for c in range(6)])
    opt.add(total_demand_r <= reg_capacity[r] * If(open_reg[r], 1, 0))

# Hub capacity constraints
for h in range(2):
    total_demand_h = Sum([If(And(assign_reg[c] == r, supply[r] == h), customer_demand[c], 0) for c in range(6) for r in range(4)])
    opt.add(total_demand_h <= hub_capacity[h] * If(open_hub[h], 1, 0))

# Truck limits per hub per time slot
for h in range(2):
    for ts in time_slots:
        deliveries = Sum([If(And(assign_reg[c] == r, supply[r] == h, assign_time[c] == ts), 1, 0) for c in range(6) for r in range(4)])
        opt.add(deliveries <= hub_trucks[h])

# Cost calculation
# Opening costs
opening_cost = Sum([If(open_hub[h], hub_open_cost[h], 0) for h in range(2)]) + Sum([If(open_reg[r], reg_open_cost[r], 0) for r in range(4)])
# Hub to regional transport cost
hub_reg_transport = 0
for r in range(4):
    demand_r = Sum([If(assign_reg[c] == r, customer_demand[c], 0) for c in range(6)])
    # cost depends on supplying hub
    cost_expr = If(supply[r] == 0, hub_reg_cost[0][r] if hub_reg_cost[0][r] is not None else 0,
                   hub_reg_cost[1][r] if hub_reg_cost[1][r] is not None else 0)
    hub_reg_transport += demand_r * cost_expr
# Regional to customer transport cost
reg_cust_transport = Sum([If(assign_reg[c] == r, customer_demand[c] * (reg_cust_cost[r][c] if reg_cust_cost[r][c] is not None else 0), 0) for c in range(6) for r in range(4)])

total_cost = opening_cost + hub_reg_transport + reg_cust_transport
opt.minimize(total_cost)

# Solve
if opt.check() == sat:
    m = opt.model()
    # Extract results
    open_hubs_res = [hub_names[i] for i in range(2) if m.eval(open_hub[i])]
    open_regs_res = [regional_names[i] for i in range(4) if m.eval(open_reg[i])]
    hub_assignments_res = {}
    for r in range(4):
        if m.eval(open_reg[r]):
            hub_idx = m.eval(supply[r]).as_long()
            hub_assignments_res[regional_names[r]] = hub_names[hub_idx]
    customer_deliveries_res = []
    for c in range(6):
        reg_idx = m.eval(assign_reg[c]).as_long()
        ts = m.eval(assign_time[c]).as_long()
        customer_deliveries_res.append((customer_names[c], regional_names[reg_idx], ts))
    total_cost_val = m.eval(total_cost).as_long()
    print("STATUS: sat")
    print("total_cost =", total_cost_val)
    print("open_hubs =", open_hubs_res)
    print("open_regionals =", open_regs_res)
    print("hub_assignments =", hub_assignments_res)
    print("customer_deliveries =", customer_deliveries_res)
else:
    print("STATUS: unsat")