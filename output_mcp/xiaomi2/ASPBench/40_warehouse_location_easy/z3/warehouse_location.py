from z3 import *

# Problem data
warehouses = ['W1', 'W2', 'W3']
customers = ['C1', 'C2', 'C3', 'C4', 'C5', 'C6']

capacity = {'W1': 100, 'W2': 150, 'W3': 120}
demand = {'C1': 25, 'C2': 30, 'C3': 20, 'C4': 35, 'C5': 15, 'C6': 25}

# Distance matrix: distance[w][c]
distance = {
    'W1': {'C1': 10, 'C2': 15, 'C3': 25, 'C4': 20, 'C5': 30, 'C6': 12},
    'W2': {'C1': 18, 'C2':  8, 'C3': 12, 'C4': 15, 'C5': 10, 'C6': 20},
    'W3': {'C1': 22, 'C2': 25, 'C3':  8, 'C4': 18, 'C5': 12, 'C6': 15},
}

opt = Optimize()

# Decision variables
open_w = {w: Bool(f'open_{w}') for w in warehouses}
assign = {(c, w): Bool(f'assign_{c}_{w}') for c in customers for w in warehouses}

# Constraint 1: Each customer assigned to exactly one warehouse
for c in customers:
    # At least one
    opt.add(Or([assign[c, w] for w in warehouses]))
    # At most one (pairwise)
    for i in range(len(warehouses)):
        for j in range(i+1, len(warehouses)):
            opt.add(Not(And(assign[c, warehouses[i]], assign[c, warehouses[j]])))

# Constraint 2: Assignment implies warehouse is open
for c in customers:
    for w in warehouses:
        opt.add(Implies(assign[c, w], open_w[w]))

# Constraint 3: Warehouse capacity not exceeded
for w in warehouses:
    opt.add(Sum([If(assign[c, w], demand[c], 0) for c in customers]) <= capacity[w])

# Objective: minimize total transportation cost
total_cost = Sum([If(assign[c, w], distance[w][c] * demand[c], 0)
                  for c in customers for w in warehouses])
opt.minimize(total_cost)

result = opt.check()
if result == sat:
    model = opt.model()
    print("STATUS: sat")
    
    # Extract selected warehouses
    selected = [w for w in warehouses if is_true(model[open_w[w]])]
    print(f"selected_warehouses: {selected}")
    
    # Extract assignments
    assignments = {}
    for c in customers:
        for w in warehouses:
            if is_true(model[assign[c, w]]):
                assignments[c] = w
                break
    print(f"assignments: {assignments}")
    
    # Compute and print total cost
    cost_val = sum(distance[assignments[c]][c] * demand[c] for c in customers)
    print(f"total_cost: {cost_val}")
    
    # Print detailed breakdown
    print("\nBreakdown:")
    for c in customers:
        w = assignments[c]
        d = distance[w][c]
        dem = demand[c]
        print(f"  {c} -> {w}: distance={d}, demand={dem}, cost={d*dem}")
else:
    print(f"STATUS: {result}")