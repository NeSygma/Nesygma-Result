from z3 import *

# Problem data
warehouses = ["W1", "W2", "W3"]
customers = ["C1", "C2", "C3", "C4", "C5", "C6"]

# Capacities: [W1, W2, W3]
capacities = [100, 150, 120]

# Demands: [C1, C2, C3, C4, C5, C6]
demands = [25, 30, 20, 35, 15, 25]

# Distance matrix: distance[warehouse][customer]
distance = [
    [10, 15, 25, 20, 30, 12],  # W1
    [18, 8, 12, 15, 10, 20],   # W2
    [22, 25, 8, 18, 12, 15]    # W3
]

# Create solver
solver = Solver()

# Decision variables
# selected[i] = True if warehouse i is opened
selected = [Bool(f"selected_{i}") for i in range(3)]

# assignment[i][j] = True if customer j is assigned to warehouse i
assignment = [[Bool(f"assign_{i}_{j}") for j in range(6)] for i in range(3)]

# Total cost variable
total_cost = Int("total_cost")

# Constraint 1: Each customer assigned to exactly one warehouse
for j in range(6):
    solver.add(Sum([If(assignment[i][j], 1, 0) for i in range(3)]) == 1)

# Constraint 2: Only open warehouses can receive assignments
for i in range(3):
    for j in range(6):
        solver.add(Implies(assignment[i][j], selected[i]))

# Constraint 3: Warehouse capacity constraints
for i in range(3):
    # Sum of demands assigned to warehouse i must not exceed capacity
    assigned_demand = Sum([If(assignment[i][j], demands[j], 0) for j in range(6)])
    solver.add(assigned_demand <= capacities[i])

# Constraint 4: Total cost calculation
# cost = Σ(distance[i][j] × demand[j] × assignment[i][j])
cost_terms = []
for i in range(3):
    for j in range(6):
        cost_terms.append(If(assignment[i][j], distance[i][j] * demands[j], 0))
solver.add(total_cost == Sum(cost_terms))

# Objective: Minimize total cost
# We'll use the Optimize solver for minimization
opt = Optimize()

# Add all constraints to the optimizer
for c in solver.assertions():
    opt.add(c)

# Minimize total cost
opt.minimize(total_cost)

# Check for solution
BENCHMARK_MODE = True
result = opt.check()

if result == sat:
    model = opt.model()
    print("STATUS: sat")
    
    # Extract selected warehouses
    selected_warehouses = []
    for i in range(3):
        if is_true(model[selected[i]]):
            selected_warehouses.append(warehouses[i])
    
    # Extract assignments
    assignments = {}
    for j in range(6):
        for i in range(3):
            if is_true(model[assignment[i][j]]):
                assignments[customers[j]] = warehouses[i]
    
    # Get total cost
    total_cost_value = model[total_cost]
    
    print(f"selected_warehouses: {selected_warehouses}")
    print(f"assignments: {assignments}")
    print(f"total_cost: {total_cost_value}")
    
    # Verify the expected optimal cost
    if total_cost_value == 1625:
        print("Optimal cost matches expected value: 1625")
    
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")