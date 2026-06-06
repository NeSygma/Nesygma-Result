from z3 import *

# Create solver
solver = Solver()

# Define students and years
students = ["Louis", "Mollie", "Onyx", "Ryan", "Tiffany", "Yoshio"]
years = [1921, 1922, 1923, 1924]

# Create assignment variables: assign[student] = year
# We'll use a dictionary mapping student names to Z3 variables
assign = {}
for student in students:
    assign[student] = Int(f"assign_{student}")

# Each student can be assigned to a year (1921-1924) or not assigned (0)
# We'll use 0 to represent "not assigned"
for student in students:
    solver.add(Or([assign[student] == year for year in years] + [assign[student] == 0]))

# Each year must have exactly one student assigned
for year in years:
    # Count how many students are assigned to this year
    count = Sum([If(assign[student] == year, 1, 0) for student in students])
    solver.add(count == 1)

# Yoshio is NOT assigned to the project
solver.add(assign["Yoshio"] == 0)

# Condition 1: Only Louis or Tiffany can be assigned to 1923
# This means: if someone is assigned to 1923, it must be Louis or Tiffany
# We need to ensure that if 1923 is assigned, it's to Louis or Tiffany
# Also, Louis and Tiffany cannot both be assigned to 1923 (only one per year)
solver.add(Or(
    assign["Louis"] != 1923,
    assign["Tiffany"] != 1923
))
# Additionally, if 1923 is assigned, it must be to Louis or Tiffany
# We'll enforce this by saying: if any student other than Louis/Tiffany is assigned to 1923, it's invalid
for student in students:
    if student not in ["Louis", "Tiffany"]:
        solver.add(assign[student] != 1923)

# Condition 2: If Mollie is assigned, she must be in 1921 or 1922
solver.add(Implies(assign["Mollie"] != 0, Or(assign["Mollie"] == 1921, assign["Mollie"] == 1922)))

# Condition 3: If Tiffany is assigned, Ryan must be assigned
solver.add(Implies(assign["Tiffany"] != 0, assign["Ryan"] != 0))

# Condition 4: If Ryan is assigned, Onyx must be assigned to the year immediately prior to Ryan's
# This means: if Ryan is in year Y, then Onyx must be in year Y-1
for year in years:
    if year > 1921:  # Only years that have a prior year
        solver.add(Implies(assign["Ryan"] == year, assign["Onyx"] == year - 1))
    else:
        # If Ryan is in 1921, there's no prior year, so this condition can't be satisfied
        # But the condition only applies if Ryan is assigned, so we need to handle this
        # Actually, if Ryan is in 1921, then Onyx would need to be in 1920, which doesn't exist
        # So Ryan cannot be in 1921 if he's assigned
        solver.add(Implies(assign["Ryan"] == 1921, False))  # This makes Ryan in 1921 impossible

# Additional constraint: Each student can be assigned to at most one year (already enforced by assignment variable)

# Now define the answer choices as constraints
# The question asks: "If Yoshio is not assigned to the project, which one of the following could be true?"
# We already have Yoshio not assigned, so we just need to check which option could be true

# Option A: Louis is not assigned to the project
opt_a = (assign["Louis"] == 0)

# Option B: Ryan is not assigned to the project
opt_b = (assign["Ryan"] == 0)

# Option C: Tiffany is not assigned to the project
opt_c = (assign["Tiffany"] == 0)

# Option D: Onyx is assigned to 1922
opt_d = (assign["Onyx"] == 1922)

# Option E: Louis is assigned to 1924
opt_e = (assign["Louis"] == 1924)

# Test each option
found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
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