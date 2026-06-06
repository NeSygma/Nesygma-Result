from z3 import *

# Create optimizer
opt = Optimize()

# ============================================================
# DATA
# ============================================================

# Facilities
hubs = ['H1', 'H2']
regionals = ['R1', 'R2', 'R3', 'R4']
customers = ['C1', 'C2', 'C3', 'C4', 'C5', 'C6']
time_slots = [1, 2, 3, 4]

# Opening costs
hub_open_cost = {'H1': 1000, 'H2': 1200}
regional_open_cost = {'R1': 200, 'R2': 250, 'R3': 220, 'R4': 180}

# Capacities
hub_capacity = {'H1': 400, 'H2': 350}
regional_capacity = {'R1': 70, 'R2': 80, 'R3': 60, 'R4': 90}

# Trucks per hub per time slot
hub_trucks = {'H1': 2, 'H2': 1}

# Customer demands and time windows
customer_demand = {'C1': 20, 'C2': 30, 'C3': 15, 'C4': 25, 'C5': 35, 'C6': 10}
customer_tw_start = {'C1': 2, 'C2': 1, 'C3': 3, 'C4': 1, 'C5': 2, 'C6': 1}
customer_tw_end = {'C1': 3, 'C2': 2, 'C3': 4, 'C4': 4, 'C5': 4, 'C6': 1}

# Transportation costs: Hub to Regional
hub_regional_cost = {
    ('H1', 'R1'): 5, ('H1', 'R2'): 6,
    ('H2', 'R3'): 5, ('H2', 'R4'): 6
}

# Transportation costs: Regional to Customer
regional_customer_cost = {
    ('R1', 'C1'): 10, ('R1', 'C2'): 12,
    ('R2', 'C2'): 13, ('R2', 'C3'): 15,
    ('R3', 'C4'): 9, ('R3', 'C5'): 11,
    ('R4', 'C5'): 14, ('R4', 'C6'): 7
}

# Connectivity: Hub can supply Regional
hub_regional_connect = {
    'H1': ['R1', 'R2'],
    'H2': ['R3', 'R4']
}

# Connectivity: Regional can serve Customer
regional_customer_connect = {
    'R1': ['C1', 'C2'],
    'R2': ['C2', 'C3'],
    'R3': ['C4', 'C5'],
    'R4': ['C5', 'C6']
}

# Maintenance schedules (unavailable time slots)
# R2 unavailable at time slot 2, H1 unavailable at time slot 4
maintenance = {
    'R2': [2],
    'H1': [4]
}

# ============================================================
# DECISION VARIABLES
# ============================================================

# Binary: is hub/regional open?
open_hub = {h: Bool(f'open_{h}') for h in hubs}
open_regional = {r: Bool(f'open_{r}') for r in regionals}

# Binary: is regional r supplied by hub h?
supply = {(h, r): Bool(f'supply_{h}_{r}') for h in hubs for r in regionals}

# Binary: is customer c assigned to regional r at time t?
assign = {(c, r, t): Bool(f'assign_{c}_{r}_{t}') for c in customers for r in regionals for t in time_slots}

# ============================================================
# CONSTRAINTS
# ============================================================

# 1. Assignment uniqueness: Each customer assigned to exactly one regional at exactly one time slot
for c in customers:
    # At least one assignment
    opt.add(Or([assign[c, r, t] for r in regionals for t in time_slots]))
    # At most one assignment (pairwise exclusion)
    for r1 in regionals:
        for t1 in time_slots:
            for r2 in regionals:
                for t2 in time_slots:
                    if (r1, t1) != (r2, t2):
                        opt.add(Implies(assign[c, r1, t1], Not(assign[c, r2, t2])))

# 2. Connectivity: Customer can only be assigned to connected regional
for c in customers:
    for r in regionals:
        if r not in regional_customer_connect or c not in regional_customer_connect[r]:
            for t in time_slots:
                opt.add(Not(assign[c, r, t]))

# 3. Time windows: Customer delivery must be within time window
for c in customers:
    for r in regionals:
        for t in time_slots:
            if t < customer_tw_start[c] or t > customer_tw_end[c]:
                opt.add(Not(assign[c, r, t]))

# 4. Opening prerequisite: If customer assigned to regional, regional must be open
for c in customers:
    for r in regionals:
        for t in time_slots:
            opt.add(Implies(assign[c, r, t], open_regional[r]))

# 5. Supply uniqueness: Each open regional supplied by exactly one hub
for r in regionals:
    # If regional is open, exactly one hub supplies it
    possible_hubs = [h for h in hubs if r in hub_regional_connect.get(h, [])]
    if possible_hubs:
        opt.add(Implies(open_regional[r], Or([supply[h, r] for h in possible_hubs])))
        # At most one hub
        for i in range(len(possible_hubs)):
            for j in range(i+1, len(possible_hubs)):
                opt.add(Not(And(supply[possible_hubs[i], r], supply[possible_hubs[j], r])))
    # If regional not open, no supply
    for h in hubs:
        opt.add(Implies(Not(open_regional[r]), Not(supply[h, r])))

# 6. Connectivity: Hub can only supply connected regional
for h in hubs:
    for r in regionals:
        if r not in hub_regional_connect.get(h, []):
            opt.add(Not(supply[h, r]))

# 7. Opening prerequisite: If hub supplies a regional, hub must be open
for h in hubs:
    for r in regionals:
        opt.add(Implies(supply[h, r], open_hub[h]))

# 8. Regional capacity: Total demand served by each regional <= capacity
for r in regionals:
    total_demand_r = Sum([If(assign[c, r, t], customer_demand[c], 0) for c in customers for t in time_slots])
    opt.add(total_demand_r <= regional_capacity[r])

# 9. Hub capacity: Total demand passing through each hub <= hub capacity
for h in hubs:
    # Demand at regional r = sum of customer demands assigned to r
    demand_at_r = {r: Sum([If(assign[c, r, t], customer_demand[c], 0) for c in customers for t in time_slots]) for r in regionals}
    total_demand_h = Sum([If(supply[h, r], demand_at_r[r], 0) for r in regionals])
    opt.add(total_demand_h <= hub_capacity[h])

# 10. Truck limits: Number of deliveries in each time slot from regionals supplied by hub <= trucks
for h in hubs:
    for t in time_slots:
        # Count deliveries at time t through regionals supplied by h
        delivery_count = Sum([If(And(supply[h, r], assign[c, r, t]), 1, 0) for r in regionals for c in customers])
        opt.add(delivery_count <= hub_trucks[h])

# 11. Maintenance: No deliveries through facilities during maintenance
# R2 unavailable at time slot 2
for c in customers:
    opt.add(Not(assign[c, 'R2', 2]))

# H1 unavailable at time slot 4: no supply from H1 at time 4
# This means no customer can be served through a regional supplied by H1 at time 4
for c in customers:
    for r in regionals:
        if r in hub_regional_connect.get('H1', []):
            opt.add(Implies(And(supply['H1', r], assign[c, r, 4]), False))

# ============================================================
# OBJECTIVE: Minimize total cost
# ============================================================

# Fixed opening costs
fixed_cost = Sum([If(open_hub[h], hub_open_cost[h], 0) for h in hubs] +
                 [If(open_regional[r], regional_open_cost[r], 0) for r in regionals])

# Hub-to-Regional transport costs
# Cost = total demand at regional r * unit cost from supplying hub h to r
hub_reg_transport = Sum([If(supply[h, r],
                           Sum([If(assign[c, r, t], customer_demand[c], 0) for c in customers for t in time_slots]) * hub_regional_cost.get((h, r), 0),
                           0) for h in hubs for r in regionals])

# Regional-to-Customer transport costs
reg_cust_transport = Sum([If(assign[c, r, t], customer_demand[c] * regional_customer_cost.get((r, c), 0), 0)
                         for c in customers for r in regionals for t in time_slots])

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
    
    # Extract open hubs
    open_hubs_list = [h for h in hubs if is_true(m.evaluate(open_hub[h]))]
    print(f"open_hubs: {open_hubs_list}")
    
    # Extract open regionals
    open_regionals_list = [r for r in regionals if is_true(m.evaluate(open_regional[r]))]
    print(f"open_regionals: {open_regionals_list}")
    
    # Extract hub assignments
    hub_assignments = {}
    for r in regionals:
        for h in hubs:
            if is_true(m.evaluate(supply[h, r])):
                hub_assignments[r] = h
    print(f"hub_assignments: {hub_assignments}")
    
    # Extract customer deliveries
    customer_deliveries = []
    for c in customers:
        for r in regionals:
            for t in time_slots:
                if is_true(m.evaluate(assign[c, r, t])):
                    customer_deliveries.append({'customer': c, 'regional': r, 'time_slot': t})
    print(f"customer_deliveries: {customer_deliveries}")
    
    # Compute and print total cost
    computed_cost = m.evaluate(total_cost)
    print(f"total_cost: {computed_cost}")
    
    # Print detailed cost breakdown
    fc = m.evaluate(fixed_cost)
    hrt = m.evaluate(hub_reg_transport)
    rct = m.evaluate(reg_cust_transport)
    print(f"fixed_cost: {fc}")
    print(f"hub_regional_transport: {hrt}")
    print(f"regional_customer_transport: {rct}")
    
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")