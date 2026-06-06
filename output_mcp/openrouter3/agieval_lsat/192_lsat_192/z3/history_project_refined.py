from z3 import *

# Create solver
solver = Solver()

# Students and years
students = ["Louis", "Mollie", "Onyx", "Ryan", "Tiffany", "Yoshio"]
years = [1921, 1922, 1923, 1924]

# Create assignment variables: assign[student] = year
# Using Int for year values
assign = {s: Int(f"assign_{s}") for s in students}

# Domain constraints: each student assigned to at most one year (or not assigned)
# Since we have 6 students and 4 years, some students won't be assigned
for s in students:
    solver.add(Or([assign[s] == y for y in years] + [assign[s] == 0]))  # 0 means not assigned

# Each year has exactly one student assigned
for y in years:
    solver.add(Or([assign[s] == y for s in students]))

# Ensure each year has exactly one student (no two students assigned to same year)
for y in years:
    solver.add(Sum([If(assign[s] == y, 1, 0) for s in students]) == 1)

# Given condition: Both Ryan and Yoshio are assigned to the project
solver.add(assign["Ryan"] != 0)
solver.add(assign["Yoshio"] != 0)

# Constraint 1: Only Louis or Tiffany can be assigned to 1923
# This means: if someone is assigned to 1923, it must be Louis or Tiffany
# Since each year must have exactly one student, someone must be assigned to 1923
solver.add(Or(assign["Louis"] == 1923, assign["Tiffany"] == 1923))

# Constraint 2: If Mollie is assigned, she must be assigned to 1921 or 1922
solver.add(Implies(assign["Mollie"] != 0, Or(assign["Mollie"] == 1921, assign["Mollie"] == 1922)))

# Constraint 3: If Tiffany is assigned, then Ryan must be assigned
# Note: Ryan is already assigned (given condition), so this is automatically satisfied
# But we should still include it for completeness
solver.add(Implies(assign["Tiffany"] != 0, assign["Ryan"] != 0))

# Constraint 4: If Ryan is assigned, then Onyx must be assigned to the year immediately prior to Ryan's
# This means: if Ryan is assigned to year Y, then Onyx must be assigned to Y-1
# We need to handle the case where Ryan is assigned to 1921 (no prior year)
# If Ryan is in 1921, then the constraint doesn't apply (or Onyx can't be assigned)
# Let's interpret: if Ryan is in 1921, then Onyx doesn't need to be assigned to a prior year
# But the problem says "Onyx must be assigned to the year immediately prior to Ryan's"
# This implies Ryan cannot be in 1921, because there's no prior year
# So we should add: Ryan cannot be assigned to 1921
solver.add(assign["Ryan"] != 1921)

# Now add the constraint for Onyx
solver.add(Implies(assign["Ryan"] != 0, 
                   And(assign["Onyx"] != 0, assign["Onyx"] == assign["Ryan"] - 1)))

# Let's also add that Onyx must be assigned (since Ryan is assigned and constraint requires Onyx)
solver.add(assign["Onyx"] != 0)

# Now test each answer choice using the required skeleton
found_options = []

# Option A: Louis is assigned to 1923
opt_a_constr = (assign["Louis"] == 1923)

# Option B: Mollie is assigned to 1921
opt_b_constr = (assign["Mollie"] == 1921)

# Option C: Onyx is assigned to 1922
opt_c_constr = (assign["Onyx"] == 1922)

# Option D: Tiffany is assigned to 1924
opt_d_constr = (assign["Tiffany"] == 1924)

# Option E: Yoshio is assigned to 1922
opt_e_constr = (assign["Yoshio"] == 1922)

for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), 
                       ("D", opt_d_constr), ("E", opt_e_constr)]:
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