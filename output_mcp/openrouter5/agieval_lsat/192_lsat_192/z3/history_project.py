from z3 import *

solver = Solver()

# We have 6 students: Louis, Mollie, Onyx, Ryan, Tiffany, Yoshio
# But only 4 are assigned (one per year: 1921, 1922, 1923, 1924)
# We'll model assignment as: for each student, which year they are assigned (0 = not assigned, 1=1921, 2=1922, 3=1923, 4=1924)
# Or we can model: for each year, which student is assigned.

# Let's use: for each year, a student variable
years = [1921, 1922, 1923, 1924]
# We'll use Int variables for each year, values 0..5 representing students
# 0=Louis, 1=Mollie, 2=Onyx, 3=Ryan, 4=Tiffany, 5=Yoshio
student_names = ["Louis", "Mollie", "Onyx", "Ryan", "Tiffany", "Yoshio"]
# Map names to indices
Louis, Mollie, Onyx, Ryan, Tiffany, Yoshio = 0, 1, 2, 3, 4, 5

# Variables: y1921, y1922, y1923, y1924 are the students assigned to those years
y1921 = Int('y1921')
y1922 = Int('y1922')
y1923 = Int('y1923')
y1924 = Int('y1924')

year_vars = [y1921, y1922, y1923, y1924]

# Each year gets a student index 0..5
for v in year_vars:
    solver.add(v >= 0, v <= 5)

# Each student can be assigned to at most one year (Distinct among assigned years)
solver.add(Distinct(year_vars))

# Exactly 4 students are assigned (all 4 year vars are distinct and valid)
# That's already enforced by Distinct.

# Condition 1: Only Louis or Tiffany can be assigned to 1923.
solver.add(Or(y1923 == Louis, y1923 == Tiffany))

# Condition 2: If Mollie is assigned to the project, then she must be assigned to either 1921 or 1922.
# Mollie is assigned iff Mollie appears in one of the year vars.
mollie_assigned = Or([v == Mollie for v in year_vars])
solver.add(Implies(mollie_assigned, Or(y1921 == Mollie, y1922 == Mollie)))

# Condition 3: If Tiffany is assigned to the project, then Ryan must be assigned to the project.
tiffany_assigned = Or([v == Tiffany for v in year_vars])
ryan_assigned = Or([v == Ryan for v in year_vars])
solver.add(Implies(tiffany_assigned, ryan_assigned))

# Condition 4: If Ryan is assigned to the project, then Onyx must be assigned to the year immediately prior to Ryan's.
# Ryan's year: find which year var equals Ryan
# Onyx must be assigned to the year immediately prior.
# We need: if Ryan is at year Y (1921..1924), then Onyx is at year Y-1.
# But 1921 has no prior year, so Ryan cannot be 1921 if Onyx must be prior.
# Let's encode: For each possible year for Ryan, Onyx is at the prior year.
for i, yr_var in enumerate(year_vars):
    # yr_var is the student assigned to year years[i]
    # If Ryan is at this year, then Onyx must be at the previous year (if one exists)
    if i > 0:
        solver.add(Implies(yr_var == Ryan, year_vars[i-1] == Onyx))
    else:
        # Ryan cannot be at 1921 because no prior year for Onyx
        solver.add(yr_var != Ryan)

# Additional: If Ryan is assigned, Onyx must be assigned too (implied by the prior-year condition)
# But also need: Onyx must be assigned to some year (the prior year). That's covered.

# Given condition: Both Ryan and Yoshio are assigned to the project.
solver.add(ryan_assigned)
yoshio_assigned = Or([v == Yoshio for v in year_vars])
solver.add(yoshio_assigned)

# Now evaluate each option
# (A) Louis is assigned to 1923.
opt_a = (y1923 == Louis)

# (B) Mollie is assigned to 1921.
opt_b = (y1921 == Mollie)

# (C) Onyx is assigned to 1922.
opt_c = (y1922 == Onyx)

# (D) Tiffany is assigned to 1924.
opt_d = (y1924 == Tiffany)

# (E) Yoshio is assigned to 1922.
opt_e = (y1922 == Yoshio)

found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
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