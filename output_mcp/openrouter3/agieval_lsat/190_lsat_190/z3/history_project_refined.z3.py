from z3 import *

# Create solver
solver = Solver()

# Define students and years
students = ["Louis", "Mollie", "Onyx", "Ryan", "Tiffany", "Yoshio"]
years = [1921, 1922, 1923, 1924]

# Create assignment variables: assign[year] = student
# We'll use an array indexed by year index (0-3 for 1921-1924)
assign = [Int(f"assign_{i}") for i in range(4)]  # 0=1921, 1=1922, 2=1923, 3=1924

# Map student names to integers for easier constraint writing
student_to_int = {name: i for i, name in enumerate(students)}
int_to_student = {i: name for i, name in enumerate(students)}

# Each year gets exactly one student (0-5 range)
for i in range(4):
    solver.add(assign[i] >= 0)
    solver.add(assign[i] <= 5)

# All four years must have different students
solver.add(Distinct(assign))

# Base constraints from problem statement:

# 1. Only Louis or Tiffany can be assigned to 1923 (year index 2)
solver.add(Or(assign[2] == student_to_int["Louis"], assign[2] == student_to_int["Tiffany"]))

# 2. If Mollie is assigned to the project, then she must be assigned to either 1921 or 1922
# This is a conditional: Mollie_in_1921_or_1922 OR Mollie_not_assigned
# We need to check if Mollie is assigned anywhere
mollie_assigned = Or([assign[i] == student_to_int["Mollie"] for i in range(4)])
mollie_in_1921_or_1922 = Or(assign[0] == student_to_int["Mollie"], assign[1] == student_to_int["Mollie"])
solver.add(Implies(mollie_assigned, mollie_in_1921_or_1922))

# 3. If Tiffany is assigned to the project, then Ryan must be assigned to the project
tiffany_assigned = Or([assign[i] == student_to_int["Tiffany"] for i in range(4)])
ryan_assigned = Or([assign[i] == student_to_int["Ryan"] for i in range(4)])
solver.add(Implies(tiffany_assigned, ryan_assigned))

# 4. If Ryan is assigned to the project, then Onyx must be assigned to the year immediately prior to Ryan's
# This means: if Ryan is in year i (i > 0), then Onyx must be in year i-1
# We need to handle all possible positions for Ryan
for i in range(4):
    if i > 0:  # Ryan can't be in 1921 (no prior year)
        solver.add(Implies(assign[i] == student_to_int["Ryan"], 
                          assign[i-1] == student_to_int["Onyx"]))
    else:  # If Ryan is in 1921, the condition is vacuously true (no prior year needed)
        pass

# Now test each answer choice
# Answer choices are in order from earliest year (1921) to latest (1924)
# We need to map each choice to constraints on assign[0], assign[1], assign[2], assign[3]

found_options = []

# Option A: Louis, Onyx, Ryan, Yoshio
opt_a_constr = And(
    assign[0] == student_to_int["Louis"],
    assign[1] == student_to_int["Onyx"],
    assign[2] == student_to_int["Ryan"],
    assign[3] == student_to_int["Yoshio"]
)

# Option B: Mollie, Yoshio, Tiffany, Onyx
opt_b_constr = And(
    assign[0] == student_to_int["Mollie"],
    assign[1] == student_to_int["Yoshio"],
    assign[2] == student_to_int["Tiffany"],
    assign[3] == student_to_int["Onyx"]
)

# Option C: Onyx, Ryan, Louis, Tiffany
opt_c_constr = And(
    assign[0] == student_to_int["Onyx"],
    assign[1] == student_to_int["Ryan"],
    assign[2] == student_to_int["Louis"],
    assign[3] == student_to_int["Tiffany"]
)

# Option D: Tiffany, Onyx, Louis, Ryan
opt_d_constr = And(
    assign[0] == student_to_int["Tiffany"],
    assign[1] == student_to_int["Onyx"],
    assign[2] == student_to_int["Louis"],
    assign[3] == student_to_int["Ryan"]
)

# Option E: Yoshio, Onyx, Louis, Mollie
opt_e_constr = And(
    assign[0] == student_to_int["Yoshio"],
    assign[1] == student_to_int["Onyx"],
    assign[2] == student_to_int["Louis"],
    assign[3] == student_to_int["Mollie"]
)

# Test each option
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), 
                       ("D", opt_d_constr), ("E", opt_e_constr)]:
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