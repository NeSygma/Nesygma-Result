from z3 import *

# ========== SETS ==========
hubs = ["H1", "H2"]
regionals = ["R1", "R2", "R3", "R4"]
customers = ["C1", "C2", "C3", "C4", "C5", "C6"]
time_slots = [1, 2, 3, 4]

# ========== DATA ==========
open_cost_hub = {"H1": 1000, "H2": 1200}
open_cost_reg = {"R1": 200, "R2": 250, "R3": 220, "R4": 180}

capacity_hub = {"H1": 400, "H2": 350}
capacity_reg = {"R1": 70, "R2": 80, "R3": 60, "R4": 90}

trucks_hub = {"H1": 2, "H2": 1}

demand = {"C1": 20, "C2": 30, "C3": 15, "C4": 25, "C5": 35, "C6": 10}

time_window = {"C1": (2, 3), "C2": (1, 2), "C3": (3, 4), "C4": (1, 4), "C5": (2, 4), "C6": (1, 1)}

hub_reg_cost = {("H1", "R1"): 5, ("H1", "R2"): 6, ("H2", "R3"): 5, ("H2", "R4"): 6}

reg_cust_cost = {("R1", "C1"): 10, ("R1", "C2"): 12,
                 ("R2", "C2"): 13, ("R2", "C3"): 15,
                 ("R3", "C4"): 9,  ("R3", "C5"): 11,
                 ("R4", "C5"): 14, ("R4", "C6"): 7}

hub_can_supply = {"H1": ["R1", "R2"], "H2": ["R3", "R4"]}
reg_can_serve = {"R1": ["C1", "C2"], "R2": ["C2", "C3"], "R3": ["C4", "C5"], "R4": ["C5", "C6"]}

# Maintenance: facilities unavailable during specific time slots
maintenance_reg = {"R2": [2]}
maintenance_hub = {"H1": [4]}

# ========== DECISION VARIABLES ==========
open_hub = {h: Bool(f"open_hub_{h}") for h in hubs}
open_reg = {r: Bool(f"open_reg_{r}") for r in regionals}

# hub_supplies[h][r]: hub h supplies regional r
hub_supplies = {}
for h in hubs:
    for r in regionals:
        hub_supplies[(h, r)] = Bool(f"hub_supplies_{h}_{r}")

# assign[c][r][t]: customer c assigned to regional r at time t
assign = {}
for c in customers:
    for r in regionals:
        for t in time_slots:
            assign[(c, r, t)] = Bool(f"assign_{c}_{r}_{t}")

# ========== OPTIMIZER ==========
opt = Optimize()

# ========== CONSTRAINT 1: Opening prerequisite ==========
# If a customer is assigned to a regional, that regional must be open
for c in customers:
    for r in regionals:
        for t in time_slots:
            opt.add(Implies(assign[(c, r, t)], open_reg[r]))

# If hub supplies regional, both must be open
for h in hubs:
    for r in regionals:
        opt.add(Implies(hub_supplies[(h, r)], open_hub[h]))
        opt.add(Implies(hub_supplies[(h, r)], open_reg[r]))

# ========== CONSTRAINT 2: Assignment uniqueness ==========
# Each customer must be assigned to exactly one regional at exactly one time slot
for c in customers:
    opt.add(Sum([If(assign[(c, r, t)], 1, 0) for r in regionals for t in time_slots]) == 1)

# ========== CONSTRAINT 3: Supply uniqueness ==========
# Each open regional must be supplied by exactly one hub
for r in regionals:
    opt.add(Implies(open_reg[r], Sum([If(hub_supplies[(h, r)], 1, 0) for h in hubs]) == 1))
    # If regional is not open, no hub supplies it
    opt.add(Implies(Not(open_reg[r]), Sum([If(hub_supplies[(h, r)], 1, 0) for h in hubs]) == 0))

# ========== CONSTRAINT 4: Connectivity ==========
# Hub-to-Regional connectivity
for h in hubs:
    for r in regionals:
        if r not in hub_can_supply[h]:
            opt.add(Not(hub_supplies[(h, r)]))

# Regional-to-Customer connectivity
for c in customers:
    for r in regionals:
        for t in time_slots:
            if c not in reg_can_serve[r]:
                opt.add(Not(assign[(c, r, t)]))

# ========== CONSTRAINT 5: Time windows ==========
for c in customers:
    tw_min, tw_max = time_window[c]
    for r in regionals:
        for t in time_slots:
            if t < tw_min or t > tw_max:
                opt.add(Not(assign[(c, r, t)]))

# ========== CONSTRAINT 6: Maintenance ==========
# R2 unavailable at time slot 2
for c in customers:
    opt.add(Not(assign[(c, "R2", 2)]))

# H1 unavailable at time slot 4
# No deliveries can pass through H1 at time slot 4
# This means: if hub H1 supplies regional r, then no customer can be assigned to r at time 4
for r in regionals:
    for c in customers:
        opt.add(Not(And(hub_supplies[("H1", r)], assign[(c, r, 4)])))

# ========== CONSTRAINT 7: Regional capacity ==========
for r in regionals:
    total_demand_r = Sum([If(assign[(c, r, t)], demand[c], 0) for c in customers for t in time_slots])
    opt.add(total_demand_r <= If(open_reg[r], capacity_reg[r], 0))

# ========== CONSTRAINT 8: Hub capacity ==========
for h in hubs:
    total_demand_h = Sum([If(And(hub_supplies[(h, r)], assign[(c, r, t)]), demand[c], 0)
                          for r in regionals for c in customers for t in time_slots])
    opt.add(total_demand_h <= If(open_hub[h], capacity_hub[h], 0))

# ========== CONSTRAINT 9: Truck limits ==========
# For each hub h and time slot t:
# number of customer deliveries in time slot t from regionals supplied by h ≤ trucks available at h
for h in hubs:
    for t in time_slots:
        deliveries_h_t = Sum([If(And(hub_supplies[(h, r)], assign[(c, r, t)]), 1, 0)
                              for r in regionals for c in customers])
        opt.add(deliveries_h_t <= trucks_hub[h])

# ========== OBJECTIVE: Minimize total cost ==========
# Fixed opening costs
fixed_cost = Sum([If(open_hub[h], open_cost_hub[h], 0) for h in hubs]) + \
             Sum([If(open_reg[r], open_cost_reg[r], 0) for r in regionals])

# Hub-to-Regional transport costs
# For each supply link (h, r), cost = (total demand at regional r) * unit cost
hub_reg_transport_list = []
for h in hubs:
    for r in regionals:
        if (h, r) in hub_reg_cost:
            total_demand_r = Sum([If(assign[(c, r, t)], demand[c], 0) for c in customers for t in time_slots])
            link_cost = If(hub_supplies[(h, r)], total_demand_r * hub_reg_cost[(h, r)], 0)
            hub_reg_transport_list.append(link_cost)
hub_reg_transport = Sum(hub_reg_transport_list)

# Regional-to-Customer transport costs
reg_cust_transport_list = []
for r in regionals:
    for c in customers:
        if (r, c) in reg_cust_cost:
            for t in time_slots:
                reg_cust_transport_list.append(
                    If(assign[(c, r, t)], demand[c] * reg_cust_cost[(r, c)], 0)
                )
reg_cust_transport = Sum(reg_cust_transport_list)

total_cost = fixed_cost + hub_reg_transport + reg_cust_transport

opt.minimize(total_cost)

# ========== SOLVE ==========
result = opt.check()

if result == sat:
    m = opt.model()

    # Extract open hubs
    open_hubs_sol = sorted([h for h in hubs if is_true(m[open_hub[h]])])
    # Extract open regionals
    open_regs_sol = sorted([r for r in regionals if is_true(m[open_reg[r]])])

    # Extract hub assignments
    hub_assign_sol = {}
    for r in regionals:
        for h in hubs:
            if is_true(m[hub_supplies[(h, r)]]):
                hub_assign_sol[r] = h

    # Extract customer deliveries
    deliveries_sol = []
    for c in customers:
        for r in regionals:
            for t in time_slots:
                if is_true(m[assign[(c, r, t)]]):
                    deliveries_sol.append({"customer": c, "regional": r, "time": t})

    total_cost_val = m.eval(total_cost)

    print("STATUS: sat")
    print(f"open_hubs: {open_hubs_sol}")
    print(f"open_regionals: {open_regs_sol}")
    print(f"hub_assignments: {hub_assign_sol}")
    print(f"customer_deliveries: {deliveries_sol}")
    print(f"total_cost: {total_cost_val}")

    # Verify expected optimal cost
    print(f"\nExpected minimum total cost: 5215")
    print(f"Found total cost: {total_cost_val}")

elif result == unsat:
    print("STATUS: unsat")
    print("No feasible solution found.")
else:
    print("STATUS: unknown")