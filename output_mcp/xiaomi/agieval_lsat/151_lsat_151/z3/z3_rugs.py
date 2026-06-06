from z3 import *

solver = Solver()

# Colors: forest=0, olive=1, peach=2, turquoise=3, white=4, yellow=5
colors = ['forest', 'olive', 'peach', 'turquoise', 'white', 'yellow']
n_colors = 6
n_rugs = 3

# rug_color[r][c] = True if color c is used in rug r
rug_color = [[Bool(f"rug{r}_{colors[c]}") for c in range(n_colors)] for r in range(n_rugs)]

# Exactly 5 of the 6 colors are used (across all rugs)
# Each color used appears in exactly one rug
for c in range(n_colors):
    # Each color is used in at most one rug
    for r1 in range(n_rugs):
        for r2 in range(r1+1, n_rugs):
            solver.add(Not(And(rug_color[r1][c], rug_color[r2][c])))

# Exactly 5 colors are used
solver.add(Sum([If(Or([rug_color[r][c] for r in range(n_rugs)]), 1, 0) for c in range(n_colors)]) == 5)

# Each color used is used in exactly one rug (already enforced above)
# A rug is solid if exactly one color, multicolored if 2+ colors
# rug_size[r] = number of colors in rug r
rug_size = [Int(f"rug_size_{r}") for r in range(n_rugs)]
for r in range(n_rugs):
    solver.add(rug_size[r] == Sum([If(rug_color[r][c], 1, 0) for c in range(n_colors)]))
    # Each rug must have at least 1 color
    solver.add(rug_size[r] >= 1)

# Rule 1: In any rug in which white is used, two other colors are also used (so 3 total)
for r in range(n_rugs):
    solver.add(Implies(rug_color[r][4], rug_size[r] >= 3))

# Rule 2: In any rug in which olive is used, peach is also used
for r in range(n_rugs):
    solver.add(Implies(rug_color[r][1], rug_color[r][2]))

# Rule 3: Forest and turquoise are not used together in a rug
for r in range(n_rugs):
    solver.add(Not(And(rug_color[r][0], rug_color[r][3])))

# Rule 4: Peach and turquoise are not used together in a rug
for r in range(n_rugs):
    solver.add(Not(And(rug_color[r][2], rug_color[r][3])))

# Rule 5: Peach and yellow are not used together in a rug
for r in range(n_rugs):
    solver.add(Not(And(rug_color[r][2], rug_color[r][5])))

# CONSTRAINT: One of the rugs is solid peach
# This means one rug has exactly peach and nothing else
solver.add(Or([
    And(rug_color[r][2], rug_size[r] == 1) for r in range(n_rugs)
]))

# Define the answer options
# (A) One of the rugs is solid forest
opt_a = Or([And(rug_color[r][0], rug_size[r] == 1) for r in range(n_rugs)])

# (B) One of the rugs is solid turquoise
opt_b = Or([And(rug_color[r][3], rug_size[r] == 1) for r in range(n_rugs)])

# (C) One of the rugs is solid yellow
opt_c = Or([And(rug_color[r][5], rug_size[r] == 1) for r in range(n_rugs)])

# (D) Forest and white are used together in a rug
opt_d = Or([And(rug_color[r][0], rug_color[r][4]) for r in range(n_rugs)])

# (E) White and yellow are used together in a rug
opt_e = Or([And(rug_color[r][4], rug_color[r][5]) for r in range(n_rugs)])

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