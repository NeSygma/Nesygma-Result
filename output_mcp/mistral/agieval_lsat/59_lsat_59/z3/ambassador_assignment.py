from z3 import *

# BENCHMARK_MODE: ON (model-finding mode)
BENCHMARK_MODE = True

# Declare symbolic variables for ambassador assignments
# 0: Jaramillo, 1: Kayne, 2: Landon, 3: Novetzke, 4: Ong
venezuela = Int('venezuela')
yemen = Int('yemen')
zambia = Int('zambia')

# Domain constraints: each ambassador is assigned to at most one country
solver = Solver()
solver.add(venezuela >= 0, venezuela <= 4)
solver.add(yemen >= 0, yemen <= 4)
solver.add(zambia >= 0, zambia <= 4)
solver.add(Distinct(venezuela, yemen, zambia))

# Constraint 1: Either Kayne or Novetzke, but not both, is assigned to one of the ambassadorships
solver.add(Or(
    And(
        Or(venezuela == 1, yemen == 1, zambia == 1),
        And(venezuela != 3, yemen != 3, zambia != 3)
    ),
    And(
        And(venezuela != 1, yemen != 1, zambia != 1),
        Or(venezuela == 3, yemen == 3, zambia == 3)
    )
))

# Constraint 2: If Jaramillo is assigned to one of the ambassadorships, then so is Kayne
# Original constraint: Implies(Or(venezuela == 0, yemen == 0, zambia == 0), Or(venezuela == 1, yemen == 1, zambia == 1))
# We will replace this with each option's constraint in turn

# Constraint 3: If Ong is assigned as ambassador to Venezuela, Kayne is not assigned as ambassador to Yemen
solver.add(Implies(venezuela == 4, yemen != 1))

# Constraint 4: If Landon is assigned to an ambassadorship, it is to Zambia
solver.add(Implies(Or(venezuela == 2, yemen == 2), zambia == 2))

# Helper function to check satisfiability with a given substitution for the original constraint
def check_option(option_constr):
    s = Solver()
    s.add(solver.assertions())  # Add all base constraints
    s.add(option_constr)        # Add the option's constraint
    return s.check()

# Define the options as constraints replacing the original constraint
# Original constraint: If Jaramillo is assigned, then Kayne is assigned
# Equivalent to: Jaramillo is not assigned OR Kayne is assigned
# We will replace this with each option's constraint

# Option A: If Kayne is assigned to an ambassadorship, then so is Jaramillo
# Equivalent to: Kayne is not assigned OR Jaramillo is assigned
opt_a_constr = Implies(
    Or(venezuela == 1, yemen == 1, zambia == 1),
    Or(venezuela == 0, yemen == 0, zambia == 0)
)

# Option B: If Landon and Ong are both assigned to ambassadorships, then so is Novetzke
opt_b_constr = Implies(
    And(
        Or(venezuela == 2, yemen == 2, zambia == 2),
        Or(venezuela == 4, yemen == 4, zambia == 4)
    ),
    Or(venezuela == 3, yemen == 3, zambia == 3)
)

# Option C: If Ong is not assigned to an ambassadorship, then Kayne is assigned to an ambassadorship
opt_c_constr = Implies(
    Not(Or(venezuela == 4, yemen == 4, zambia == 4)),
    Or(venezuela == 1, yemen == 1, zambia == 1)
)

# Option D: Jaramillo and Novetzke are not both assigned to ambassadorships
opt_d_constr = Not(And(
    Or(venezuela == 0, yemen == 0, zambia == 0),
    Or(venezuela == 3, yemen == 3, zambia == 3)
))

# Option E: Novetzke and Ong are not both assigned to ambassadorships
opt_e_constr = Not(And(
    Or(venezuela == 3, yemen == 3, zambia == 3),
    Or(venezuela == 4, yemen == 4, zambia == 4)
))

# Evaluate each option
found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
    if check_option(constr) == sat:
        found_options.append(letter)

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")