from z3 import *

# Create solver
solver = Solver()

# Students: Louis, Mollie, Onyx, Ryan, Tiffany, Yoshio
# 0: Louis, 1: Mollie, 2: Onyx, 3: Ryan, 4: Tiffany, 5: Yoshio
students = [0, 1, 2, 3, 4, 5]
student_names = ["Louis", "Mollie", "Onyx", "Ryan", "Tiffany", "Yoshio"]

# Years: 1921, 1922, 1923, 1924
# 0:1921, 1:1922, 2:1923, 3:1924
years = [0, 1, 2, 3]
year_names = ["1921", "1922", "1923", "1924"]

# Variable: assignment[year] = student assigned to that year
assignment = [Int(f"year_{i}") for i in years]

# Domain constraints: each year gets a student from 0-5
for year in years:
    solver.add(assignment[year] >= 0)
    solver.add(assignment[year] <= 5)

# Constraint: Each year gets exactly one student (all different)
solver.add(Distinct(assignment))

# Constraint 1: Only Louis or Tiffany can be assigned to 1923 (year index 2)
# Louis = 0, Tiffany = 4
solver.add(Or(assignment[2] == 0, assignment[2] == 4))

# Constraint 2: If Mollie is assigned to the project, then she must be assigned to either 1921 or 1922
# Mollie = 1
# This means: If Mollie appears in any assignment, it must be in year 0 or 1
for year in years:
    solver.add(Implies(assignment[year] == 1, Or(year == 0, year == 1)))

# Constraint 3: If Tiffany is assigned to the project, then Ryan must be assigned to the project
# Tiffany = 4, Ryan = 3
# If any year has Tiffany (4), then some year must have Ryan (3)
tiffany_assigned = Or([assignment[year] == 4 for year in years])
ryan_assigned = Or([assignment[year] == 3 for year in years])
solver.add(Implies(tiffany_assigned, ryan_assigned))

# Constraint 4: If Ryan is assigned to the project, then Onyx must be assigned to the year immediately prior to Ryan's
# Ryan = 3, Onyx = 2
# If Ryan is in year Y, then Onyx must be in year Y-1
# But if Ryan is in 1921 (year 0), there's no prior year, so this constraint can't be satisfied
# Therefore, Ryan cannot be in 1921
for year in years:
    if year > 0:  # Only for years that have a prior year
        solver.add(Implies(assignment[year] == 3, assignment[year-1] == 2))
    else:
        # If Ryan is in year 0 (1921), then the constraint can't be satisfied
        # So we must ensure Ryan is NOT in year 0
        solver.add(assignment[year] != 3)

# Now test each option for 1922
found_options = []

# Option A: Louis (student 0) in 1922 (year 1)
solver.push()
solver.add(assignment[1] == 0)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: Mollie (student 1) in 1922 (year 1)
solver.push()
solver.add(assignment[1] == 1)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: Onyx (student 2) in 1922 (year 1)
solver.push()
solver.add(assignment[1] == 2)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: Ryan (student 3) in 1922 (year 1)
solver.push()
solver.add(assignment[1] == 3)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: Yoshio (student 5) in 1922 (year 1)
solver.push()
solver.add(assignment[1] == 5)
if solver.check() == sat:
    found_options.append("E")
solver.pop()

print(f"Found options (CAN be assigned to 1922): {found_options}")

# For "CANNOT be assigned", we want the option that is NOT in found_options
all_options = ["A", "B", "C", "D", "E"]
impossible_options = [opt for opt in all_options if opt not in found_options]

print(f"Impossible options (CANNOT be assigned to 1922): {impossible_options}")

if len(impossible_options) == 1:
    print("STATUS: sat")
    print(f"answer:{impossible_options[0]}")
elif len(impossible_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple impossible options found {impossible_options}")
else:
    print("STATUS: unsat")
    print("Refine: No impossible options found")