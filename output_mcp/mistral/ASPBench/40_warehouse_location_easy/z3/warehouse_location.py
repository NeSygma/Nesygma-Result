from z3 import *

# BENCHMARK_MODE: ON (problem is guaranteed solvable)
BENCHMARK_MODE = True

# Create optimizer instance for minimization
opt = Optimize()

# === 1. Declare symbolic variables ===
# Warehouse selection: 1 if open, 0 if closed
W1_open = Bool('W1_open')
W2_open = Bool('W2_open')
W3_open = Bool('W3_open')

# Customer assignments: which warehouse each customer is assigned to
# We'll use Int variables with values 1, 2, 3 representing W1, W2, W3
C1_assign = Int('C1_assign')
C2_assign = Int('C2_assign')
C3_assign = Int('C3_assign')
C4_assign = Int('C4_assign')
C5_assign = Int('C5_assign')
C6_assign = Int('C6_assign')

# === 2. Add constraints ===

# Constraint: Each customer must be assigned to exactly one warehouse
# We'll constrain the assignment variables to be in {1, 2, 3}
opt.add(C1_assign >= 1, C1_assign <= 3)
opt.add(C2_assign >= 1, C2_assign <= 3)
opt.add(C3_assign >= 1, C3_assign <= 3)
opt.add(C4_assign >= 1, C4_assign <= 3)
opt.add(C5_assign >= 1, C5_assign <= 3)
opt.add(C6_assign >= 1, C6_assign <= 3)

# Constraint: Only open warehouses can receive assignments
# If a warehouse is closed (False), no customer can be assigned to it
# We'll enforce this by ensuring that if a warehouse is closed, 
# no assignment variable equals its ID
opt.add(Implies(Not(W1_open), C1_assign != 1))
opt.add(Implies(Not(W1_open), C2_assign != 1))
opt.add(Implies(Not(W1_open), C3_assign != 1))
opt.add(Implies(Not(W1_open), C4_assign != 1))
opt.add(Implies(Not(W1_open), C5_assign != 1))
opt.add(Implies(Not(W1_open), C6_assign != 1))

opt.add(Implies(Not(W2_open), C1_assign != 2))
opt.add(Implies(Not(W2_open), C2_assign != 2))
opt.add(Implies(Not(W2_open), C3_assign != 2))
opt.add(Implies(Not(W2_open), C4_assign != 2))
opt.add(Implies(Not(W2_open), C5_assign != 2))
opt.add(Implies(Not(W2_open), C6_assign != 2))

opt.add(Implies(Not(W3_open), C1_assign != 3))
opt.add(Implies(Not(W3_open), C2_assign != 3))
opt.add(Implies(Not(W3_open), C3_assign != 3))
opt.add(Implies(Not(W3_open), C4_assign != 3))
opt.add(Implies(Not(W3_open), C5_assign != 3))
opt.add(Implies(Not(W3_open), C6_assign != 3))

# Constraint: Warehouse capacity must not be exceeded
# We need to count the total demand assigned to each warehouse
# and ensure it's <= capacity

# Demands for each customer
C1_demand = 25
C2_demand = 30
C3_demand = 20
C4_demand = 35
C5_demand = 15
C6_demand = 25

# Total demand assigned to each warehouse
# We'll use If expressions to sum demands based on assignments
W1_total = Sum(
    If(C1_assign == 1, C1_demand, 0),
    If(C2_assign == 1, C2_demand, 0),
    If(C3_assign == 1, C3_demand, 0),
    If(C4_assign == 1, C4_demand, 0),
    If(C5_assign == 1, C5_demand, 0),
    If(C6_assign == 1, C6_demand, 0)
)

W2_total = Sum(
    If(C1_assign == 2, C1_demand, 0),
    If(C2_assign == 2, C2_demand, 0),
    If(C3_assign == 2, C3_demand, 0),
    If(C4_assign == 2, C4_demand, 0),
    If(C5_assign == 2, C5_demand, 0),
    If(C6_assign == 2, C6_demand, 0)
)

W3_total = Sum(
    If(C1_assign == 3, C1_demand, 0),
    If(C2_assign == 3, C2_demand, 0),
    If(C3_assign == 3, C3_demand, 0),
    If(C4_assign == 3, C4_demand, 0),
    If(C5_assign == 3, C5_demand, 0),
    If(C6_assign == 3, C6_demand, 0)
)

# Capacity constraints
opt.add(W1_total <= 100)
opt.add(W2_total <= 150)
opt.add(W3_total <= 120)

# === 3. Define the objective function ===
# Transportation cost = distance * demand for each assignment
# Distance matrix (warehouse to customer):
#      C1  C2  C3  C4  C5  C6
# W1:  10  15  25  20  30  12
# W2:  18   8  12  15  10  20
# W3:  22  25   8  18  12  15

# Cost for each customer based on assignment
C1_cost = If(C1_assign == 1, 10 * C1_demand,
             If(C1_assign == 2, 18 * C1_demand,
             22 * C1_demand))

C2_cost = If(C2_assign == 1, 15 * C2_demand,
             If(C2_assign == 2, 8 * C2_demand,
             25 * C2_demand))

C3_cost = If(C3_assign == 1, 25 * C3_demand,
             If(C3_assign == 2, 12 * C3_demand,
             8 * C3_demand))

C4_cost = If(C4_assign == 1, 20 * C4_demand,
             If(C4_assign == 2, 15 * C4_demand,
             18 * C4_demand))

C5_cost = If(C5_assign == 1, 30 * C5_demand,
             If(C5_assign == 2, 10 * C5_demand,
             12 * C5_demand))

C6_cost = If(C6_assign == 1, 12 * C6_demand,
             If(C6_assign == 2, 20 * C6_demand,
             15 * C6_demand))

# Total cost to minimize
total_cost = C1_cost + C2_cost + C3_cost + C4_cost + C5_cost + C6_cost

# Minimize the total cost
opt.minimize(total_cost)

# === 4. Solve and output results ===
result = opt.check()

if result == sat:
    model = opt.model()
    
    # Extract warehouse selection
    selected_warehouses = []
    if is_true(model[W1_open]):
        selected_warehouses.append(1)
    if is_true(model[W2_open]):
        selected_warehouses.append(2)
    if is_true(model[W3_open]):
        selected_warehouses.append(3)
    
    # Extract assignments
    assignments = {
        'C1': model[C1_assign].as_long(),
        'C2': model[C2_assign].as_long(),
        'C3': model[C3_assign].as_long(),
        'C4': model[C4_assign].as_long(),
        'C5': model[C5_assign].as_long(),
        'C6': model[C6_assign].as_long()
    }
    
    # Extract total cost
    total_cost_value = model.eval(total_cost)
    
    print("STATUS: sat")
    print(f"selected_warehouses = {selected_warehouses}")
    print(f"assignments = {assignments}")
    print(f"total_cost = {total_cost_value}")
    
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")