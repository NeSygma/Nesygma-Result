from z3 import *

def count_solutions(solver, vars):
    """Count number of unique solutions for the given solver and list of variables."""
    count = 0
    while solver.check() == sat:
        count += 1
        m = solver.model()
        # Block this solution
        solver.add(Or([v != m.eval(v, model_completion=True) for v in vars]))
        if count > 1:
            # Early exit if more than one found
            return count
    return count

# Create base solver
solver = Solver()

# Decision variables: positions of each article
pos_G, pos_H, pos_J = Ints('pos_G pos_H pos_J')
pos_Q, pos_R, pos_S = Ints('pos_Q pos_R pos_S')
pos_Y = Int('pos_Y')

all_vars = [pos_G, pos_H, pos_J, pos_Q, pos_R, pos_S, pos_Y]

# Domain: positions 1 through 7
for v in all_vars:
    solver.add(v >= 1, v <= 7)

# All distinct positions
solver.add(Distinct(all_vars))

# Constraint 1: Consecutive articles cannot have the same topic
# Finance: G, H, J
solver.add(pos_G - pos_H != 1, pos_H - pos_G != 1)
solver.add(pos_G - pos_J != 1, pos_J - pos_G != 1)
solver.add(pos_H - pos_J != 1, pos_J - pos_H != 1)

# Nutrition: Q, R, S
solver.add(pos_Q - pos_R != 1, pos_R - pos_Q != 1)
solver.add(pos_Q - pos_S != 1, pos_S - pos_Q != 1)
solver.add(pos_R - pos_S != 1, pos_S - pos_R != 1)

# Constraint 2: S can be earlier than Q only if Q is third
solver.add(Implies(pos_S < pos_Q, pos_Q == 3))

# Constraint 3: S must be earlier than Y
solver.add(pos_S < pos_Y)

# Constraint 4: J < G < R
solver.add(pos_J < pos_G)
solver.add(pos_G < pos_R)

# Now test each option
options = {
    "A": pos_H == 4,
    "B": pos_H == 6,
    "C": pos_R == 4,
    "D": pos_R == 7,
    "E": pos_Y == 5,
}

found_options = []

for letter, constr in options.items():
    s = Solver()
    # Copy the base context. We can add constraints similarly.
    # Actually, we need to re-add all base constraints.
    # Let's define a function to set up base constraints in a solver.
    # We'll just recreate from scratch inside the loop to avoid side effects.
    pass

# Better design: extract base constraints and add them per option.
base_constraints = [
    # domain
    pos_G >= 1, pos_G <= 7,
    pos_H >= 1, pos_H <= 7,
    pos_J >= 1, pos_J <= 7,
    pos_Q >= 1, pos_Q <= 7,
    pos_R >= 1, pos_R <= 7,
    pos_S >= 1, pos_S <= 7,
    pos_Y >= 1, pos_Y <= 7,
    # distinct
    Distinct(all_vars),
    # consecutive same topic constraints
    pos_G - pos_H != 1, pos_H - pos_G != 1,
    pos_G - pos_J != 1, pos_J - pos_G != 1,
    pos_H - pos_J != 1, pos_J - pos_H != 1,
    pos_Q - pos_R != 1, pos_R - pos_Q != 1,
    pos_Q - pos_S != 1, pos_S - pos_Q != 1,
    pos_R - pos_S != 1, pos_S - pos_R != 1,
    # S before Q only if Q is third
    Implies(pos_S < pos_Q, pos_Q == 3),
    # S before Y
    pos_S < pos_Y,
    # J < G < R
    pos_J < pos_G,
    pos_G < pos_R,
]

for letter, constr in options.items():
    s = Solver()
    s.add(base_constraints)
    s.add(constr)
    
    # Count solutions
    n_sol = count_solutions(s, all_vars)
    if n_sol == 1:
        found_options.append(letter)
    # Note: if n_sol == 0 (unsat), it's not a valid option

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")