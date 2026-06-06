from z3 import *

# Problem data
warehouses = ['W1', 'W2', 'W3']
capacities = {'W1': 100, 'W2': 150, 'W3': 120}

customers = ['C1', 'C2', 'C3', 'C4', 'C5', 'C6']
demands = {'C1': 25, 'C2': 30, 'C3': 20, 'C4': 35, 'C5': 15, 'C6': 25}

# Distance matrix: warehouse -> customer
# distances[warehouse][customer]
distances = {
    'W1': {'C1':10, 'C2':15, 'C3':25, 'C4':20, 'C5':30, 'C6':12},
    'W2': {'C1':18, 'C2':8,  'C3':12, 'C4':15, 'C5':10, 'C6':20},
    'W3': {'C1':22, 'C2':25, 'C3':8,  'C4':18, 'C5':12, 'C6':15}
}

# Create solver
opt = Optimize()

# Variables
open_vars = {w: Bool(f"open_{w}") for w in warehouses}
assign_vars = {(c,w): Bool(f"assign_{c}_{w}") for c in customers for w in warehouses}

# Constraints
# 1. Each customer assigned to exactly one warehouse
for c in customers:
    opt.add(Sum([If(assign_vars[(c,w)], 1, 0) for w in warehouses]) == 1)

# 2. Only open warehouses can receive assignments
for c in customers:
    for w in warehouses:
        opt.add(Implies(assign_vars[(c,w)], open_vars[w]))

# 3. Capacity constraints
for w in warehouses:
    opt.add(Sum([If(assign_vars[(c,w)], demands[c], 0) for c in customers]) <= capacities[w])

# Objective: minimize total cost
cost_expr = Sum([If(assign_vars[(c,w)], demands[c] * distances[w][c], 0) for c in customers for w in warehouses])
opt.minimize(cost_expr)

# Solve
result = opt.check()
if result == sat:
    model = opt.model()
    selected = [w for w in warehouses if is_true(model[open_vars[w]])]
    assignments = {}
    for c in customers:
        for w in warehouses:
            if is_true(model[assign_vars[(c,w)]]):
                assignments[c] = w
                break
    total_cost = model.evaluate(cost_expr, model_completion=True).as_long()
    print("STATUS: sat")
    print("selected_warehouses:", selected)
    print("assignments:", assignments)
    print("total_cost:", total_cost)
else:
    print("STATUS: unsat")