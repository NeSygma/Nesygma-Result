from z3 import *

BENCHMARK_MODE = True

# Data
warehouses = ["W1", "W2", "W3"]
customers = ["C1", "C2", "C3", "C4", "C5", "C6"]

demand = {"C1": 25, "C2": 30, "C3": 20, "C4": 35, "C5": 15, "C6": 25}
capacity = {"W1": 100, "W2": 150, "W3": 120}

dist = {
    ("W1","C1"): 10, ("W1","C2"): 15, ("W1","C3"): 25, ("W1","C4"): 20, ("W1","C5"): 30, ("W1","C6"): 12,
    ("W2","C1"): 18, ("W2","C2"): 8,  ("W2","C3"): 12, ("W2","C4"): 15, ("W2","C5"): 10, ("W2","C6"): 20,
    ("W3","C1"): 22, ("W3","C2"): 25, ("W3","C3"): 8,  ("W3","C4"): 18, ("W3","C5"): 12, ("W3","C6"): 15,
}

# Create variables
open_w = {w: Bool(f"open_{w}") for w in warehouses}
assign = {}
for c in customers:
    for w in warehouses:
        assign[(c,w)] = Bool(f"assign_{c}_{w}")

solver = Optimize()

# Each customer assigned to exactly one warehouse
for c in customers:
    solver.add(Sum([assign[(c,w)] for w in warehouses]) == 1)

# Capacity constraints
for w in warehouses:
    assigned_demands = [demand[c] * assign[(c,w)] for c in customers]
    solver.add(Sum(assigned_demands) <= capacity[w] * open_w[w])

# Assignment only if warehouse is open
for c in customers:
    for w in warehouses:
        solver.add(assign[(c,w)] <= open_w[w])

# Objective: minimize total transportation cost
total_cost = Sum([dist[(w,c)] * demand[c] * assign[(c,w)] for c in customers for w in warehouses])
solver.minimize(total_cost)

# Solve
result = solver.check()
if result == sat:
    print("STATUS: sat")
    m = solver.model()
    # selected warehouses
    selected = [w for w in warehouses if m[open_w[w]]]
    print("selected_warehouses:", selected)
    # assignments
    assignments = {}
    for c in customers:
        for w in warehouses:
            if m[assign[(c,w)]]:
                assignments[c] = w
                break
    print("assignments:", assignments)
    # total cost
    print("total_cost:", m[total_cost])
else:
    print("STATUS: unsat")