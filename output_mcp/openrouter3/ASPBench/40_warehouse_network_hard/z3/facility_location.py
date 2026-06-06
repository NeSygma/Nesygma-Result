from z3 import *

# Problem data
hubs = ['H1', 'H2']
regionals = ['R1', 'R2', 'R3', 'R4']
customers = ['C1', 'C2', 'C3', 'C4', 'C5', 'C6']
time_slots = [1, 2, 3, 4]

# Opening costs
hub_opening_cost = {'H1': 1000, 'H2': 1200}
regional_opening_cost = {'R1': 200, 'R2': 250, 'R3': 220, 'R4': 180}

# Capacities
hub_capacity = {'H1': 400, 'H2': 350}
regional_capacity = {'R1': 70, 'R2': 80, 'R3': 60, 'R4': 90}

# Truck resources per hub per time slot
truck_limit = {'H1': 2, 'H2': 1}

# Customer demands and time windows
customer_demand = {'C1': 20, 'C2': 30, 'C3': 15, 'C4': 25, 'C5': 35, 'C6': 10}
customer_time_windows = {
    'C1': [2, 3],
    'C2': [1, 2],
    'C3': [3, 4],
    'C4': [1, 4],
    'C5': [2, 4],
    'C6': [1, 1]
}

# Transportation costs
hub_to_regional_cost = {
    ('H1', 'R1'): 5,
    ('H1', 'R2'): 6,
    ('H2', 'R3'): 5,
    ('H2', 'R4'): 6
}

regional_to_customer_cost = {
    ('R1', 'C1'): 10,
    ('R1', 'C2'): 12,
    ('R2', 'C2'): 13,
    ('R2', 'C3'): 15,
    ('R3', 'C4'): 9,
    ('R3', 'C5'): 11,
    ('R4', 'C5'): 14,
    ('R4', 'C6'): 7
}

# Connectivity constraints
hub_to_regional_connectivity = {
    'H1': ['R1', 'R2'],
    'H2': ['R3', 'R4']
}

regional_to_customer_connectivity = {
    'R1': ['C1', 'C2'],
    'R2': ['C2', 'C3'],
    'R3': ['C4', 'C5'],
    'R4': ['C5', 'C6']
}

# Maintenance schedules
maintenance = {
    'R2': [2],  # R2 unavailable at time slot 2
    'H1': [4]   # H1 unavailable at time slot 4
}

# Create solver
solver = Solver()

# Decision variables
open_h = {h: Bool(f'open_h_{h}') for h in hubs}
open_r = {r: Bool(f'open_r_{r}') for r in regionals}

# Hub assignment for each regional warehouse (which hub supplies it)
# Use integer variable: 0 for H1, 1 for H2 (or -1 if not assigned)
hub_assign = {r: Int(f'hub_assign_{r}') for r in regionals}

# Customer assignment: customer c assigned to regional warehouse r at time t
customer_assign = {}
for c in customers:
    for r in regionals:
        for t in time_slots:
            customer_assign[(c, r, t)] = Bool(f'assign_{c}_{r}_{t}')

# 1. Opening prerequisite: A customer can only be served by an open regional warehouse,
#    which must be supplied by an open hub
for c in customers:
    for r in regionals:
        for t in time_slots:
            # If customer c is assigned to regional r at time t, then r must be open
            solver.add(Implies(customer_assign[(c, r, t)], open_r[r]))
            # If regional r is assigned to a hub, that hub must be open
            # We'll handle this through hub_assign constraints

# 2. Assignment uniqueness: Each customer must be assigned to exactly one regional warehouse at exactly one time slot
for c in customers:
    # Sum over all regions and time slots
    assignments = [customer_assign[(c, r, t)] for r in regionals for t in time_slots]
    solver.add(Sum([If(a, 1, 0) for a in assignments]) == 1)

# 3. Supply uniqueness: Each open regional warehouse must be supplied by exactly one hub
for r in regionals:
    # If regional r is open, it must be assigned to exactly one hub
    # hub_assign[r] should be 0 for H1, 1 for H2
    solver.add(Implies(open_r[r], Or(hub_assign[r] == 0, hub_assign[r] == 1)))
    # If regional r is not open, hub_assign[r] can be anything (we'll handle with constraints)
    # Actually, we need to ensure that if not open, it's not assigned to any hub
    # We'll handle this by ensuring hub_assign only matters when open_r is true

# 4. Connectivity: Hub-to-Regional assignments must respect connectivity
for h in hubs:
    for r in regionals:
        if r not in hub_to_regional_connectivity[h]:
            # If r is not in h's connectivity list, then h cannot supply r
            # This means if hub_assign[r] corresponds to h, then open_r[r] must be false
            # But we need to map hub names to indices
            h_index = hubs.index(h)
            solver.add(Implies(hub_assign[r] == h_index, Not(open_r[r])))

# 5. Regional-to-Customer connectivity
for r in regionals:
    for c in customers:
        if c not in regional_to_customer_connectivity[r]:
            # If c is not in r's connectivity list, then r cannot serve c
            for t in time_slots:
                solver.add(Not(customer_assign[(c, r, t)]))

# 6. Time windows: Customer deliveries must occur within their specified time windows
for c in customers:
    min_t, max_t = customer_time_windows[c]
    for r in regionals:
        for t in time_slots:
            if t < min_t or t > max_t:
                solver.add(Not(customer_assign[(c, r, t)]))

# 7. Maintenance: No deliveries can pass through facilities during their maintenance time slots
# For regional warehouses
for r in regionals:
    if r in maintenance:
        for t in maintenance[r]:
            # No customer can be assigned to r at time t
            for c in customers:
                solver.add(Not(customer_assign[(c, r, t)]))

# For hubs: H1 unavailable at time slot 4
# This means no deliveries can pass through H1 at time slot 4
# Since deliveries are assigned to regional warehouses at specific times,
# and regional warehouses are supplied by hubs, we need to ensure that
# if a regional warehouse is supplied by H1, it cannot serve customers at time slot 4
for r in regionals:
    if 'H1' in hub_to_regional_connectivity:
        # Check if r can be supplied by H1
        if r in hub_to_regional_connectivity['H1']:
            for t in [4]:  # H1 maintenance at time slot 4
                for c in customers:
                    # If r is supplied by H1 and customer c is assigned to r at time t, that's invalid
                    # We need to express: hub_assign[r] == 0 (H1) implies not customer_assign at t=4
                    solver.add(Implies(
                        And(hub_assign[r] == 0, customer_assign[(c, r, t)]),
                        False
                    ))

# 8. Regional capacity: Total demand served by each regional warehouse cannot exceed its capacity
for r in regionals:
    # Sum of demands of customers assigned to r (across all time slots)
    total_demand_r = Sum([
        If(customer_assign[(c, r, t)], customer_demand[c], 0)
        for c in customers for t in time_slots
    ])
    solver.add(Implies(open_r[r], total_demand_r <= regional_capacity[r]))

# 9. Hub capacity: Total demand passing through each hub cannot exceed hub capacity
for h in hubs:
    h_index = hubs.index(h)
    # Sum of demands of all regional warehouses supplied by this hub
    total_demand_h = Sum([
        If(And(open_r[r], hub_assign[r] == h_index), 
           Sum([If(customer_assign[(c, r, t)], customer_demand[c], 0) for c in customers for t in time_slots]),
           0)
        for r in regionals
    ])
    solver.add(Implies(open_h[h], total_demand_h <= hub_capacity[h]))

# 10. Truck limits: Number of customer deliveries in each time slot from regional warehouses
#     supplied by a hub cannot exceed the hub's available trucks for that time slot
for h in hubs:
    h_index = hubs.index(h)
    for t in time_slots:
        # Count deliveries at time t from regional warehouses supplied by hub h
        delivery_count = Sum([
            If(And(open_r[r], hub_assign[r] == h_index, customer_assign[(c, r, t)]), 1, 0)
            for r in regionals for c in customers
        ])
        solver.add(Implies(open_h[h], delivery_count <= truck_limit[h]))

# Additional constraint: If a regional warehouse is not open, it cannot be assigned to any hub
# We'll ensure this by making hub_assign irrelevant when open_r is false
# Actually, we need to ensure that if open_r is false, then no customer is assigned to it
for r in regionals:
    for c in customers:
        for t in time_slots:
            solver.add(Implies(Not(open_r[r]), Not(customer_assign[(c, r, t)])))

# Objective: Minimize total cost
# Fixed opening costs
fixed_cost = Sum([
    If(open_h[h], hub_opening_cost[h], 0) for h in hubs
]) + Sum([
    If(open_r[r], regional_opening_cost[r], 0) for r in regionals
])

# Hub-to-Regional transport costs
hub_to_regional_transport_cost = Sum([
    If(And(open_r[r], hub_assign[r] == hubs.index(h)),
       Sum([If(customer_assign[(c, r, t)], customer_demand[c], 0) for c in customers for t in time_slots]) * hub_to_regional_cost[(h, r)],
       0)
    for h in hubs for r in regionals if (h, r) in hub_to_regional_cost
])

# Regional-to-Customer transport costs
regional_to_customer_transport_cost = Sum([
    If(customer_assign[(c, r, t)], customer_demand[c] * regional_to_customer_cost[(r, c)], 0)
    for c in customers for r in regionals for t in time_slots
    if (r, c) in regional_to_customer_cost
])

total_cost = fixed_cost + hub_to_regional_transport_cost + regional_to_customer_transport_cost

# Minimize total cost
opt = Optimize()
opt.add([solver.assertions()])  # Add all constraints from solver
opt.minimize(total_cost)

# Check and print results
BENCHMARK_MODE = True
result = opt.check()

if result == sat:
    model = opt.model()
    print("STATUS: sat")
    
    # Extract solution
    open_hubs = [h for h in hubs if is_true(model[open_h[h]])]
    open_regionals = [r for r in regionals if is_true(model[open_r[r]])]
    
    # Hub assignments
    hub_assignments = {}
    for r in regionals:
        if is_true(model[open_r[r]]):
            hub_idx = model[hub_assign[r]].as_long()
            hub_assignments[r] = hubs[hub_idx]
    
    # Customer deliveries
    customer_deliveries = []
    for c in customers:
        for r in regionals:
            for t in time_slots:
                if is_true(model[customer_assign[(c, r, t)]]):
                    customer_deliveries.append({
                        'customer': c,
                        'warehouse': r,
                        'time_slot': t
                    })
    
    # Calculate total cost from model
    total_cost_value = model.eval(total_cost).as_long()
    
    print(f"open_hubs: {open_hubs}")
    print(f"open_regionals: {open_regionals}")
    print(f"hub_assignments: {hub_assignments}")
    print(f"customer_deliveries: {customer_deliveries}")
    print(f"total_cost: {total_cost_value}")
    
    # Check if we found the expected optimal cost
    if total_cost_value == 5215:
        print("Optimal solution found with expected cost!")
    else:
        print(f"Note: Found cost {total_cost_value}, expected 5215")
        
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")