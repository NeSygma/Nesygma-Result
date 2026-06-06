from z3 import *

# BENCHMARK_MODE: ON (model-finding mode)
BENCHMARK_MODE = True

solver = Solver()

# Declare rugs and colors
# Rugs: 3 rugs, each can be solid or multicolored
# Colors: forest, olive, peach, turquoise, white, yellow (6 total, 5 used)
rugs = 3
colors = ["forest", "olive", "peach", "turquoise", "white", "yellow"]

# For each color, assign it to a rug (0, 1, or 2) or mark it as unused (-1)
color_to_rug = {c: Int(f"color_to_rug_{c}") for c in colors}

# Each color is either assigned to a rug or unused
for c in colors:
    solver.add(Or([color_to_rug[c] == i for i in range(rugs)] + [color_to_rug[c] == -1]))

# Exactly 5 colors are used (one color is unused)
used_colors = [color_to_rug[c] != -1 for c in colors]
solver.add(Sum([If(used, 1, 0) for used in used_colors]) == 5)

# For each rug, determine if it is solid or multicolored
# A rug is solid if exactly one color is used in it
# A rug is multicolored if more than one color is used in it
rug_is_solid = [Bool(f"rug_is_solid_{i}") for i in range(rugs)]
rug_is_multicolored = [Bool(f"rug_is_multicolored_{i}") for i in range(rugs)]

for i in range(rugs):
    # Count the number of colors in rug i
    colors_in_rug_i = [If(color_to_rug[c] == i, 1, 0) for c in colors]
    num_colors_in_rug_i = Sum(colors_in_rug_i)
    
    # A rug is solid if exactly one color is used in it
    solver.add(rug_is_solid[i] == (num_colors_in_rug_i == 1))
    # A rug is multicolored if more than one color is used in it
    solver.add(rug_is_multicolored[i] == (num_colors_in_rug_i > 1))

# Constraints from the problem:
# 1. In any rug in which white is used, two other colors are also used.
# This means if white is in a rug, that rug must have at least 3 colors (white + 2 others).
for i in range(rugs):
    solver.add(Implies(color_to_rug["white"] == i, 
                       Sum([If(color_to_rug[c] == i, 1, 0) for c in colors]) >= 3))

# 2. In any rug in which olive is used, peach is also used.
for i in range(rugs):
    solver.add(Implies(color_to_rug["olive"] == i, 
                       color_to_rug["peach"] == i))

# 3. Forest and turquoise are not used together in a rug.
for i in range(rugs):
    solver.add(Not(And(color_to_rug["forest"] == i, color_to_rug["turquoise"] == i)))

# 4. Peach and turquoise are not used together in a rug.
for i in range(rugs):
    solver.add(Not(And(color_to_rug["peach"] == i, color_to_rug["turquoise"] == i)))

# 5. Peach and yellow are not used together in a rug.
for i in range(rugs):
    solver.add(Not(And(color_to_rug["peach"] == i, color_to_rug["yellow"] == i)))

# Now, evaluate the multiple choice options
# We will check each option to see if it must be true in all valid models

# Option A: There are no multicolored rugs in which forest is used.
# This means: for all rugs, if forest is used in the rug, the rug is not multicolored.
opt_a_constr = And([Implies(color_to_rug["forest"] == i, Not(rug_is_multicolored[i])) for i in range(rugs)])

# Option B: There are no multicolored rugs in which turquoise is used.
opt_b_constr = And([Implies(color_to_rug["turquoise"] == i, Not(rug_is_multicolored[i])) for i in range(rugs)])

# Option C: Peach is used in one of the rugs.
opt_c_constr = (color_to_rug["peach"] != -1)

# Option D: Turquoise is used in one of the rugs.
opt_d_constr = (color_to_rug["turquoise"] != -1)

# Option E: Yellow is used in one of the rugs.
opt_e_constr = (color_to_rug["yellow"] != -1)

# Now, check each option
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