from z3 import *

# Instance Data
warehouses = ["W1", "W2", "W3"]
customers = ["C1", "C2", "C3", "C4", "C5", "C6"]

capacity = {"W1": 100, "W2": 150, "W3": 120}
demand = {"C1": 25, "C2": 30, "C3": 20, "C4": 35, "C5": 15, "C6": 25}

# Distance matrix: distance[warehouse_idx][customer_idx]
dist = [
    [10, 15, 25, 20, 30, 12],  # W1
    [18,  8, 12, 15, 10, 20],  # W2
    [22, 25,  8, 18, 12, 15],  # W3
]

nW = len(warehouses)
nC = len(customers)

# Decision variables
# open[w] = 1 if warehouse w is opened, 0 otherwise
open = [Int(f"open_{w}") for w in range(nW)]

# assign[w][c] = 1 if customer c is assigned to warehouse w, 0 otherwise
assign = [[Int(f"assign_{w}_{c}") for c in range(nC)] for w in range(nW)]

opt = Optimize()

# Domain constraints: all variables are 0 or 1
for w in range(nW):
    opt.add(Or(open[w] == 0, open[w] == 1))
    for c in range(nC):
        opt.add(Or(assign[w][c] == 0, assign[w][c] == 1))

# Constraint 1: Each customer assigned to exactly one warehouse
for c in range(nC):
    opt.add(Sum([assign[w][c] for w in range(nW)]) == 1)

# Constraint 2: Only open warehouses can receive assignments
for w in range(nW):
    for c in range(nC):
        opt.add(Implies(assign[w][c] == 1, open[w] == 1))

# Constraint 3: Warehouse capacity must not be exceeded
for w in range(nW):
    total_demand = Sum([assign[w][c] * demand[customers[c]] for c in range(nC)])
    opt.add(total_demand <= capacity[warehouses[w]])

# Objective: Minimize total transportation cost
total_cost = Sum([assign[w][c] * dist[w][c] * demand[customers[c]] for w in range(nW) for c in range(nC)])
opt.minimize(total_cost)

BENCHMARK_MODE = True
result = opt.check()

if result == sat:
    m = opt.model()
    print("STATUS: sat")
    
    selected = []
    for w in range(nW):
        if m.eval(open[w]) == 1:
            selected.append(warehouses[w])
    print(f"selected_warehouses = {selected}")
    
    assignments = {}
    for c in range(nC):
        for w in range(nW):
            if m.eval(assign[w][c]) == 1:
                assignments[customers[c]] = warehouses[w]
    print(f"assignments = {assignments}")
    
    tc = m.eval(total_cost)
    print(f"total_cost = {tc}")
    
    # Verify expected optimal cost
    if tc.as_long() == 1625:
        print("Optimal cost matches expected: 1625")
    else:
        print(f"Optimal cost is {tc}, expected 1625")
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")