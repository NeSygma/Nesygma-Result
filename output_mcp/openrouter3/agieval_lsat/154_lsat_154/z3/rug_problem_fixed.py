from z3 import *

# Colors: forest, olive, peach, turquoise, white, yellow
COLORS = ["forest", "olive", "peach", "turquoise", "white", "yellow"]
COLOR_MAP = {c: i for i, c in enumerate(COLORS)}

# Rugs: 0, 1, 2
RUGS = [0, 1, 2]

# For each color, which rug it's used in (-1 means unused)
color_rug = [Int(f"color_rug_{c}") for c in COLORS]

# For each rug, whether it's solid (single color) or multicolored
rug_solid = [Bool(f"rug_solid_{r}") for r in RUGS]

# For each rug, count of colors used
rug_color_count = [Int(f"rug_color_count_{r}") for r in RUGS]

solver = Solver()

# Constraint: Exactly 5 colors are used (one unused)
used_colors = [If(color_rug[i] == -1, 0, 1) for i in range(6)]
solver.add(Sum(used_colors) == 5)

# Constraint: Each used color appears in exactly one rug
for i in range(6):
    solver.add(Or(color_rug[i] == -1, And(color_rug[i] >= 0, color_rug[i] <= 2)))

# Constraint: One rug is solid yellow
# We'll use a symbolic variable for which rug is solid yellow
solid_yellow_rug = Int("solid_yellow_rug")
solver.add(solid_yellow_rug >= 0, solid_yellow_rug <= 2)

# The yellow color must be in that rug
solver.add(color_rug[COLOR_MAP["yellow"]] == solid_yellow_rug)

# The solid yellow rug must be solid and have exactly 1 color
# Use Or-loop pattern for rug_solid
solver.add(Or([And(solid_yellow_rug == r, rug_solid[r]) for r in RUGS]))
solver.add(Or([And(solid_yellow_rug == r, rug_color_count[r] == 1) for r in RUGS]))

# For other rugs, if solid, count = 1; if multicolored, count >= 2
for r in RUGS:
    # Use Or-loop to handle the condition based on whether this rug is the solid yellow one
    solver.add(Or(
        solid_yellow_rug == r,  # If this is the solid yellow rug, already handled
        And(
            Or(
                And(rug_solid[r], rug_color_count[r] == 1),
                And(Not(rug_solid[r]), rug_color_count[r] >= 2)
            )
        )
    ))

# Count colors per rug
for r in RUGS:
    colors_in_rug = [If(color_rug[i] == r, 1, 0) for i in range(6)]
    solver.add(rug_color_count[r] == Sum(colors_in_rug))

# Rule 1: If white is used in a rug, that rug must have exactly 3 colors
white_rug = color_rug[COLOR_MAP["white"]]
solver.add(Implies(white_rug != -1, rug_color_count[white_rug] == 3))

# Rule 2: If olive is used, peach must also be used in the same rug
olive_rug = color_rug[COLOR_MAP["olive"]]
peach_rug = color_rug[COLOR_MAP["peach"]]
solver.add(Implies(olive_rug != -1, olive_rug == peach_rug))

# Rule 3: Forest and turquoise cannot be together
forest_rug = color_rug[COLOR_MAP["forest"]]
turquoise_rug = color_rug[COLOR_MAP["turquoise"]]
solver.add(Or(forest_rug == -1, turquoise_rug == -1, forest_rug != turquoise_rug))

# Rule 4: Peach and turquoise cannot be together
solver.add(Or(peach_rug == -1, turquoise_rug == -1, peach_rug != turquoise_rug))

# Rule 5: Peach and yellow cannot be together
yellow_rug = color_rug[COLOR_MAP["yellow"]]
solver.add(Or(peach_rug == -1, yellow_rug == -1, peach_rug != yellow_rug))

# Now evaluate each option
# Option A: There is exactly one solid color rug
opt_a = (Sum([If(rug_solid[r], 1, 0) for r in RUGS]) == 1)

# Option B: One of the rugs is solid forest
opt_b = Or([And(rug_solid[r], color_rug[COLOR_MAP["forest"]] == r) for r in RUGS])

# Option C: Turquoise is not used in any of the rugs
opt_c = (turquoise_rug == -1)

# Option D: Forest and olive are used together in a rug
opt_d = Or([And(forest_rug == r, olive_rug == r) for r in RUGS])

# Option E: Peach and white are used together in a rug
opt_e = Or([And(peach_rug == r, white_rug == r) for r in RUGS])

# Test each option
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