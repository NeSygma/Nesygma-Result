from z3 import *

# Colors: forest, olive, peach, turquoise, white, yellow
# We'll use indices: 0=forest, 1=olive, 2=peach, 3=turquoise, 4=white, 5=yellow

# For each rug, we need to know which colors it contains
# We'll use a 3x6 matrix: rug_colors[rug][color] = Bool (True if color used in rug)
rug_colors = [[Bool(f"rug_{r}_color_{c}") for c in range(6)] for r in range(3)]

solver = Solver()

# Constraint 1: Exactly 5 colors are used overall (one color not used at all)
# Count how many colors are used across all rugs
color_used = [Or([rug_colors[r][c] for r in range(3)]) for c in range(6)]
solver.add(Sum([If(color_used[c], 1, 0) for c in range(6)]) == 5)

# Constraint 2: Each used color appears in exactly one rug
for c in range(6):
    # Count how many rugs use this color
    count = Sum([If(rug_colors[r][c], 1, 0) for r in range(3)])
    solver.add(Or(count == 0, count == 1))

# Constraint 3: Each rug has at least one color
for r in range(3):
    solver.add(Or([rug_colors[r][c] for c in range(6)]))

# Rule 1: If white (color 4) is used in a rug, that rug must have exactly 3 colors
for r in range(3):
    # If white is used in rug r, then total colors in rug r must be 3
    white_used = rug_colors[r][4]
    total_colors_r = Sum([If(rug_colors[r][c], 1, 0) for c in range(6)])
    solver.add(Implies(white_used, total_colors_r == 3))

# Rule 2: If olive (color 1) is used in a rug, peach (color 2) must also be used in that rug
for r in range(3):
    solver.add(Implies(rug_colors[r][1], rug_colors[r][2]))

# Rule 3: Forest (0) and turquoise (3) cannot be together in any rug
for r in range(3):
    solver.add(Not(And(rug_colors[r][0], rug_colors[r][3])))

# Rule 4: Peach (2) and turquoise (3) cannot be together in any rug
for r in range(3):
    solver.add(Not(And(rug_colors[r][2], rug_colors[r][3])))

# Rule 5: Peach (2) and yellow (5) cannot be together in any rug
for r in range(3):
    solver.add(Not(And(rug_colors[r][2], rug_colors[r][5])))

# Now test each option
# Option A: forest only; turquoise only; olive, peach, and white
# This means:
# Rug 0: forest only (color 0)
# Rug 1: turquoise only (color 3)
# Rug 2: olive (1), peach (2), white (4)

opt_a_constr = And(
    # Rug 0: only forest
    rug_colors[0][0], Not(rug_colors[0][1]), Not(rug_colors[0][2]), Not(rug_colors[0][3]), Not(rug_colors[0][4]), Not(rug_colors[0][5]),
    # Rug 1: only turquoise
    Not(rug_colors[1][0]), Not(rug_colors[1][1]), Not(rug_colors[1][2]), rug_colors[1][3], Not(rug_colors[1][4]), Not(rug_colors[1][5]),
    # Rug 2: olive, peach, white
    Not(rug_colors[2][0]), rug_colors[2][1], rug_colors[2][2], Not(rug_colors[2][3]), rug_colors[2][4], Not(rug_colors[2][5])
)

# Option B: forest only; turquoise only; olive, peach, and yellow
opt_b_constr = And(
    # Rug 0: only forest
    rug_colors[0][0], Not(rug_colors[0][1]), Not(rug_colors[0][2]), Not(rug_colors[0][3]), Not(rug_colors[0][4]), Not(rug_colors[0][5]),
    # Rug 1: only turquoise
    Not(rug_colors[1][0]), Not(rug_colors[1][1]), Not(rug_colors[1][2]), rug_colors[1][3], Not(rug_colors[1][4]), Not(rug_colors[1][5]),
    # Rug 2: olive, peach, yellow
    Not(rug_colors[2][0]), rug_colors[2][1], rug_colors[2][2], Not(rug_colors[2][3]), Not(rug_colors[2][4]), rug_colors[2][5]
)

# Option C: peach only; turquoise only; forest, olive, and white
opt_c_constr = And(
    # Rug 0: only peach
    Not(rug_colors[0][0]), Not(rug_colors[0][1]), rug_colors[0][2], Not(rug_colors[0][3]), Not(rug_colors[0][4]), Not(rug_colors[0][5]),
    # Rug 1: only turquoise
    Not(rug_colors[1][0]), Not(rug_colors[1][1]), Not(rug_colors[1][2]), rug_colors[1][3], Not(rug_colors[1][4]), Not(rug_colors[1][5]),
    # Rug 2: forest, olive, white
    rug_colors[2][0], rug_colors[2][1], Not(rug_colors[2][2]), Not(rug_colors[2][3]), rug_colors[2][4], Not(rug_colors[2][5])
)

# Option D: yellow only; forest and turquoise; olive and peach
opt_d_constr = And(
    # Rug 0: only yellow
    Not(rug_colors[0][0]), Not(rug_colors[0][1]), Not(rug_colors[0][2]), Not(rug_colors[0][3]), Not(rug_colors[0][4]), rug_colors[0][5],
    # Rug 1: forest and turquoise
    rug_colors[1][0], Not(rug_colors[1][1]), Not(rug_colors[1][2]), rug_colors[1][3], Not(rug_colors[1][4]), Not(rug_colors[1][5]),
    # Rug 2: olive and peach
    Not(rug_colors[2][0]), rug_colors[2][1], rug_colors[2][2], Not(rug_colors[2][3]), Not(rug_colors[2][4]), Not(rug_colors[2][5])
)

# Option E: yellow only; olive and peach; turquoise and white
opt_e_constr = And(
    # Rug 0: only yellow
    Not(rug_colors[0][0]), Not(rug_colors[0][1]), Not(rug_colors[0][2]), Not(rug_colors[0][3]), Not(rug_colors[0][4]), rug_colors[0][5],
    # Rug 1: olive and peach
    Not(rug_colors[1][0]), rug_colors[1][1], rug_colors[1][2], Not(rug_colors[1][3]), Not(rug_colors[1][4]), Not(rug_colors[1][5]),
    # Rug 2: turquoise and white
    Not(rug_colors[2][0]), Not(rug_colors[2][1]), Not(rug_colors[2][2]), rug_colors[2][3], rug_colors[2][4], Not(rug_colors[2][5])
)

# Test each option
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