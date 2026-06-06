from z3 import *

# Variables: positions for each business
pos_O = Int('pos_O')  # optometrist
pos_P = Int('pos_P')  # pharmacy
pos_R1 = Int('pos_R1')  # restaurant 1
pos_R2 = Int('pos_R2')  # restaurant 2
pos_S = Int('pos_S')  # shoe store
pos_T = Int('pos_T')  # toy store
pos_V = Int('pos_V')  # veterinarian

vars_list = [pos_O, pos_P, pos_R1, pos_R2, pos_S, pos_T, pos_V]

# Base domain constraints: each in 1..7
def add_domain(s):
    for v in vars_list:
        s.add(v >= 1, v <= 7)

# All distinct
def add_distinct(s):
    s.add(Distinct(vars_list))

# Base constraints = all original constraints EXCEPT constraint 2
def add_base_constraints(s):
    # Constraint 1: Pharmacy at one end, one restaurant at the other
    s.add(Or(
        And(pos_P == 1, Or(pos_R1 == 7, pos_R2 == 7)),
        And(pos_P == 7, Or(pos_R1 == 1, pos_R2 == 1))
    ))
    # Constraint 3: Pharmacy next to optometrist or veterinarian
    s.add(Or(
        pos_P - pos_O == 1, pos_O - pos_P == 1,
        pos_P - pos_V == 1, pos_V - pos_P == 1
    ))
    # Constraint 4: Toy store not next to veterinarian
    s.add(And(pos_T - pos_V != 1, pos_V - pos_T != 1))

# Constraint 2: Two restaurants separated by at least two other businesses
# |pos_R1 - pos_R2| >= 3
def add_constr_2(s):
    s.add(Or(pos_R1 - pos_R2 >= 3, pos_R2 - pos_R1 >= 3))

# ----- Answer Choices -----
# A: A restaurant must be in either space 3, space 4, or space 5.
def opt_A(s):
    s.add(Or(pos_R1 == 3, pos_R1 == 4, pos_R1 == 5, pos_R2 == 3, pos_R2 == 4, pos_R2 == 5))

# B: A restaurant must be next to either the optometrist or the veterinarian.
def opt_B(s):
    s.add(Or(
        pos_R1 - pos_O == 1, pos_O - pos_R1 == 1,
        pos_R1 - pos_V == 1, pos_V - pos_R1 == 1,
        pos_R2 - pos_O == 1, pos_O - pos_R2 == 1,
        pos_R2 - pos_V == 1, pos_V - pos_R2 == 1
    ))

# C: Either the toy store or the veterinarian must be somewhere between the two restaurants.
def opt_C(s):
    s.add(Or(
        And(pos_R1 < pos_T, pos_T < pos_R2),
        And(pos_R2 < pos_T, pos_T < pos_R1),
        And(pos_R1 < pos_V, pos_V < pos_R2),
        And(pos_R2 < pos_V, pos_V < pos_R1)
    ))

# D: No more than two businesses can separate the pharmacy and the restaurant nearest it.
# i.e., min(|pos_P - pos_R1|, |pos_P - pos_R2|) <= 3
def opt_D(s):
    # At least one restaurant within distance <= 3 (since they can't be same space, distance >= 1)
    s.add(Or(
        And(pos_P - pos_R1 <= 3, pos_R1 - pos_P <= 3),
        And(pos_P - pos_R2 <= 3, pos_R2 - pos_P <= 3)
    ))

# E: The optometrist cannot be next to the shoe store.
def opt_E(s):
    s.add(And(pos_O - pos_S != 1, pos_S - pos_O != 1))

options = [("A", opt_A), ("B", opt_B), ("C", opt_C), ("D", opt_D), ("E", opt_E)]

# First verify that the original constraint set has at least one solution
solver_orig = Solver()
add_domain(solver_orig)
add_distinct(solver_orig)
add_base_constraints(solver_orig)
add_constr_2(solver_orig)

if solver_orig.check() != sat:
    print("STATUS: unsat")
    print("Refine: Original constraints have no solutions")
    exit()

# Now check each option for equivalence
found = []

for letter, constr_func in options:
    # Forward direction: Original (with constraint 2) implies the new constraint
    # Check: (base ∧ constraint_2) ∧ NOT(new_constraint) is unsat?
    fwd = Solver()
    add_domain(fwd)
    add_distinct(fwd)
    add_base_constraints(fwd)
    add_constr_2(fwd)
    # We want to check if adding NOT(new_constraint) leads to unsat
    # Build new constraint as a formula
    # We need to evaluate the constraint without adding it to solver, then negate it.
    # Instead, use push/pop with a fresh solver for negation check.
    
    # Actually, let's do a different approach:
    # Create a solver with base + constr_2, then push, add Not(new_constraint), check.
    # We already have fwd with base + constr_2.
    fwd.push()
    # We need to add the negation of the new constraint.
    # We can create a temporary solver to get the constraint as a formula, but easier:
    # Just add the constraint and check if it's necessary by testing the negation.
    # Let's make a helper: compute the constraint formula by creating a temp solver with the constraint.
    temp_s = Solver()
    add_domain(temp_s)
    add_distinct(temp_s)
    add_base_constraints(temp_s)
    constr_func(temp_s)
    # temp_s has base + new_constraint. But we want the formula for new_constraint alone?
    # Actually we can't extract the formula easily. Let's restructure.
    
    # Better approach: We'll check forward by creating a solver with all original constraints
    # and the negation of the new constraint. If unsat, forward holds.
    fwd_s = Solver()
    add_domain(fwd_s)
    add_distinct(fwd_s)
    add_base_constraints(fwd_s)
    add_constr_2(fwd_s)
    # Now we need to assert NOT(new_constraint). To get the new constraint formula,
    # we can create a small function that returns the constraint formula.
    # Let's refactor options to return formulas instead of adding to solver.
    
    # For now, skip and handle differently.
    pass

# Let me refactor: each option returns a Z3 formula
def opt_A_formula():
    return Or(pos_R1 == 3, pos_R1 == 4, pos_R1 == 5, pos_R2 == 3, pos_R2 == 4, pos_R2 == 5)

def opt_B_formula():
    return Or(
        pos_R1 - pos_O == 1, pos_O - pos_R1 == 1,
        pos_R1 - pos_V == 1, pos_V - pos_R1 == 1,
        pos_R2 - pos_O == 1, pos_O - pos_R2 == 1,
        pos_R2 - pos_V == 1, pos_V - pos_R2 == 1
    )

def opt_C_formula():
    return Or(
        And(pos_R1 < pos_T, pos_T < pos_R2),
        And(pos_R2 < pos_T, pos_T < pos_R1),
        And(pos_R1 < pos_V, pos_V < pos_R2),
        And(pos_R2 < pos_V, pos_V < pos_R1)
    )

def opt_D_formula():
    return Or(
        And(pos_P - pos_R1 <= 3, pos_R1 - pos_P <= 3),
        And(pos_P - pos_R2 <= 3, pos_R2 - pos_P <= 3)
    )

def opt_E_formula():
    return And(pos_O - pos_S != 1, pos_S - pos_O != 1)

options_with_formula = [
    ("A", opt_A_formula),
    ("B", opt_B_formula),
    ("C", opt_C_formula),
    ("D", opt_D_formula),
    ("E", opt_E_formula)
]

# Helper to build solver with base constraints
def base_solver():
    s = Solver()
    add_domain(s)
    add_distinct(s)
    add_base_constraints(s)
    return s

# Constraint 2 formula
constr_2_formula = Or(pos_R1 - pos_R2 >= 3, pos_R2 - pos_R1 >= 3)

found = []

for letter, formula_func in options_with_formula:
    new_constr = formula_func()
    
    # Forward: (base ∧ constr_2) → new_constr
    # Check: base ∧ constr_2 ∧ Not(new_constr) is unsat
    fwd_s = base_solver()
    fwd_s.add(constr_2_formula)
    fwd_s.add(Not(new_constr))
    fwd_res = fwd_s.check()
    
    # Backward: (base ∧ new_constr) → constr_2
    # Check: base ∧ new_constr ∧ Not(constr_2) is unsat
    bwd_s = base_solver()
    bwd_s.add(new_constr)
    bwd_s.add(Not(constr_2_formula))
    bwd_res = bwd_s.check()
    
    if fwd_res == unsat and bwd_res == unsat:
        found.append(letter)
        print(f"Option {letter}: EQUIVALENT (forward unsat={fwd_res}, backward unsat={bwd_res})")
    else:
        print(f"Option {letter}: NOT equivalent (forward={fwd_res}, backward={bwd_res})")

if len(found) == 1:
    print("STATUS: sat")
    print(f"answer:{found[0]}")
elif len(found) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple equivalent options found {found}")
else:
    print("STATUS: unsat")
    print("Refine: No equivalent options found")