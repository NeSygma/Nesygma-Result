from z3 import *

# Data
warehouses = ['W1', 'W2', 'W3']
capacities = {'W1': 100, 'W2': 150, 'W3': 120}
customers = ['C1', 'C2', 'C3', 'C4', 'C5', 'C6']
demands = {'C1': 25, 'C2': 30, 'C3': 20, 'C4': 35, 'C5': 15, 'C6': 25}
distances = {
    'W1': {'C1': 10, 'C2': 15, 'C3': 25, 'C4': 20, 'C5': 30, 'C6': 12},
    'W2': {'C1': 18, 'C2': 8, 'C3': 12, 'C4': 15, 'C5': 10, 'C6': 20},
    'W3': {'C1': 22, 'C2': 25, 'C3': 8, 'C4': 18, 'C5': 12, 'C6': 15}
}

# Optimization model
opt = Optimize()

# Decision variables
# x[w][c] = 1 if customer c is assigned to warehouse w, 0 otherwise
x = {}
for w in warehouses:
    x[w] = {}
    for c in customers:
        x[w][c] = Int(f'x_{w}_{c}')
        opt.add(Or(x[w][c] == 0, x[w][c] == 1))

# y[w] = 1 if warehouse w is open, 0 otherwise
y = {w: Int(f'y_{w}') for w in warehouses}
for w in warehouses:
    opt.add(Or(y[w] == 0, y[w] == 1))

# Constraints
# 1. Each customer assigned to exactly one warehouse
for c in customers:
    opt.add(Sum([x[w][c] for w in warehouses]) == 1)

# 2. Only open warehouses can receive assignments
for w in warehouses:
    for c in customers:
        opt.add(x[w][c] <= y[w])

# 3. Warehouse capacity must not be exceeded
for w in warehouses:
    opt.add(Sum([x[w][c] * demands[c] for c in customers]) <= capacities[w])

# Objective: Minimize total cost
total_cost = Sum([x[w][c] * distances[w][c] * demands[c] for w in warehouses for c in customers])
opt.minimize(total_cost)

# Solve
result = opt.check()

if result == sat:
    m = opt.model()
    print("STATUS: sat")
    print(f"total_cost: {m.evaluate(total_cost)}")
    
    selected_warehouses = [w for w in warehouses if m.evaluate(y[w]) == 1]
    print(f"selected_warehouses: {selected_warehouses}")
    
    assignments = {}
    for c in customers:
        for w in warehouses:
            if m.evaluate(x[w][c]) == 1:
                assignments[c] = w
    print(f"assignments: {assignments}")
else:
    print("STATUS: unsat")