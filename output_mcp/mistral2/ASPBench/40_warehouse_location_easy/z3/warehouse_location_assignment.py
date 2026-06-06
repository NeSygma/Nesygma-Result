from z3 import *

# BENCHMARK_MODE: ON (model-finding mode)
BENCHMARK_MODE = True

# 1. Declare symbolic variables
# Warehouse selection (Boolean)
selected = [Bool(f'selected_{w}') for w in range(1, 4)]  # W1, W2, W3

# Customer assignments (Int representing warehouse ID)
assignments = [Int(f'assign_{c}') for c in range(1, 7)]  # C1 to C6

# 2. Add constraints
solver = Optimize()

# Helper: Map warehouse index to capacity
capacities = {1: 100, 2: 150, 3: 120}

# Helper: Map (warehouse, customer) to distance
distance = {
    (1, 1): 10, (1, 2): 15, (1, 3): 25, (1, 4): 20, (1, 5): 30, (1, 6): 12,
    (2, 1): 18, (2, 2): 8,  (2, 3): 12, (2, 4): 15, (2, 5): 10, (2, 6): 20,
    (3, 1): 22, (3, 2): 25, (3, 3): 8,  (3, 4): 18, (3, 5): 12, (3, 6): 15
}

# Helper: Customer demands
demands = {1: 25, 2: 30, 3: 20, 4: 35, 5: 15, 6: 25}

# Constraint 1: Each customer assigned to exactly one warehouse
for c in range(1, 7):
    solver.add(Or([assignments[c-1] == w for w in range(1, 4)]))

# Constraint 2: Only open warehouses can receive assignments
for c in range(1, 7):
    for w in range(1, 4):
        solver.add(Implies(assignments[c-1] == w, selected[w-1]))

# Constraint 3: Warehouse capacity not exceeded
# For each warehouse, sum demands of assigned customers <= capacity
for w in range(1, 4):
    total_assigned_demand = Sum([If(assignments[c-1] == w, demands[c], 0) for c in range(1, 7)])
    solver.add(total_assigned_demand <= capacities[w])

# Constraint 4: All customer demands satisfied (implicit in assignment and capacity)

# Objective: Minimize total transportation cost
total_cost = Sum([If(assignments[c-1] == w, distance[(w, c)] * demands[c], 0) for c in range(1, 7) for w in range(1, 4)])
solver.minimize(total_cost)

# 3. Check and print a clear result
result = solver.check()

if result == sat:
    model = solver.model()
    print("STATUS: sat")
    # Extract selected warehouses
    selected_warehouses = [w for w in range(1, 4) if is_true(model[selected[w-1]])]
    print("selected_warehouses =", selected_warehouses)
    # Extract assignments
    assignments_dict = {c: model[assignments[c-1]].as_long() for c in range(1, 7)}
    print("assignments =", assignments_dict)
    # Extract total cost
    total_cost_val = model.eval(total_cost)
    print("total_cost =", total_cost_val)
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")