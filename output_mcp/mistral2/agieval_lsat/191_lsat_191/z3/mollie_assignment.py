from z3 import *

# Declare students and years
students = ['Louis', 'Mollie', 'Onyx', 'Ryan', 'Tiffany', 'Yoshio']
years = [1921, 1922, 1923, 1924]

# Create a solver
solver = Solver()

# Declare symbolic variables for year_to_student as Strings
year_to_student = {y: String(f'year_{y}_student') for y in years}
student_to_year = {s: Int(f'student_{s}_year') for s in students}

# Add constraints: each year is assigned exactly one student
for y in years:
    solver.add(Or([year_to_student[y] == s for s in students]))

# Ensure no two years have the same student (Distinct constraint)
for i in range(len(years)):
    for j in range(i + 1, len(years)):
        solver.add(year_to_student[years[i]] != year_to_student[years[j]])

# Constraint 1: Only Louis or Tiffany can be assigned to 1923
solver.add(Or(year_to_student[1923] == 'Louis', year_to_student[1923] == 'Tiffany'))

# Constraint 2: If Mollie is assigned, she must be assigned to 1921 or 1922
# We will handle this via student_to_year later

# Constraint 3: If Tiffany is assigned, Ryan must also be assigned
# We will handle this via student_to_year later

# Constraint 4: If Ryan is assigned, Onyx must be assigned to the year immediately prior to Ryan's
# We will handle this via student_to_year later

# Helper: Define student_to_year from year_to_student
for s in students:
    solver.add(Or([And(year_to_student[y] == s, student_to_year[s] == y) for y in years]))

# Additional constraints for Mollie, Tiffany, and Ryan
# Constraint 2: If Mollie is assigned, she must be assigned to 1921 or 1922
mollie_year = student_to_year['Mollie']
solver.add(Implies(Or([year_to_student[y] == 'Mollie' for y in years]),
                  Or(mollie_year == 1921, mollie_year == 1922)))

# Constraint 3: If Tiffany is assigned, Ryan must also be assigned
tiffany_assigned = Or([year_to_student[y] == 'Tiffany' for y in years])
ryan_assigned = Or([year_to_student[y] == 'Ryan' for y in years])
solver.add(Implies(tiffany_assigned, ryan_assigned))

# Constraint 4: If Ryan is assigned, Onyx must be assigned to the year immediately prior to Ryan's
for y in years:
    if y - 1 in years:
        solver.add(Implies(year_to_student[y] == 'Ryan',
                          year_to_student[y - 1] == 'Onyx'))

# Now, evaluate each answer choice to see if it forces Mollie to be assigned to 1922.
found_options = []

# Choice A: Louis is assigned to 1924
solver.push()
solver.add(year_to_student[1924] == 'Louis')
if solver.check() == sat:
    m = solver.model()
    mollie_assigned = [m[year_to_student[y]] == 'Mollie' for y in years]
    if any(mollie_assigned):
        mollie_year_val = m[student_to_year['Mollie']]
        if mollie_year_val == 1922:
            found_options.append("A")
solver.pop()

# Choice B: Onyx is assigned to 1921
solver.push()
solver.add(year_to_student[1921] == 'Onyx')
if solver.check() == sat:
    m = solver.model()
    mollie_assigned = [m[year_to_student[y]] == 'Mollie' for y in years]
    if any(mollie_assigned):
        mollie_year_val = m[student_to_year['Mollie']]
        if mollie_year_val == 1922:
            found_options.append("B")
solver.pop()

# Choice C: Onyx is assigned to 1924
solver.push()
solver.add(year_to_student[1924] == 'Onyx')
if solver.check() == sat:
    m = solver.model()
    mollie_assigned = [m[year_to_student[y]] == 'Mollie' for y in years]
    if any(mollie_assigned):
        mollie_year_val = m[student_to_year['Mollie']]
        if mollie_year_val == 1922:
            found_options.append("C")
solver.pop()

# Choice D: Tiffany is assigned to 1923
solver.push()
solver.add(year_to_student[1923] == 'Tiffany')
if solver.check() == sat:
    m = solver.model()
    mollie_assigned = [m[year_to_student[y]] == 'Mollie' for y in years]
    if any(mollie_assigned):
        mollie_year_val = m[student_to_year['Mollie']]
        if mollie_year_val == 1922:
            found_options.append("D")
solver.pop()

# Choice E: Yoshio is assigned to 1921
solver.push()
solver.add(year_to_student[1921] == 'Yoshio')
if solver.check() == sat:
    m = solver.model()
    mollie_assigned = [m[year_to_student[y]] == 'Mollie' for y in years]
    if any(mollie_assigned):
        mollie_year_val = m[student_to_year['Mollie']]
        if mollie_year_val == 1922:
            found_options.append("E")
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