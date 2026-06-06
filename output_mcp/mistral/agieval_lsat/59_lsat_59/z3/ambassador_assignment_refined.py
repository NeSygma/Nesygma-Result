from z3 import *

# BENCHMARK_MODE: ON (model-finding mode)
BENCHMARK_MODE = True

# Declare symbolic variables for ambassador assignments
# 0: Jaramillo, 1: Kayne, 2: Landon, 3: Novetzke, 4: Ong
venezuela = Int('venezuela')
yemen = Int('yemen')
zambia = Int('zambia')

# Helper function to get all base constraints
def get_base_constraints():
    constraints = []
    # Domain constraints: each ambassador is assigned to at most one country
    constraints.append(venezuela >= 0)
    constraints.append(venezuela <= 4)
    constraints.append(yemen >= 0)
    constraints.append(yemen <= 4)
    constraints.append(zambia >= 0)
    constraints.append(zambia <= 4)
    constraints.append(Distinct(venezuela, yemen, zambia))

    # Constraint 1: Either Kayne or Novetzke, but not both, is assigned to one of the ambassadorships
    constraints.append(Or(
        And(
            Or(venezuela == 1, yemen == 1, zambia == 1),
            And(venezuela != 3, yemen != 3, zambia != 3)
        ),
        And(
            And(venezuela != 1, yemen != 1, zambia != 1),
            Or(venezuela == 3, yemen == 3, zambia == 3)
        )
    ))

    # Constraint 3: If Ong is assigned as ambassador to Venezuela, Kayne is not assigned as ambassador to Yemen
    constraints.append(Implies(venezuela == 4, yemen != 1))

    # Constraint 4: If Landon is assigned to an ambassadorship, it is to Zambia
    constraints.append(Implies(Or(venezuela == 2, yemen == 2), zambia == 2))

    return constraints

# Original constraint: If Jaramillo is assigned, then Kayne is assigned
original_constraint = Implies(
    Or(venezuela == 0, yemen == 0, zambia == 0),
    Or(venezuela == 1, yemen == 1, zambia == 1)
)

# Define the options as constraints replacing the original constraint
# Option A: If Kayne is assigned, then Jaramillo is assigned
opt_a_constr = Implies(
    Or(venezuela == 1, yemen == 1, zambia == 1),
    Or(venezuela == 0, yemen == 0, zambia == 0)
)

# Option B: If Landon and Ong are both assigned, then Novetzke is assigned
opt_b_constr = Implies(
    And(
        Or(venezuela == 2, yemen == 2, zambia == 2),
        Or(venezuela == 4, yemen == 4, zambia == 4)
    ),
    Or(venezuela == 3, yemen == 3, zambia == 3)
)

# Option C: If Ong is not assigned, then Kayne is assigned
opt_c_constr = Implies(
    Not(Or(venezuela == 4, yemen == 4, zambia == 4)),
    Or(venezuela == 1, yemen == 1, zambia == 1)
)

# Option D: Jaramillo and Novetzke are not both assigned
opt_d_constr = Not(And(
    Or(venezuela == 0, yemen == 0, zambia == 0),
    Or(venezuela == 3, yemen == 3, zambia == 3)
))

# Option E: Novetzke and Ong are not both assigned
opt_e_constr = Not(And(
    Or(venezuela == 3, yemen == 3, zambia == 3),
    Or(venezuela == 4, yemen == 4, zambia == 4)
))

# Function to check if the option's constraint has the same effect as the original constraint
def has_same_effect(option_constr):
    # Solver with original constraint
    s_original = Solver()
    s_original.add(get_base_constraints())
    s_original.add(original_constraint)

    # Solver with option's constraint
    s_option = Solver()
    s_option.add(get_base_constraints())
    s_option.add(option_constr)

    # Check if the two solvers produce the same set of models
    # We do this by checking if the constraints are logically equivalent
    # by ensuring that the addition of the negation of one constraint makes the solver unsat
    # if the original constraint is logically equivalent to the option's constraint
    
    # Check if (original_constraint AND NOT option_constr) is unsat
    s_equiv1 = Solver()
    s_equiv1.add(get_base_constraints())
    s_equiv1.add(original_constraint)
    s_equiv1.add(Not(option_constr))
    equiv1 = (s_equiv1.check() == unsat)

    # Check if (option_constr AND NOT original_constraint) is unsat
    s_equiv2 = Solver()
    s_equiv2.add(get_base_constraints())
    s_equiv2.add(option_constr)
    s_equiv2.add(Not(original_constraint))
    equiv2 = (s_equiv2.check() == unsat)

    return equiv1 and equiv2

# Evaluate each option
found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
    if has_same_effect(constr):
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