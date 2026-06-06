from z3 import *

# Problem data
hubs = ['H1', 'H2']
regionals = ['R1', 'R2', 'R3', 'R4']
customers = ['C1', 'C2', 'C3', 'C4', 'C5', 'C6']
time_slots = [1, 2, 3, 4]

# Opening costs
hub_costs = {'H1': 1000, 'H2': 1200}
regional_costs = {'R1': 200, 'R2': 250, 'R3': 220, 'R4': 180}

# Capacities
hub_caps = {'H1': 400, 'H2': 350}
regional_caps = {'R1': 70, 'R2': 80, 'R3': 60, 'R4': 90}

# Truck availability per hub per time slot (adjusted for maintenance)
truck_limits = {
    'H1': {1: 2, 2: 2, 3: 2, 4: 0},  # H1 unavailable at time slot 4
    'H2': {1: 1, 2: 1, 3: 1, 4: 1}
}

# Customer demands and time windows
customer_data = {
    'C1': {'demand': 20, 'window': [2, 3]},
    'C2': {'demand': 30, 'window': [1, 2]},
    'C3': {'demand': 15, 'window': [3, 4]},
    'C4': {'demand': 25, 'window': [1, 4]},
    'C5': {'demand': 35, 'window': [2, 4]},
    'C6': {'demand': 10, 'window': [1, 1]}
}

# Transportation costs (per unit)
hub_to_regional = {
    ('H1', 'R1'): 5,
    ('H1', 'R2'): 6,
    ('H2', 'R3'): 5,
    ('H2', 'R4'): 6
}

regional_to_customer = {
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
hub_regional_allowed = {
    'H1': ['R1', 'R2'],
    'H2': ['R3', 'R4']
}

regional_customer_allowed = {
    'R1': ['C1', 'C2'],
    'R2': ['C2', 'C3'],
    'R3': ['C4', 'C5'],
    'R4': ['C5', 'C6']
}

# Maintenance schedules
maintenance = {
    'R2': [2],  # unavailable at time slot 2
    'H1': [4]   # unavailable at time slot 4
}

# Create optimizer
opt = Optimize()

# Decision variables
open_hubs = {h: Bool(f'open_hub_{h}') for h in hubs}
open_regionals = {r: Bool(f'open_regional_{r}') for r in regionals}

# Supply variables: which hub supplies which regional warehouse
supply = {}
for h in hubs:
    for r in regionals:
        supply[(h, r)] = Bool(f'supply_{h}_{r}')

# Assignment variables: which customer is served by which regional warehouse at which time
assign = {}
for c in customers:
    for r in regionals:
        for t in time_slots:
            assign[(c, r, t)] = Bool(f'assign_{c}_{r}_{t}')

# 1. Opening prerequisite: Customer can only be served by open regional warehouse supplied by open hub
for c in customers:
    for r in regionals:
        for t in time_slots:
            # If customer is assigned to regional warehouse r at time t, then:
            # - regional warehouse r must be open
            # - there must exist a hub h that supplies r and is open
            supplier_exists = Or([And(supply[(h, r)], open_hubs[h]) for h in hubs])
            opt.add(Implies(assign[(c, r, t)], And(open_regionals[r], supplier_exists)))

# 2. Assignment uniqueness: Each customer assigned to exactly one regional warehouse at exactly one time
for c in customers:
    opt.add(Sum([assign[(c, r, t)] for r in regionals for t in time_slots]) == 1)

# 3. Supply uniqueness: Each open regional warehouse supplied by exactly one hub
for r in regionals:
    # Sum of supply variables for this regional warehouse must equal 1 if open, 0 if closed
    opt.add(Sum([supply[(h, r)] for h in hubs]) == If(open_regionals[r], 1, 0))

# 4. Connectivity constraints
# Hub to regional allowed pairs
for h in hubs:
    for r in regionals:
        if r not in hub_regional_allowed[h]:
            opt.add(Not(supply[(h, r)]))

# Regional to customer allowed pairs
for r in regionals:
    for c in customers:
        if c not in regional_customer_allowed[r]:
            for t in time_slots:
                opt.add(Not(assign[(c, r, t)]))

# 5. Time windows
for c in customers:
    window = customer_data[c]['window']
    for t in time_slots:
        if t < window[0] or t > window[1]:
            for r in regionals:
                opt.add(Not(assign[(c, r, t)]))

# 6. Maintenance constraints
# R2 unavailable at time slot 2
for c in customers:
    opt.add(Not(assign[(c, 'R2', 2)]))

# H1 unavailable at time slot 4: This affects truck limits (already set to 0)

# 7. Regional capacity constraints
for r in regionals:
    total_demand = Sum([If(assign[(c, r, t)], customer_data[c]['demand'], 0) 
                       for c in customers for t in time_slots])
    opt.add(total_demand <= regional_caps[r])

# 8. Hub capacity constraints
for h in hubs:
    total_demand = 0
    for r in regionals:
        # Demand served by regional warehouse r (if supplied by hub h)
        regional_demand = Sum([If(assign[(c, r, t)], customer_data[c]['demand'], 0) 
                              for c in customers for t in time_slots])
        # Only count if hub h supplies r
        total_demand += If(supply[(h, r)], regional_demand, 0)
    opt.add(total_demand <= hub_caps[h])

# 9. Truck limits
for h in hubs:
    for t in time_slots:
        # Number of deliveries from regional warehouses supplied by hub h at time t
        deliveries = Sum([If(And(supply[(h, r)], assign[(c, r, t)]), 1, 0) 
                         for r in regionals for c in customers])
        opt.add(deliveries <= truck_limits[h][t])

# Objective: Minimize total cost
# Fixed opening costs
fixed_cost = Sum([If(open_hubs[h], hub_costs[h], 0) for h in hubs]) + \
             Sum([If(open_regionals[r], regional_costs[r], 0) for r in regionals])

# Hub-to-regional transport costs
hub_regional_cost = 0
for r in regionals:
    for h in hubs:
        if (h, r) in hub_to_regional:
            # Total demand served by regional warehouse r
            regional_demand = Sum([If(assign[(c, r, t)], customer_data[c]['demand'], 0) 
                                  for c in customers for t in time_slots])
            unit_cost = hub_to_regional[(h, r)]
            hub_regional_cost += If(supply[(h, r)], regional_demand * unit_cost, 0)

# Regional-to-customer transport costs
regional_customer_cost = 0
for c in customers:
    for r in regionals:
        if (r, c) in regional_to_customer:
            unit_cost = regional_to_customer[(r, c)]
            for t in time_slots:
                regional_customer_cost += If(assign[(c, r, t)], customer_data[c]['demand'] * unit_cost, 0)

total_cost = fixed_cost + hub_regional_cost + regional_customer_cost

# Minimize total cost
opt.minimize(total_cost)

# Solve
print("Solving distribution network optimization...")
result = opt.check()

if result == sat:
    model = opt.model()
    print("STATUS: sat")
    
    # Extract solution
    open_hubs_sol = [h for h in hubs if is_true(model[open_hubs[h]])]
    open_regionals_sol = [r for r in regionals if is_true(model[open_regionals[r]])]
    
    # Hub assignments
    hub_assignments = {}
    for r in regionals:
        if is_true(model[open_regionals[r]]):
            for h in hubs:
                if is_true(model[supply[(h, r)]]):
                    hub_assignments[r] = h
                    break
    
    # Customer deliveries
    customer_deliveries = []
    for c in customers:
        for r in regionals:
            for t in time_slots:
                if is_true(model[assign[(c, r, t)]]):
                    customer_deliveries.append({
                        'customer': c,
                        'regional': r,
                        'time_slot': t
                    })
    
    # Calculate total cost from model
    total_cost_val = model.evaluate(total_cost)
    
    print(f"open_hubs: {open_hubs_sol}")
    print(f"open_regionals: {open_regionals_sol}")
    print(f"hub_assignments: {hub_assignments}")
    print(f"customer_deliveries: {customer_deliveries}")
    print(f"total_cost: {total_cost_val}")
    
    # Verify the expected cost
    if total_cost_val == 5215:
        print("SUCCESS: Total cost matches expected minimum of 5215")
    else:
        print(f"NOTE: Total cost is {total_cost_val}, expected 5215")
        
elif result == unsat:
    print("STATUS: unsat")
    print("No feasible solution found - constraints may be too strict")
elif result == unknown:
    print("STATUS: unknown")
    print("Solver could not determine satisfiability")
else:
    print("STATUS: unknown")
    print(f"Unexpected solver result: {result}")