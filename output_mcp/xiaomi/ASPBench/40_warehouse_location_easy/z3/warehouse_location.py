from z3 import *

# Problem Data
warehouses = ['W1', 'W2', 'W3']
customers = ['C1', 'C2', 'C3', 'C4', 'C5', 'C6']

capacity = {'W1': 100, 'W2': 150, 'W3': 120}
demand = {'C1': 25, 'C2': 30, 'C3': 20, 'C4': 35, 'C5': 15, 'C6': 25}

# Distance matrix
distance = {
    ('W1', 'C1'): 10, ('W1', 'C2'): 15, ('W1', 'C3'): 25, ('W1', 'C4'): 20, ('W1', 'C5'): 30, ('W1', 'C6'): 12,
    ('W2', 'C1'): 18, ('W2', 'C2'):  8, ('W2', 'C3'): 12, ('W2', 'C4'): 15, ('W2', 'C5'): 10, ('W2', 'C6'): 20,
    ('W3', 'C1'): 22, ('W3', 'C2'): 25, ('W3', 'C3'):  8, ('W3', 'C4'): 18, ('W3', 'C5'): 12, ('W3', 'C6'): 15,
}

opt = Optimize()

# Decision Variables
# open[w] = 1 if warehouse w is opened
open_w = {w: Bool(f'open_{w}') for w in warehouses}

# assign[c][w] = 1 if customer c is assigned to warehouse w
assign = {c: {w: Bool(f'assign_{c}_{w}') for w in warehouses} for c in customers}

# Constraints

# 1. Each customer must be assigned to exactly one warehouse
for c in customers:
    # At least one warehouse
    opt.add(Or([assign[c][w] for w in warehouses]))
    # At most one warehouse (pairwise exclusion)
    for i in range(len(warehouses)):
        for j in range(i+1, len(warehouses)):
            opt.add(Not(And(assign[c][warehouses[i]], assign[c][warehouses[j]])))

# 2. Only open warehouses can receive customer assignments
for c in customers:
    for w in warehouses:
        opt.add(Implies(assign[c][w], open_w[w]))

# 3. Warehouse capacity must not be exceeded
for w in warehouses:
    opt.add(Sum([If(assign[c][w], demand[c], 0) for c in customers]) <= capacity[w])

# Objective: minimize total transportation cost
# cost = sum over all (c, w) of distance[w,c] * demand[c] * assign[c][w]
total_cost = Sum([If(assign[c][w], distance[(w, c)] * demand[c], 0) for c in customers for w in warehouses])
opt.minimize(total_cost)

BENCHMARK_MODE = True
result = opt.check()

if result == sat:
    m = opt.model()
    print("STATUS: sat")
    
    # Extract solution
    selected = [w for w in warehouses if m.evaluate(open_w[w], model_completion=True)]
    assignments = {}
    for c in customers:
        for w in warehouses:
            if m.evaluate(assign[c][w], model_completion=True):
                assignments[c] = w
    
    # Compute total cost
    cost_val = sum(distance[(assignments[c], c)] * demand[c] for c in customers)
    
    print(f"selected_warehouses: {selected}")
    print(f"assignments: {assignments}")
    print(f"total_cost: {cost_val}")
    
    # Verify expected optimal cost
    if cost_val == 1625:
        print("VERIFIED: Optimal cost matches expected value of 1625")
    else:
        print(f"NOTE: Computed cost {cost_val} differs from expected 1625")
        
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")