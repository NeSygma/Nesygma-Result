from z3 import *

solver = Solver()

# Student indices
Louis = 0
Mollie = 1
Onyx = 2
Ryan = 3
Tiffany = 4
Yoshio = 5

# Year indices: 1921, 1922, 1923, 1924
year_assign = [Int(f'assign_{year}') for year in [1921, 1922, 1923, 1924]]

# Base constraints
# 1. Each year assigned exactly one student, all distinct
solver.add(Distinct(year_assign))

# 2. Only Louis or Tiffany can be assigned to 1923
solver.add(Or(year_assign[2] == Louis, year_assign[2] == Tiffany))

# 3. If Mollie is assigned, she must be in 1921 or 1922
# Equivalent: Mollie not in 1923 or 1924
solver.add(year_assign[2] != Mollie)
solver.add(year_assign[3] != Mollie)

# 4. If Tiffany is assigned, then Ryan must be assigned
tiffany_assigned = Or([year_assign[i] == Tiffany for i in range(4)])
ryan_assigned = Or([year_assign[i] == Ryan for i in range(4)])
solver.add(Implies(tiffany_assigned, ryan_assigned))

# 5. If Ryan is assigned, then Onyx must be assigned to the year immediately prior
# Ryan cannot be in 1921 (no prior year)
solver.add(year_assign[0] != Ryan)
# For years 1922,1923,1924 (indices 1,2,3)
for i in range(1, 4):
    solver.add(Implies(year_assign[i] == Ryan, year_assign[i-1] == Onyx))

# Now test each option: which student CANNOT be assigned to 1922?
found_options = []
for letter, student in [("A", Louis), ("B", Mollie), ("C", Onyx), ("D", Ryan), ("E", Yoshio)]:
    solver.push()
    # Constraint: this student is assigned to 1922 (index 1)
    solver.add(year_assign[1] == student)
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