from z3 import *

# Declare symbolic variables for each year's assignment
assignments = [Int(f'assign_{year}') for year in [1921, 1922, 1923, 1924]]

# List of all students
# 0: Louis, 1: Mollie, 2: Onyx, 3: Ryan, 4: Tiffany, 5: Yoshio

# Create a solver
solver = Solver()

# Each assignment is a student index (0-5)
for a in assignments:
    solver.add(a >= 0, a <= 5)

# Each student is assigned to at most one year (implicit in Distinct)
solver.add(Distinct(assignments))

# Constraint 1: Only Louis or Tiffany can be assigned to 1923
solver.add(Or(assignments[2] == 0, assignments[2] == 4))  # 1923 is index 2

# Constraint 2: If Mollie is assigned, she must be assigned to 1921 or 1922
mollie_assigned = Or([assignments[i] == 1 for i in range(4)])
solver.add(Implies(mollie_assigned, Or(assignments[0] == 1, assignments[1] == 1)))

# Constraint 3: If Tiffany is assigned, Ryan must be assigned
tiffany_assigned = Or([assignments[i] == 4 for i in range(4)])
ryan_assigned = Or([assignments[i] == 3 for i in range(4)])
solver.add(Implies(tiffany_assigned, ryan_assigned))

# Constraint 4: If Ryan is assigned, Onyx must be assigned to the year immediately prior to Ryan's
for i in range(1, 4):
    solver.add(Implies(assignments[i] == 3, assignments[i-1] == 2))

# Now, evaluate each option to see if it can be assigned to 1922 (index 1)
found_options = []

# Option A: Louis can be assigned to 1922
solver.push()
solver.add(assignments[1] == 0)  # 1922 is index 1, Louis is 0
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: Mollie can be assigned to 1922
solver.push()
solver.add(assignments[1] == 1)  # 1922 is index 1, Mollie is 1
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: Onyx can be assigned to 1922
solver.push()
solver.add(assignments[1] == 2)  # 1922 is index 1, Onyx is 2
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: Ryan can be assigned to 1922
solver.push()
solver.add(assignments[1] == 3)  # 1922 is index 1, Ryan is 3
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: Yoshio can be assigned to 1922
solver.push()
solver.add(assignments[1] == 5)  # 1922 is index 1, Yoshio is 5
if solver.check() == sat:
    found_options.append("E")
solver.pop()

# Output the result
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")