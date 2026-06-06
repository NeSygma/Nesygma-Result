from z3 import *

# Colors as integers for easier handling
forest, olive, peach, turquoise, white, yellow = Ints('forest olive peach turquoise white yellow')

# Rugs: 3 rugs, each represented as a set of colors
rugs = [Array(f'rug_{i}', IntSort(), BoolSort()) for i in range(3)]

# Total distinct colors used across all rugs
total_colors = [Bool(f'total_color_{c}') for c in range(6)]
solver = Solver()

# Exactly 5 distinct colors are used
solver.add(Sum(total_colors) == 5)

# Helper function to check if a color is used in a rug
def color_in_rug(color, rug):
    return Select(rug, color)

# Forest and peach are used together in exactly one rug
solver.add(Sum([If(And(color_in_rug(forest, rugs[i]), color_in_rug(peach, rugs[i])), 1, 0) for i in range(3)]) == 1)

# Constraints on color usage in rugs
for rug in rugs:
    # If white is used, two other colors must also be used
    solver.add(Implies(color_in_rug(white, rug), 
                       Sum([If(color_in_rug(c, rug), 1, 0) for c in range(6)]) >= 3))

    # If olive is used, peach must also be used
    solver.add(Implies(color_in_rug(olive, rug), color_in_rug(peach, rug)))

    # Forest and turquoise cannot be used together
    solver.add(Not(And(color_in_rug(forest, rug), color_in_rug(turquoise, rug))))

    # Peach and turquoise cannot be used together
    solver.add(Not(And(color_in_rug(peach, rug), color_in_rug(turquoise, rug))))

    # Peach and yellow cannot be used together
    solver.add(Not(And(color_in_rug(peach, rug), color_in_rug(yellow, rug))))

# Helper function to check if a rug is solid (exactly one color)
def is_solid(rug):
    return Sum([If(color_in_rug(c, rug), 1, 0) for c in range(6)]) == 1

# Helper function to check if a color is used in any rug
def color_used(color):
    return Or([color_in_rug(color, rug) for rug in rugs])

# Base constraints are now set. Now evaluate the multiple-choice options.

# Option A: There is exactly one solid rug.
opt_a_constr = Sum([If(is_solid(rugs[i]), 1, 0) for i in range(3)]) == 1

# Option B: White is not used in any of the rugs.
opt_b_constr = Not(color_used(white))

# Option C: Yellow is not used in any of the rugs.
opt_c_constr = Not(color_used(yellow))

# Option D: Turquoise and white are used together in a rug.
opt_d_constr = Or([
    And(color_in_rug(turquoise, rugs[i]), color_in_rug(white, rugs[i])) for i in range(3)
])

# Option E: Turquoise and yellow are used together in a rug.
opt_e_constr = Or([
    And(color_in_rug(turquoise, rugs[i]), color_in_rug(yellow, rugs[i])) for i in range(3)
])

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