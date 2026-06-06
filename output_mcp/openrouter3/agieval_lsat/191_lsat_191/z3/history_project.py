from z3 import *

# Student IDs
LOUIS, MOLLIE, ONYX, RYAN, TIFFANY, YOSHIO = 0, 1, 2, 3, 4, 5
STUDENTS = [LOUIS, MOLLIE, ONYX, RYAN, TIFFANY, YOSHIO]
STUDENT_NAMES = ["Louis", "Mollie", "Onyx", "Ryan", "Tiffany", "Yoshio"]

# Year indices (0=1921, 1=1922, 2=1923, 3=1924)
YEAR_1921, YEAR_1922, YEAR_1923, YEAR_1924 = 0, 1, 2, 3
YEARS = [YEAR_1921, YEAR_1922, YEAR_1923, YEAR_1924]
YEAR_NAMES = ["1921", "1922", "1923", "1924"]

# Create solver
solver = Solver()

# Variable: assignment[year] = student assigned to that year
assignment = [Int(f"assign_{year}") for year in YEARS]

# Domain constraints: each assignment must be one of the 6 students
for year in YEARS:
    solver.add(Or([assignment[year] == s for s in STUDENTS]))

# Constraint: Each year has exactly one student (already enforced by assignment array)
# Constraint: Each student can be assigned to at most one year (all-different)
solver.add(Distinct(assignment))

# Constraint 1: Only Louis or Tiffany can be assigned to 1923
solver.add(Or(assignment[YEAR_1923] == LOUIS, assignment[YEAR_1923] == TIFFANY))

# Constraint 2: If Mollie is assigned to the project, then she must be assigned to either 1921 or 1922
# This means: if Mollie appears in any assignment, it must be to 1921 or 1922
# We can express this as: for all years, if assignment[year] == MOLLIE, then year must be 1921 or 1922
for year in YEARS:
    solver.add(Implies(assignment[year] == MOLLIE, Or(year == YEAR_1921, year == YEAR_1922)))

# Constraint 3: If Tiffany is assigned to the project, then Ryan must be assigned to the project
# This means: if Tiffany appears in any assignment, then Ryan must appear in some assignment
tiffany_assigned = Or([assignment[year] == TIFFANY for year in YEARS])
ryan_assigned = Or([assignment[year] == RYAN for year in YEARS])
solver.add(Implies(tiffany_assigned, ryan_assigned))

# Constraint 4: If Ryan is assigned to the project, then Onyx must be assigned to the year immediately prior to Ryan's
# This means: if Ryan is assigned to year Y, then Onyx must be assigned to year Y-1
for year in YEARS:
    if year > 0:  # For years 1922, 1923, 1924 (indices 1,2,3)
        solver.add(Implies(assignment[year] == RYAN, assignment[year-1] == ONYX))
    # For year 1921 (index 0), Ryan cannot be assigned because there's no prior year
    solver.add(Not(assignment[YEAR_1921] == RYAN))

# Base constraints are now added

# Now evaluate each answer choice
# The question: "Mollie must be assigned to 1922 if which one of the following is true?"
# We need to find which condition forces Mollie to be in 1922

# For each option, we add the option's condition and check if it forces Mollie to 1922
# Actually, we need to check: if the option is true, does it imply Mollie must be in 1922?
# This is equivalent to: adding the option condition, and checking if Mollie NOT in 1922 leads to unsat

# Let's define the options:
# (A) Louis is assigned to 1924
# (B) Onyx is assigned to 1921
# (C) Onyx is assigned to 1924
# (D) Tiffany is assigned to 1923
# (E) Yoshio is assigned to 1921

# For each option, we'll check: if the option is true, does it force Mollie to be in 1922?
# We'll do this by checking if adding the option AND Mollie NOT in 1922 leads to unsat

found_options = []

# Option A: Louis is assigned to 1924
solver.push()
solver.add(assignment[YEAR_1924] == LOUIS)
# Check if Mollie must be in 1922: try to find a model where Mollie is NOT in 1922
solver.push()
solver.add(Not(assignment[YEAR_1922] == MOLLIE))
if solver.check() == unsat:
    # If unsat, then Mollie MUST be in 1922 when Louis is in 1924
    found_options.append("A")
solver.pop()
solver.pop()

# Option B: Onyx is assigned to 1921
solver.push()
solver.add(assignment[YEAR_1921] == ONYX)
solver.push()
solver.add(Not(assignment[YEAR_1922] == MOLLIE))
if solver.check() == unsat:
    found_options.append("B")
solver.pop()
solver.pop()

# Option C: Onyx is assigned to 1924
solver.push()
solver.add(assignment[YEAR_1924] == ONYX)
solver.push()
solver.add(Not(assignment[YEAR_1922] == MOLLIE))
if solver.check() == unsat:
    found_options.append("C")
solver.pop()
solver.pop()

# Option D: Tiffany is assigned to 1923
solver.push()
solver.add(assignment[YEAR_1923] == TIFFANY)
solver.push()
solver.add(Not(assignment[YEAR_1922] == MOLLIE))
if solver.check() == unsat:
    found_options.append("D")
solver.pop()
solver.pop()

# Option E: Yoshio is assigned to 1921
solver.push()
solver.add(assignment[YEAR_1921] == YOSHIO)
solver.push()
solver.add(Not(assignment[YEAR_1922] == MOLLIE))
if solver.check() == unsat:
    found_options.append("E")
solver.pop()
solver.pop()

# Print results
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")