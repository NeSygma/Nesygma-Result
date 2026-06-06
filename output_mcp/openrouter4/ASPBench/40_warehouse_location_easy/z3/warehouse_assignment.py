from z3 import *

# Instance data
num_warehouses = 3
num_customers = 6

capacities = [100, 150, 120]
demands = [25, 30, 20, 35, 15, 25]
distances = [
    [10, 15, 25, 20, 30, 12],
    [18,  8, 12, 15, 10, 20],
    [22, 25,  8, 18, 12, 15]
]

# Variables
open_wh = [Bool(f'open_W{w+1}') for w in range(num_warehouses)]
# x[w][c] = Bool: customer c assigned to warehouse w
x = [[Bool(f'x_W{w+1}_C{c+1}') for c in range(num_customers)] for w in range(num_warehouses)]

opt = Optimize()

# Constraint 1: Each customer assigned to exactly one warehouse
for c in range(num_customers):
    opt.add(Sum([x[w][c] for w in range(num_warehouses)]) == 1)

# Constraint 2: Only open warehouses can receive assignments
for w in range(num_warehouses):
    for c in range(num_customers):
        opt.add(Implies(x[w][c], open_wh[w]))

# Constraint 3: Warehouse capacity must not be exceeded
for w in range(num_warehouses):
    opt.add(Sum([If(x[w][c], demands[c], 0) for c in range(num_customers)]) <= capacities[w])

# Objective: minimize total transportation cost
total_cost = Sum([
    If(x[w][c], distances[w][c] * demands[c], 0)
    for w in range(num_warehouses)
    for c in range(num_customers)
])
opt.minimize(total_cost)

# Solve
result = opt.check()

if result == sat:
    m = opt.model()
    print("STATUS: sat")
    # Extract open warehouses
    selected = []
    for w in range(num_warehouses):
        if is_true(m.eval(open_wh[w])):
            selected.append(f"W{w+1}")
    print(f"selected_warehouses = {selected}")
    
    # Extract assignments
    assignments = {}
    for c in range(num_customers):
        for w in range(num_warehouses):
            if is_true(m.eval(x[w][c])):
                assignments[f"C{c+1}"] = f"W{w+1}"
                break
    print(f"assignments = {assignments}")
    
    # Extract total cost
    tc = m.eval(total_cost)
    print(f"total_cost = {tc}")
else:
    print("STATUS: unsat")
    if True:  # BENCHMARK_MODE is ON
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")