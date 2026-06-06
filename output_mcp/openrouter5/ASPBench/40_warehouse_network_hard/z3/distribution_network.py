from z3 import *

# ============================================================
# DATA
# ============================================================
hubs = ["H1", "H2"]
regionals = ["R1", "R2", "R3", "R4"]
customers = ["C1", "C2", "C3", "C4", "C5", "C6"]
time_slots = [1, 2, 3, 4]

# Opening costs
hub_open_cost = {"H1": 1000, "H2": 1200}
reg_open_cost = {"R1": 200, "R2": 250, "R3": 220, "R4": 180}

# Capacities
hub_capacity = {"H1": 400, "H2": 350}
reg_capacity = {"R1": 70, "R2": 80, "R3": 60, "R4": 90}

# Trucks per hub per time slot
hub_trucks = {"H1": 2, "H2": 1}

# Customer demands and time windows
demand = {"C1": 20, "C2": 30, "C3": 15, "C4": 25, "C5": 35, "C6": 10}
tw_low = {"C1": 2, "C2": 1, "C3": 3, "C4": 1, "C5": 2, "C6": 1}
tw_high = {"C1": 3, "C2": 2, "C3": 4, "C4": 4, "C5": 4, "C6": 1}

# Transportation costs (hub->regional)
hub_reg_cost = {
    ("H1", "R1"): 5, ("H1", "R2"): 6,
    ("H2", "R3"): 5, ("H2", "R4"): 6
}

# Transportation costs (regional->customer)
reg_cust_cost = {
    ("R1", "C1"): 10, ("R1", "C2"): 12,
    ("R2", "C2"): 13, ("R2", "C3"): 15,
    ("R3", "C4"): 9,  ("R3", "C5"): 11,
    ("R4", "C5"): 14, ("R4", "C6"): 7
}

# Connectivity: hub can supply regional
hub_supplies_reg = {
    "H1": ["R1", "R2"],
    "H2": ["R3", "R4"]
}

# Connectivity: regional can serve customer
reg_serves_cust = {
    "R1": ["C1", "C2"],
    "R2": ["C2", "C3"],
    "R3": ["C4", "C5"],
    "R4": ["C5", "C6"]
}

# Maintenance: facilities unavailable at specific time slots
maintenance = {
    "R2": [2],
    "H1": [4]
}

# ============================================================
# DECISION VARIABLES
# ============================================================
opt = Optimize()

# open_hub[h] = 1 if hub h is opened
open_hub = {h: Int(f"open_hub_{h}") for h in hubs}
for h in hubs:
    opt.add(Or(open_hub[h] == 0, open_hub[h] == 1))

# open_reg[r] = 1 if regional warehouse r is opened
open_reg = {r: Int(f"open_reg_{r}") for r in regionals}
for r in regionals:
    opt.add(Or(open_reg[r] == 0, open_reg[r] == 1))

# hub_assign[r] = hub that supplies regional r (0 if r not opened, else hub index 0 or 1)
# We'll use integer: 0=H1, 1=H2, -1=not assigned
hub_assign = {r: Int(f"hub_assign_{r}") for r in regionals}
for r in regionals:
    opt.add(Or(hub_assign[r] == -1, hub_assign[r] == 0, hub_assign[r] == 1))

# For each customer c, assign to regional r at time t
# assign[c] = (r_index, t) where r_index in 0..3, t in 1..4
# We'll use two variables per customer
cust_reg = {c: Int(f"cust_reg_{c}") for c in customers}  # 0=R1,1=R2,2=R3,3=R4, -1=unassigned
cust_time = {c: Int(f"cust_time_{c}") for c in customers}  # 1..4

for c in customers:
    opt.add(Or(cust_reg[c] == -1, cust_reg[c] == 0, cust_reg[c] == 1, cust_reg[c] == 2, cust_reg[c] == 3))
    opt.add(Or(cust_time[c] == 1, cust_time[c] == 2, cust_time[c] == 3, cust_time[c] == 4))

# ============================================================
# CONSTRAINTS
# ============================================================

# 1. Opening prerequisite: customer served by open regional, regional supplied by open hub
# If cust_reg[c] == r_idx (0..3), then open_reg[r] == 1
for c in customers:
    for ri, r in enumerate(regionals):
        opt.add(Implies(cust_reg[c] == ri, open_reg[r] == 1))

# If hub_assign[r] == h_idx (0 or 1), then open_hub[h] == 1 and open_reg[r] == 1
for ri, r in enumerate(regionals):
    for hi, h in enumerate(hubs):
        opt.add(Implies(hub_assign[r] == hi, And(open_hub[h] == 1, open_reg[r] == 1)))

# 2. Assignment uniqueness: each customer assigned to exactly one regional at exactly one time slot
for c in customers:
    opt.add(cust_reg[c] >= 0)  # must be assigned (not -1)
    opt.add(cust_time[c] >= 1)

# 3. Supply uniqueness: each open regional supplied by exactly one hub
# If open_reg[r] == 1, then hub_assign[r] must be 0 or 1 (not -1)
for r in regionals:
    opt.add(Implies(open_reg[r] == 1, Or(hub_assign[r] == 0, hub_assign[r] == 1)))
    # If not open, hub_assign must be -1
    opt.add(Implies(open_reg[r] == 0, hub_assign[r] == -1))

# 4. Connectivity constraints
# Hub can only supply regionals it's connected to
for ri, r in enumerate(regionals):
    for hi, h in enumerate(hubs):
        if r not in hub_supplies_reg[h]:
            opt.add(Implies(hub_assign[r] == hi, False))  # i.e., hub_assign[r] != hi
            # Actually simpler: just forbid it
            opt.add(hub_assign[r] != hi)

# Regional can only serve customers it's connected to
for c in customers:
    for ri, r in enumerate(regionals):
        if c not in reg_serves_cust[r]:
            opt.add(cust_reg[c] != ri)

# 5. Time windows
for c in customers:
    opt.add(cust_time[c] >= tw_low[c])
    opt.add(cust_time[c] <= tw_high[c])

# 6. Maintenance: no deliveries through facilities during maintenance
# If a regional is under maintenance at time t, no customer can be assigned to it at that time
for r in regionals:
    if r in maintenance:
        for mt in maintenance[r]:
            for c in customers:
                ri = regionals.index(r)
                opt.add(Not(And(cust_reg[c] == ri, cust_time[c] == mt)))

# If a hub is under maintenance at time t, no regional supplied by it can have deliveries at that time
for h in hubs:
    if h in maintenance:
        for mt in maintenance[h]:
            hi = hubs.index(h)
            for r in regionals:
                ri = regionals.index(r)
                for c in customers:
                    opt.add(Not(And(hub_assign[r] == hi, cust_reg[c] == ri, cust_time[c] == mt)))

# 7. Regional capacity
for ri, r in enumerate(regionals):
    total_demand_reg = Sum([If(cust_reg[c] == ri, demand[c], 0) for c in customers])
    opt.add(total_demand_reg <= reg_capacity[r] * open_reg[r])  # if not open, capacity is 0

# 8. Hub capacity
for hi, h in enumerate(hubs):
    # Total demand through hub = sum of demands of all customers served by regionals supplied by this hub
    total_demand_hub = Sum([If(And(hub_assign[r] == hi, cust_reg[c] == ri), demand[c], 0)
                           for ri, r in enumerate(regionals) for c in customers])
    opt.add(total_demand_hub <= hub_capacity[h])

# 9. Truck limits: For each hub h and each time slot t,
# number of customer deliveries in that time slot from regionals supplied by h <= hub_trucks[h]
for hi, h in enumerate(hubs):
    for t in time_slots:
        deliveries_at_t = Sum([If(And(hub_assign[r] == hi, cust_reg[c] == ri, cust_time[c] == t), 1, 0)
                              for ri, r in enumerate(regionals) for c in customers])
        opt.add(deliveries_at_t <= hub_trucks[h])

# ============================================================
# OBJECTIVE: Minimize total cost
# ============================================================

# Fixed opening costs
fixed_cost = Sum([If(open_hub[h] == 1, hub_open_cost[h], 0) for h in hubs]) + \
             Sum([If(open_reg[r] == 1, reg_open_cost[r], 0) for r in regionals])

# Hub-to-Regional transport costs
hub_reg_transport = Sum([If(And(hub_assign[r] == hi, cust_reg[c] == ri), demand[c] * hub_reg_cost[(h, r)], 0)
                         for hi, h in enumerate(hubs) for ri, r in enumerate(regionals) for c in customers
                         if (h, r) in hub_reg_cost])

# Regional-to-Customer transport costs
reg_cust_transport = Sum([If(cust_reg[c] == ri, demand[c] * reg_cust_cost[(r, c)], 0)
                          for ri, r in enumerate(regionals) for c in customers
                          if (r, c) in reg_cust_cost])

total_cost = fixed_cost + hub_reg_transport + reg_cust_transport

opt.minimize(total_cost)

# ============================================================
# SOLVE
# ============================================================
BENCHMARK_MODE = True
result = opt.check()

if result == sat:
    m = opt.model()
    print("STATUS: sat")
    print(f"Total cost = {m.eval(total_cost)}")
    
    # Print solution details
    open_hubs_list = [h for h in hubs if m.eval(open_hub[h]).as_long() == 1]
    open_regs_list = [r for r in regionals if m.eval(open_reg[r]).as_long() == 1]
    
    print(f"open_hubs: {open_hubs_list}")
    print(f"open_regionals: {open_regs_list}")
    
    hub_assignments = {}
    for r in regionals:
        ha = m.eval(hub_assign[r]).as_long()
        if ha >= 0:
            hub_assignments[r] = hubs[ha]
    print(f"hub_assignments: {hub_assignments}")
    
    deliveries = []
    for c in customers:
        ri = m.eval(cust_reg[c]).as_long()
        t = m.eval(cust_time[c]).as_long()
        if ri >= 0:
            deliveries.append((c, regionals[ri], t))
    print(f"customer_deliveries: {deliveries}")
    
    # Verify expected cost
    expected = 5215
    actual = m.eval(total_cost).as_long()
    print(f"Expected minimum total cost: {expected}")
    print(f"Actual total cost: {actual}")
    if actual == expected:
        print("MATCH: Solution achieves expected optimal cost!")
    else:
        print(f"MISMATCH: Expected {expected}, got {actual}")
    
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")