from z3 import *

# Instance data
warehouses = ['W1', 'W2', 'W3']
customers = ['C1', 'C2', 'C3', 'C4', 'C5', 'C6']
capacity = {'W1': 100, 'W2': 150, 'W3': 120}
demand = {'C1': 25, 'C2': 30, 'C3': 20, 'C4': 35, 'C5': 15, 'C6': 25}

# Distance matrix (warehouse to customer)
distance = {
    ('W1', 'C1'): 10, ('W1', 'C2'): 15, ('W1', 'C3'): 25,
    ('W1', 'C4'): 20, ('W1', 'C5'): 30, ('W1', 'C6'): 12,
    ('W2', 'C1'): 18, ('W2', 'C2'): 8,  ('W2', 'C3'): 12,
    ('W2', 'C4'): 15, ('W2', 'C5'): 10, ('W2', 'C6'): 20,
    ('W3', 'C1'): 22, ('W3', 'C2'): 25, ('W3', 'C3'): 8,
    ('W3', 'C4'): 18, ('W3', 'C5'): 12, ('W3', 'C6'): 15
}

# Precompute cost = distance * demand
cost = {}
for w in warehouses:
    for c in customers:
        cost[(w, c)] = distance[(w, c)] * demand[c]

# Create solver (Optimize for minimization)
opt = Optimize()

# Decision variables
open_w = {w: Bool(f'open_{w}') for w in warehouses}
assign = {}
for w in warehouses:
    for c in customers:
        assign[(w, c)] = Bool(f'assign_{w}_{c}')

# Each customer assigned to exactly one warehouse
for c in customers:
    opt.add(Sum([If(assign[(w, c)], 1, 0) for w in warehouses]) == 1)

# Capacity constraints: sum of assigned demands <= capacity
for w in warehouses:
    total_demand = Sum([If(assign[(w, c)], demand[c], 0) for c in customers])
    opt.add(total_demand <= capacity[w])

# Only open warehouses can receive assignments
for w in warehouses:
    for c in customers:
        opt.add(Implies(Not(open_w[w]), Not(assign[(w, c)])))

# Objective: minimize total cost
total_cost = Sum([If(assign[(w, c)], cost[(w, c)], 0) for w in warehouses for c in customers])
opt.minimize(total_cost)

# Check and print results
BENCHMARK_MODE = True
result = opt.check()

if result == sat:
    model = opt.model()
    print("STATUS: sat")
    
    # Determine which warehouses are open
    selected_warehouses = []
    for w in warehouses:
        if is_true(model[open_w[w]]):
            selected_warehouses.append(w)
    
    # Determine assignments
    assignments = {}
    for c in customers:
        for w in warehouses:
            if is_true(model[assign[(w, c)]]):
                assignments[c] = w
                break
    
    # Calculate total cost from model
    total_cost_value = 0
    for w in warehouses:
        for c in customers:
            if is_true(model[assign[(w, c)]]):
                total_cost_value += cost[(w, c)]
    
    print(f"selected_warehouses: {selected_warehouses}")
    print(f"assignments: {assignments}")
    print(f"total_cost: {total_cost_value}")
    
    # Verify expected optimal cost
    if total_cost_value == 1625:
        print("Matches expected optimal cost of 1625")
    else:
        print(f"Note: Expected 1625, got {total_cost_value}")
        
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")