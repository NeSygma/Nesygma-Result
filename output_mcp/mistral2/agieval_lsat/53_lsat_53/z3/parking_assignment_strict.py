from z3 import *

# Declare employees and parking spaces
employees = ["Robertson", "Souza", "Togowa", "Vaughn", "Xu", "Young"]

# Create a dictionary to map employees to their assigned spaces
assign = {e: Int(f"assign_{e}") for e in employees}

# Create the solver
solver = Solver()

# Each employee is assigned a unique space
solver.add(Distinct(list(assign.values())))

# Constraints
# 1. Young > Togowa
solver.add(assign["Young"] > assign["Togowa"])

# 2. Xu > Souza
solver.add(assign["Xu"] > assign["Souza"])

# 3. Robertson > Young
solver.add(assign["Robertson"] > assign["Young"])

# 4. Robertson ∈ {1, 2, 3, 4}
solver.add(Or([assign["Robertson"] == i for i in [1, 2, 3, 4]]))

# Given condition: Robertson = 3
solver.add(assign["Robertson"] == 3)

# Now, evaluate each option
found_options = []

# Option A: Souza is assigned parking space #4
solver.push()
solver.add(assign["Souza"] == 4)
result = solver.check()
if result == sat:
    m = solver.model()
    # Verify Xu > Souza (Xu must be > 4, so Xu must be 5 or 6)
    # Verify Young > Togowa
    # Verify Robertson > Young (Robertson = 3, so Young must be < 3)
    if m[assign["Xu"]].as_long() > 4 and m[assign["Young"]].as_long() < 3:
        found_options.append("A")
    else:
        # This assignment is invalid due to other constraints
        pass
solver.pop()

# Option B: Togowa is assigned parking space #2
solver.push()
solver.add(assign["Togowa"] == 2)
result = solver.check()
if result == sat:
    m = solver.model()
    # Verify Young > Togowa (Young must be > 2)
    # Verify Robertson > Young (Robertson = 3, so Young must be < 3)
    if m[assign["Young"]].as_long() > 2 and m[assign["Young"]].as_long() < 3:
        # Young must be an integer, so this is impossible
        pass
    else:
        found_options.append("B")
solver.pop()

# Option C: Vaughn is assigned parking space #5
solver.push()
solver.add(assign["Vaughn"] == 5)
result = solver.check()
if result == sat:
    m = solver.model()
    # Verify all constraints are satisfied
    # No direct constraints on Vaughn, so this is valid
    found_options.append("C")
solver.pop()

# Option D: Xu is assigned parking space #6
solver.push()
solver.add(assign["Xu"] == 6)
result = solver.check()
if result == sat:
    m = solver.model()
    # Verify Xu > Souza (Souza must be < 6)
    # Verify Young > Togowa
    # Verify Robertson > Young (Robertson = 3, so Young must be < 3)
    if m[assign["Souza"]].as_long() < 6 and m[assign["Young"]].as_long() < 3:
        found_options.append("D")
    else:
        pass
solver.pop()

# Option E: Young is assigned parking space #2
solver.push()
solver.add(assign["Young"] == 2)
result = solver.check()
if result == sat:
    m = solver.model()
    # Verify Robertson > Young (Robertson = 3, so Young must be < 3)
    # This is valid
    found_options.append("E")
solver.pop()

# Determine the result
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")