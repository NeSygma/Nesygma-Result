from z3 import *

# Colors
colors = ["forest", "olive", "peach", "turquoise", "white", "yellow"]
color_to_idx = {c: i for i, c in enumerate(colors)}
N_COLORS = 6
N_RUGS = 3

# Variables
# For each color, which rug it's used in (0, 1, 2, or -1 for unused)
color_rug = [Int(f"color_rug_{c}") for c in colors]

# For each rug, how many colors it has
rug_color_count = [Int(f"rug_color_count_{r}") for r in range(N_RUGS)]

# For each rug, whether it's solid (has exactly 1 color)
rug_solid = [Bool(f"rug_solid_{r}") for r in range(N_RUGS)]

solver = Solver()

# Constraint 1: Exactly 5 colors are used (one is unused)
used_colors = [If(color_rug[i] >= 0, 1, 0) for i in range(N_COLORS)]
solver.add(Sum(used_colors) == 5)

# Constraint 2: Each used color is in exactly one rug (0, 1, or 2)
# Each color is either unused (-1) or in exactly one rug
for i in range(N_COLORS):
    solver.add(Or(color_rug[i] == -1, 
                  color_rug[i] == 0, 
                  color_rug[i] == 1, 
                  color_rug[i] == 2))

# Constraint 3: For each rug, count how many colors it has
for r in range(N_RUGS):
    colors_in_rug = [If(color_rug[i] == r, 1, 0) for i in range(N_COLORS)]
    solver.add(rug_color_count[r] == Sum(colors_in_rug))

# Constraint 4: A rug is solid iff it has exactly 1 color
for r in range(N_RUGS):
    solver.add(rug_solid[r] == (rug_color_count[r] == 1))

# Constraint 5: If white is used in a rug, that rug must have exactly 3 colors
white_idx = color_to_idx["white"]
for r in range(N_RUGS):
    # If white is in rug r, then rug r must have exactly 3 colors
    solver.add(Implies(color_rug[white_idx] == r, rug_color_count[r] == 3))

# Constraint 6: If olive is used in a rug, peach must also be used in that rug
olive_idx = color_to_idx["olive"]
peach_idx = color_to_idx["peach"]
for r in range(N_RUGS):
    solver.add(Implies(color_rug[olive_idx] == r, color_rug[peach_idx] == r))

# Constraint 7: Forest and turquoise cannot be together in a rug
forest_idx = color_to_idx["forest"]
turquoise_idx = color_to_idx["turquoise"]
for r in range(N_RUGS):
    solver.add(Not(And(color_rug[forest_idx] == r, color_rug[turquoise_idx] == r)))

# Constraint 8: Peach and turquoise cannot be together in a rug
for r in range(N_RUGS):
    solver.add(Not(And(color_rug[peach_idx] == r, color_rug[turquoise_idx] == r)))

# Constraint 9: Peach and yellow cannot be together in a rug
yellow_idx = color_to_idx["yellow"]
for r in range(N_RUGS):
    solver.add(Not(And(color_rug[peach_idx] == r, color_rug[yellow_idx] == r)))

# Additional condition: One of the rugs is solid peach
# This means peach is used in some rug, and that rug has exactly 1 color (peach)
solver.add(color_rug[peach_idx] >= 0)  # Peach is used
for r in range(N_RUGS):
    solver.add(Implies(color_rug[peach_idx] == r, rug_solid[r]))

# Now evaluate each answer choice
found_options = []

# Option A: One of the rugs is solid forest
opt_a_constr = Or([And(color_rug[forest_idx] == r, rug_solid[r]) for r in range(N_RUGS)])

# Option B: One of the rugs is solid turquoise
opt_b_constr = Or([And(color_rug[turquoise_idx] == r, rug_solid[r]) for r in range(N_RUGS)])

# Option C: One of the rugs is solid yellow
opt_c_constr = Or([And(color_rug[yellow_idx] == r, rug_solid[r]) for r in range(N_RUGS)])

# Option D: Forest and white are used together in a rug
opt_d_constr = Or([And(color_rug[forest_idx] == r, color_rug[white_idx] == r) for r in range(N_RUGS)])

# Option E: White and yellow are used together in a rug
opt_e_constr = Or([And(color_rug[white_idx] == r, color_rug[yellow_idx] == r) for r in range(N_RUGS)])

for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), 
                      ("D", opt_d_constr), ("E", opt_e_constr)]:
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