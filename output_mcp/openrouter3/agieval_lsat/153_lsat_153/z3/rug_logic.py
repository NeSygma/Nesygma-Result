from z3 import *

solver = Solver()

# Colors: 0=forest, 1=olive, 2=peach, 3=turquoise, 4=white, 5=yellow
colors = ["forest", "olive", "peach", "turquoise", "white", "yellow"]
num_colors = 6
num_rugs = 3

# Boolean variables: color_in_rug[c][r] = True if color c is in rug r
color_in_rug = [[Bool(f"color_{c}_rug_{r}") for r in range(num_rugs)] for c in range(num_colors)]

# Each color is used in exactly one rug (or not used at all)
for c in range(num_colors):
    solver.add(Or([color_in_rug[c][r] for r in range(num_rugs)] + [Not(Or([color_in_rug[c][r] for r in range(num_rugs)]))]))

# Exactly 5 colors are used (one color not used)
used_colors = [Or([color_in_rug[c][r] for r in range(num_rugs)]) for c in range(num_colors)]
solver.add(Sum([If(used_colors[c], 1, 0) for c in range(num_colors)]) == 5)

# Each rug has at least one color (since we have 3 rugs and 5 colors, some rugs may have multiple)
for r in range(num_rugs):
    solver.add(Or([color_in_rug[c][r] for c in range(num_colors)]))

# Rule 1: If white is used in a rug, that rug must have exactly 3 colors
# We need to count colors per rug
for r in range(num_rugs):
    rug_colors = [If(color_in_rug[c][r], 1, 0) for c in range(num_colors)]
    solver.add(Implies(color_in_rug[4][r], Sum(rug_colors) == 3))

# Rule 2: If olive is used in a rug, peach must also be used in that rug
for r in range(num_rugs):
    solver.add(Implies(color_in_rug[1][r], color_in_rug[2][r]))

# Rule 3: Forest and turquoise cannot be together in a rug
for r in range(num_rugs):
    solver.add(Not(And(color_in_rug[0][r], color_in_rug[3][r])))

# Rule 4: Peach and turquoise cannot be together in a rug
for r in range(num_rugs):
    solver.add(Not(And(color_in_rug[2][r], color_in_rug[3][r])))

# Rule 5: Peach and yellow cannot be together in a rug
for r in range(num_rugs):
    solver.add(Not(And(color_in_rug[2][r], color_in_rug[5][r])))

# Additional constraint: forest and peach are used together in a rug
# Find at least one rug where both forest and peach are present
forest_peach_together = Or([And(color_in_rug[0][r], color_in_rug[2][r]) for r in range(num_rugs)])
solver.add(forest_peach_together)

# Now evaluate each answer choice
# (A) There is exactly one solid rug.
# A solid rug has exactly 1 color
solid_rug_count = Sum([If(Sum([If(color_in_rug[c][r], 1, 0) for c in range(num_colors)]) == 1, 1, 0) for r in range(num_rugs)])
opt_a = (solid_rug_count == 1)

# (B) White is not used in any of the rugs.
opt_b = Not(Or([color_in_rug[4][r] for r in range(num_rugs)]))

# (C) Yellow is not used in any of the rugs.
opt_c = Not(Or([color_in_rug[5][r] for r in range(num_rugs)]))

# (D) Turquoise and white are used together in a rug.
opt_d = Or([And(color_in_rug[3][r], color_in_rug[4][r]) for r in range(num_rugs)])

# (E) Turquoise and yellow are used together in a rug.
opt_e = Or([And(color_in_rug[3][r], color_in_rug[5][r]) for r in range(num_rugs)])

# Evaluate each option
found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
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