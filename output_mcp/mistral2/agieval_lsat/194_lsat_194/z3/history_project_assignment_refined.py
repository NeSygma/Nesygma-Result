from z3 import *

# BENCHMARK_MODE: ON (model-finding mode)
BENCHMARK_MODE = True

# Create a solver
solver = Solver()

# Encode students as integers for simplicity
Louis = 0
Mollie = 1
Onyx = 2
Ryan = 3
Tiffany = 4
Yoshio = 5

# Encode years as integers for simplicity
Y1921 = 0
Y1922 = 1
Y1923 = 2
Y1924 = 3

# Assignment function: year -> student
assignment = Function('assignment', IntSort(), IntSort())

# Each year must be assigned exactly one student
solver.add(assignment(Y1921) != assignment(Y1922))
solver.add(assignment(Y1921) != assignment(Y1923))
solver.add(assignment(Y1921) != assignment(Y1924))
solver.add(assignment(Y1922) != assignment(Y1923))
solver.add(assignment(Y1922) != assignment(Y1924))
solver.add(assignment(Y1923) != assignment(Y1924))

# Only Louis or Tiffany can be assigned to 1923
solver.add(Or(assignment(Y1923) == Louis, assignment(Y1923) == Tiffany))

# If Mollie is assigned, she must be assigned to 1921 or 1922
solver.add(Implies(
    Or(
        assignment(Y1921) == Mollie,
        assignment(Y1922) == Mollie,
        assignment(Y1923) == Mollie,
        assignment(Y1924) == Mollie
    ),
    Or(assignment(Y1921) == Mollie, assignment(Y1922) == Mollie)
))

# If Tiffany is assigned, Ryan must be assigned
solver.add(Implies(
    Or(
        assignment(Y1921) == Tiffany,
        assignment(Y1922) == Tiffany,
        assignment(Y1923) == Tiffany,
        assignment(Y1924) == Tiffany
    ),
    Or(
        assignment(Y1921) == Ryan,
        assignment(Y1922) == Ryan,
        assignment(Y1923) == Ryan,
        assignment(Y1924) == Ryan
    )
))

# If Ryan is assigned, Onyx must be assigned to the year immediately prior to Ryan's year
# For Ryan in 1922, Onyx must be in 1921
# For Ryan in 1923, Onyx must be in 1922
# For Ryan in 1924, Onyx must be in 1923
solver.add(Implies(
    assignment(Y1922) == Ryan,
    assignment(Y1921) == Onyx
))
solver.add(Implies(
    assignment(Y1923) == Ryan,
    assignment(Y1922) == Onyx
))
solver.add(Implies(
    assignment(Y1924) == Ryan,
    assignment(Y1923) == Onyx
))

# Yoshio is not assigned to the project
solver.add(And(
    assignment(Y1921) != Yoshio,
    assignment(Y1922) != Yoshio,
    assignment(Y1923) != Yoshio,
    assignment(Y1924) != Yoshio
))

# Define the options as constraints
# (A) Louis is not assigned to the project
opt_a_constr = And(
    assignment(Y1921) != Louis,
    assignment(Y1922) != Louis,
    assignment(Y1923) != Louis,
    assignment(Y1924) != Louis
)

# (B) Ryan is not assigned to the project
opt_b_constr = And(
    assignment(Y1921) != Ryan,
    assignment(Y1922) != Ryan,
    assignment(Y1923) != Ryan,
    assignment(Y1924) != Ryan
)

# (C) Tiffany is not assigned to the project
opt_c_constr = And(
    assignment(Y1921) != Tiffany,
    assignment(Y1922) != Tiffany,
    assignment(Y1923) != Tiffany,
    assignment(Y1924) != Tiffany
)

# (D) Onyx is assigned to 1922
opt_d_constr = assignment(Y1922) == Onyx

# (E) Louis is assigned to 1924
opt_e_constr = assignment(Y1924) == Louis

# Evaluate each option
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