from z3 import *

solver = Solver()

# Declare students as Int constants for easier handling
louis = 0
mollie = 1
onxy = 2
ryan = 3
tiffany = 4
yoshio = 5

# Declare years as Int constants
year_1921 = 0
year_1922 = 1
year_1923 = 2
year_1924 = 3

# Assignment variables: assignment[year] = student
assignment = [Int(f"assignment_{year}") for year in range(4)]

# Each year is assigned exactly one student
for year in range(4):
    solver.add(assignment[year] >= 0, assignment[year] <= 5)

# Each student is assigned to at most one year
for student in range(6):
    solver.add(AtMost(*[assignment[year] == student for year in range(4)], 1))

# Exactly four students are assigned to the project
assigned_students = [Bool(f"assigned_{student}") for student in range(6)]
for student in range(6):
    solver.add(assigned_students[student] == Or([assignment[year] == student for year in range(4)]))
solver.add(Sum(assigned_students) == 4)

# Only Louis or Tiffany can be assigned to 1923 (year_1923)
solver.add(Or(assignment[year_1923] == louis, assignment[year_1923] == tiffany))

# If Mollie is assigned to the project, then she must be assigned to either 1921 or 1922
solver.add(Implies(
    assigned_students[mollie],
    Or(assignment[year_1921] == mollie, assignment[year_1922] == mollie)
))

# If Tiffany is assigned to the project, then Ryan must be assigned to the project
solver.add(Implies(
    assigned_students[tiffany],
    assigned_students[ryan]
))

# If Ryan is assigned to the project, then Onyx must be assigned to the year immediately prior to Ryan's
# This means if Ryan is assigned to year Y, Onyx must be assigned to year Y-1
for year in range(1, 4):
    solver.add(Implies(
        assignment[year] == ryan,
        assignment[year-1] == onxy
    ))

# Both Ryan and Yoshio are assigned to the project
solver.add(assigned_students[ryan])
solver.add(assigned_students[yoshio])

# Define the options as constraints
# Option A: Louis is assigned to 1923 (year_1923)
opt_a_constr = (assignment[year_1923] == louis)

# Option B: Mollie is assigned to 1921 (year_1921)
opt_b_constr = (assignment[year_1921] == mollie)

# Option C: Onyx is assigned to 1922 (year_1922)
opt_c_constr = (assignment[year_1922] == onxy)

# Option D: Tiffany is assigned to 1924 (year_1924)
opt_d_constr = (assignment[year_1924] == tiffany)

# Option E: Yoshio is assigned to 1922 (year_1922)
opt_e_constr = (assignment[year_1922] == yoshio)

# Test each option
found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
    solver.pop()

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")