from z3 import *

# We have 3 rugs (rug 0, rug 1, rug 2)
# 6 colors: forest, olive, peach, turquoise, white, yellow
# Exactly 5 of the 6 colors are used. Each used color appears in exactly one rug.
# Rugs are either solid (one color) or multicolored (multiple colors).
# Given: one rug is solid peach.

# Let's model which colors are used in which rug.
# We'll use boolean variables: color_in_rug[c][r] = True if color c is used in rug r.

colors = ["forest", "olive", "peach", "turquoise", "white", "yellow"]
# Map color names to indices
c_idx = {c: i for i, c in enumerate(colors)}

# Variables: color_in_rug[c][r] for color c (0..5) and rug r (0..2)
color_in_rug = [[Bool(f"{c}_in_rug_{r}") for r in range(3)] for c in range(6)]

solver = Solver()

# Each color that is used is used in exactly one rug.
# Exactly 5 of the 6 colors are used. So one color is unused.
# For each color, it's either unused (not in any rug) or used in exactly one rug.
for c in range(6):
    # color c is used in at most one rug
    solver.add(AtMost(*[color_in_rug[c][r] for r in range(3)], 1))
    # color c is used in at least one rug OR it's the unused color
    # We'll handle the "exactly 5 used" constraint separately.

# Exactly 5 colors are used. So exactly one color is unused (not in any rug).
# Count how many colors are used (appear in at least one rug).
used_colors = [Or([color_in_rug[c][r] for r in range(3)]) for c in range(6)]
solver.add(PbEq([(used_colors[c], 1) for c in range(6)], 5))

# Each rug must have at least one color (since it's woven from colored thread)
for r in range(3):
    solver.add(Or([color_in_rug[c][r] for c in range(6)]))

# Rule: In any rug in which white is used, two other colors are also used.
# So if white is in rug r, then exactly 3 colors total in that rug (white + 2 others).
for r in range(3):
    # Count colors in rug r
    colors_in_rug_r = [color_in_rug[c][r] for c in range(6)]
    # If white is in rug r, then sum of colors in rug r = 3
    solver.add(Implies(color_in_rug[c_idx["white"]][r], 
                       PbEq([(color_in_rug[c][r], 1) for c in range(6)], 3)))

# Rule: In any rug in which olive is used, peach is also used.
for r in range(3):
    solver.add(Implies(color_in_rug[c_idx["olive"]][r], 
                       color_in_rug[c_idx["peach"]][r]))

# Rule: Forest and turquoise are not used together in a rug.
for r in range(3):
    solver.add(Not(And(color_in_rug[c_idx["forest"]][r], 
                       color_in_rug[c_idx["turquoise"]][r])))

# Rule: Peach and turquoise are not used together in a rug.
for r in range(3):
    solver.add(Not(And(color_in_rug[c_idx["peach"]][r], 
                       color_in_rug[c_idx["turquoise"]][r])))

# Rule: Peach and yellow are not used together in a rug.
for r in range(3):
    solver.add(Not(And(color_in_rug[c_idx["peach"]][r], 
                       color_in_rug[c_idx["yellow"]][r])))

# Given: One of the rugs is solid peach.
# Solid means exactly one color in that rug.
# So there exists a rug r such that peach is in rug r and no other colors are in rug r.
solid_peach_rug = False
for r in range(3):
    # Rug r is solid peach: peach is in rug r, and no other color is in rug r
    other_colors_in_r = [color_in_rug[c][r] for c in range(6) if c != c_idx["peach"]]
    solver.add(Or(
        # Either this rug is not the solid peach rug, or it is
        Not(And(color_in_rug[c_idx["peach"]][r], 
                And([Not(oc) for oc in other_colors_in_r])))
    ))

# Actually, we need exactly one rug to be solid peach.
# Let's create a variable for "rug r is solid peach"
solid_peach = [Bool(f"solid_peach_{r}") for r in range(3)]
for r in range(3):
    other_colors_in_r = [color_in_rug[c][r] for c in range(6) if c != c_idx["peach"]]
    solver.add(solid_peach[r] == And(color_in_rug[c_idx["peach"]][r], 
                                     And([Not(oc) for oc in other_colors_in_r])))

# Exactly one rug is solid peach
solver.add(PbEq([(solid_peach[r], 1) for r in range(3)], 1))

# Now evaluate each option
# Option A: One of the rugs is solid forest.
opt_a = Or([And(color_in_rug[c_idx["forest"]][r], 
                And([Not(color_in_rug[c][r]) for c in range(6) if c != c_idx["forest"]])) for r in range(3)])

# Option B: One of the rugs is solid turquoise.
opt_b = Or([And(color_in_rug[c_idx["turquoise"]][r], 
                And([Not(color_in_rug[c][r]) for c in range(6) if c != c_idx["turquoise"]])) for r in range(3)])

# Option C: One of the rugs is solid yellow.
opt_c = Or([And(color_in_rug[c_idx["yellow"]][r], 
                And([Not(color_in_rug[c][r]) for c in range(6) if c != c_idx["yellow"]])) for r in range(3)])

# Option D: Forest and white are used together in a rug.
opt_d = Or([And(color_in_rug[c_idx["forest"]][r], color_in_rug[c_idx["white"]][r]) for r in range(3)])

# Option E: White and yellow are used together in a rug.
opt_e = Or([And(color_in_rug[c_idx["white"]][r], color_in_rug[c_idx["yellow"]][r]) for r in range(3)])

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