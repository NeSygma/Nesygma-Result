from z3 import *

# Declare employees and parking spaces
employees = ["Robertson", "Souza", "Togowa", "Vaughn", "Xu", "Young"]
spaces = [1, 2, 3, 4, 5, 6]

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
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: Togowa is assigned parking space #2
solver.push()
solver.add(assign["Togowa"] == 2)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: Vaughn is assigned parking space #5
solver.push()
solver.add(assign["Vaughn"] == 5)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: Xu is assigned parking space #6
solver.push()
solver.add(assign["Xu"] == 6)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: Young is assigned parking space #2
solver.push()
solver.add(assign["Young"] == 2)
if solver.check() == sat:
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