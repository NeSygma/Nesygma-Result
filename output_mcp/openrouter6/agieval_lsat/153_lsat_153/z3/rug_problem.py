from z3 import *

# Define colors
colors = ["forest", "olive", "peach", "turquoise", "white", "yellow"]
color_index = {c: i for i, c in enumerate(colors)}
# Variables: color_rug[c] = -1 if unused, else 0,1,2 for rug index
color_rug = [Int(f'rug_{c}') for c in colors]

solver = Solver()

# Domain constraints: each color_rug in {-1,0,1,2}
for cr in color_rug:
    solver.add(Or(cr == -1, cr == 0, cr == 1, cr == 2))

# Exactly five colors used
used_count = Sum([If(cr != -1, 1, 0) for cr in color_rug])
solver.add(used_count == 5)

# Each rug must have at least one color
for r in range(3):
    count_r = Sum([If(cr == r, 1, 0) for cr in color_rug])
    solver.add(count_r >= 1)

# Rule 1: If white is used, its rug has exactly three colors
white_idx = color_index["white"]
for r in range(3):
    # If white is in rug r, then count of colors in rug r is 3
    solver.add(Implies(color_rug[white_idx] == r,
                       Sum([If(cr == r, 1, 0) for cr in color_rug]) == 3))

# Rule 2: If olive is used, peach is in same rug
olive_idx = color_index["olive"]
peach_idx = color_index["peach"]
solver.add(Implies(color_rug[olive_idx] != -1,
                   color_rug[peach_idx] == color_rug[olive_idx]))

# Rule 3: Forest and turquoise not together
forest_idx = color_index["forest"]
turquoise_idx = color_index["turquoise"]
solver.add(Implies(And(color_rug[forest_idx] != -1, color_rug[turquoise_idx] != -1),
                   color_rug[forest_idx] != color_rug[turquoise_idx]))

# Rule 4: Peach and turquoise not together
solver.add(Implies(And(color_rug[peach_idx] != -1, color_rug[turquoise_idx] != -1),
                   color_rug[peach_idx] != color_rug[turquoise_idx]))

# Rule 5: Peach and yellow not together
yellow_idx = color_index["yellow"]
solver.add(Implies(And(color_rug[peach_idx] != -1, color_rug[yellow_idx] != -1),
                   color_rug[peach_idx] != color_rug[yellow_idx]))

# Additional condition: forest and peach are used together in a rug
solver.add(color_rug[forest_idx] != -1)
solver.add(color_rug[peach_idx] != -1)
solver.add(color_rug[forest_idx] == color_rug[peach_idx])

# Now evaluate each answer choice
found_options = []

# Option A: There is exactly one solid rug.
# A solid rug has exactly one color.
# Compute for each rug if it is solid (count == 1)
counts = [Sum([If(color_rug[c] == r, 1, 0) for c in range(6)]) for r in range(3)]
solid_count = Sum([If(counts[r] == 1, 1, 0) for r in range(3)])
opt_a = (solid_count == 1)

# Option B: White is not used in any rug.
opt_b = (color_rug[white_idx] == -1)

# Option C: Yellow is not used in any rug.
opt_c = (color_rug[yellow_idx] == -1)

# Option D: Turquoise and white are used together in a rug.
opt_d = And(color_rug[turquoise_idx] != -1,
            color_rug[white_idx] != -1,
            color_rug[turquoise_idx] == color_rug[white_idx])

# Option E: Turquoise and yellow are used together in a rug.
opt_e = And(color_rug[turquoise_idx] != -1,
            color_rug[yellow_idx] != -1,
            color_rug[turquoise_idx] == color_rug[yellow_idx])

options = [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]

for letter, constr in options:
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