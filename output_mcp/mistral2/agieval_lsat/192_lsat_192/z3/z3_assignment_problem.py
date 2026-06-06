from z3 import *

solver = Solver()

# Declare symbolic variables for assignments
# Each year is assigned exactly one student
# We represent the assignment as a function from years to students
# Years: 1921, 1922, 1923, 1924
# Students: Louis, Mollie, Onyx, Ryan, Tiffany, Yoshio

# We'll use IntSort for years and StringSort (or Int) for students
Year = IntSort()
Student = StringSort()

# Create student constants
louis = String("Louis")
mollie = String("Mollie")
onxy = String("Onyx")
ryan = String("Ryan")
tiffany = String("Tiffany")
yoshio = String("Yoshio")

# Create year constants
year_1921 = Int(1921)
year_1922 = Int(1922)
year_1923 = Int(1923)
year_1924 = Int(1924)

# Assignment function: year -> student
assignment = Function("assignment", Year, Student)

# Each year is assigned exactly one student
solver.add(assignment(year_1921) == louis)  # Placeholder, will be refined
solver.add(assignment(year_1922) == louis)  # Placeholder, will be refined
solver.add(assignment(year_1923) == louis)  # Placeholder, will be refined
solver.add(assignment(year_1924) == louis)  # Placeholder, will be refined

# Only Louis or Tiffany can be assigned to 1923
solver.add(Or(assignment(year_1923) == louis, assignment(year_1923) == tiffany))

# If Mollie is assigned to the project, then she must be assigned to either 1921 or 1922
# We need to ensure Mollie is assigned to exactly one year if she is in the project
# We'll handle this later with constraints

# If Tiffany is assigned to the project, then Ryan must be assigned to the project
# We'll handle this later with constraints

# If Ryan is assigned to the project, then Onyx must be assigned to the year immediately prior to Ryan's
# This means if Ryan is assigned to year Y, Onyx must be assigned to year Y-1
# We'll handle this later with constraints

# Base constraint: Both Ryan and Yoshio are assigned to the project
# This means Ryan and Yoshio must each be assigned to exactly one year
# We'll enforce this by ensuring their assignments are distinct and cover two years

# We need to ensure that each student is assigned to at most one year
# We'll use a list of all possible assignments and enforce uniqueness

# Let's define the possible assignments for each year
# We'll use a list of all possible assignments and enforce that each year has exactly one student
# and each student is assigned to at most one year

# We'll use a list of all students and years
students = [louis, mollie, onxy, ryan, tiffany, yoshio]
years = [year_1921, year_1922, year_1923, year_1924]

# Each year is assigned exactly one student
for y in years:
    solver.add(Or([assignment(y) == s for s in students]))

# Each student is assigned to at most one year
for s in students:
    solver.add(AtMost(*[assignment(y) == s for y in years], 1))

# Both Ryan and Yoshio are assigned to the project
# This means Ryan and Yoshio must each be assigned to exactly one year
# We'll enforce this by ensuring their assignments are distinct and cover two years
solver.add(Or([assignment(y) == ryan for y in years]))
solver.add(Or([assignment(y) == yoshio for y in years]))

# If Tiffany is assigned to the project, then Ryan must be assigned to the project
# We'll enforce this by ensuring that if Tiffany is assigned to any year, Ryan is also assigned
solver.add(Implies(Or([assignment(y) == tiffany for y in years]), Or([assignment(y) == ryan for y in years])))

# If Ryan is assigned to the project, then Onyx must be assigned to the year immediately prior to Ryan's
# This means if Ryan is assigned to year Y, Onyx must be assigned to year Y-1
# We'll enforce this by checking all possible years for Ryan and ensuring Onyx is assigned to Y-1
for y in years:
    solver.add(Implies(assignment(y) == ryan, 
                       Or([
                           And(y == year_1922, assignment(year_1921) == onxy),
                           And(y == year_1923, assignment(year_1922) == onxy),
                           And(y == year_1924, assignment(year_1923) == onxy)
                       ])))

# If Mollie is assigned to the project, then she must be assigned to either 1921 or 1922
solver.add(Implies(Or([assignment(y) == mollie for y in years]),
                   Or(assignment(year_1921) == mollie, assignment(year_1922) == mollie)))

# Now, we need to evaluate the multiple choice options under the condition that both Ryan and Yoshio are assigned
# We'll test each option to see if it can be true

# Define the options as constraints
# Option A: Louis is assigned to 1923
opt_a_constr = (assignment(year_1923) == louis)

# Option B: Mollie is assigned to 1921
opt_b_constr = (assignment(year_1921) == mollie)

# Option C: Onyx is assigned to 1922
opt_c_constr = (assignment(year_1922) == onxy)

# Option D: Tiffany is assigned to 1924
opt_d_constr = (assignment(year_1924) == tiffany)

# Option E: Yoshio is assigned to 1922
opt_e_constr = (assignment(year_1922) == yoshio)

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