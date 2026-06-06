from z3 import *

solver = Solver()

# Colors available
colors = ["forest", "olive", "peach", "turquoise", "white", "yellow"]

# We will use a list to represent the colors used in each rug.
# rugs[0], rugs[1], rugs[2] are the sets of colors for each rug.
# We represent each rug as a list of Booleans indicating if a color is used in that rug.
rugs = [[Bool(f"rug_{i}_forest"), Bool(f"rug_{i}_olive"), Bool(f"rug_{i}_peach"), 
         Bool(f"rug_{i}_turquoise"), Bool(f"rug_{i}_white"), Bool(f"rug_{i}_yellow")] 
        for i in range(3)]

# Helper function to extract the color Booleans for a rug
def get_rug_colors(rug_idx):
    return {
        "forest": rugs[rug_idx][0],
        "olive": rugs[rug_idx][1],
        "peach": rugs[rug_idx][2],
        "turquoise": rugs[rug_idx][3],
        "white": rugs[rug_idx][4],
        "yellow": rugs[rug_idx][5],
    }

# Exactly five of the six colors are used in total.
# We sum the number of colors used across all rugs and constrain it to 5.
color_used = []
for c in range(6):
    solver.add(Or([rugs[r][c] for r in range(3)]))
    color_used.append(Or([rugs[r][c] for r in range(3)]))

solver.add(Sum(color_used) == 5)

# Each color used is used in only one rug.
for c in range(6):
    solver.add(AtMost(*[rugs[r][c] for r in range(3)], 1))

# Rules:
# 1. In any rug in which white is used, two other colors are also used.
for r in range(3):
    white_used = rugs[r][4]  # white is index 4
    other_colors = Sum([If(rugs[r][c], 1, 0) for c in range(6) if c != 4])
    solver.add(Implies(white_used, other_colors >= 2))

# 2. In any rug in which olive is used, peach is also used.
for r in range(3):
    olive_used = rugs[r][1]  # olive is index 1
    peach_used = rugs[r][2]  # peach is index 2
    solver.add(Implies(olive_used, peach_used))

# 3. Forest and turquoise are not used together in a rug.
for r in range(3):
    forest_used = rugs[r][0]  # forest is index 0
    turquoise_used = rugs[r][3]  # turquoise is index 3
    solver.add(Not(And(forest_used, turquoise_used)))

# 4. Peach and turquoise are not used together in a rug.
for r in range(3):
    peach_used = rugs[r][2]  # peach is index 2
    turquoise_used = rugs[r][3]  # turquoise is index 3
    solver.add(Not(And(peach_used, turquoise_used)))

# 5. Peach and yellow are not used together in a rug.
for r in range(3):
    peach_used = rugs[r][2]  # peach is index 2
    yellow_used = rugs[r][5]  # yellow is index 5
    solver.add(Not(And(peach_used, yellow_used)))

# Multiple choice options
# We will encode each option as a set of constraints on the rugs.

# Option A: forest only; turquoise only; olive, peach, and white
opt_a_constr = [
    # Rug 0: forest only
    And([
        rugs[0][0],  # forest
        Not(rugs[0][1]), Not(rugs[0][2]), Not(rugs[0][3]), Not(rugs[0][4]), Not(rugs[0][5])
    ]),
    # Rug 1: turquoise only
    And([
        rugs[1][3],  # turquoise
        Not(rugs[1][0]), Not(rugs[1][1]), Not(rugs[1][2]), Not(rugs[1][4]), Not(rugs[1][5])
    ]),
    # Rug 2: olive, peach, and white
    And([
        rugs[2][1], rugs[2][2], rugs[2][4],  # olive, peach, white
        Not(rugs[2][0]), Not(rugs[2][3]), Not(rugs[2][5])  # not forest, turquoise, yellow
    ])
]

# Option B: forest only; turquoise only; olive, peach, and yellow
opt_b_constr = [
    # Rug 0: forest only
    And([
        rugs[0][0],  # forest
        Not(rugs[0][1]), Not(rugs[0][2]), Not(rugs[0][3]), Not(rugs[0][4]), Not(rugs[0][5])
    ]),
    # Rug 1: turquoise only
    And([
        rugs[1][3],  # turquoise
        Not(rugs[1][0]), Not(rugs[1][1]), Not(rugs[1][2]), Not(rugs[1][4]), Not(rugs[1][5])
    ]),
    # Rug 2: olive, peach, and yellow
    And([
        rugs[2][1], rugs[2][2], rugs[2][5],  # olive, peach, yellow
        Not(rugs[2][0]), Not(rugs[2][3]), Not(rugs[2][4])  # not forest, turquoise, white
    ])
]

# Option C: peach only; turquoise only; forest, olive, and white
opt_c_constr = [
    # Rug 0: peach only
    And([
        rugs[0][2],  # peach
        Not(rugs[0][0]), Not(rugs[0][1]), Not(rugs[0][3]), Not(rugs[0][4]), Not(rugs[0][5])
    ]),
    # Rug 1: turquoise only
    And([
        rugs[1][3],  # turquoise
        Not(rugs[1][0]), Not(rugs[1][1]), Not(rugs[1][2]), Not(rugs[1][4]), Not(rugs[1][5])
    ]),
    # Rug 2: forest, olive, and white
    And([
        rugs[2][0], rugs[2][1], rugs[2][4],  # forest, olive, white
        Not(rugs[2][2]), Not(rugs[2][3]), Not(rugs[2][5])  # not peach, turquoise, yellow
    ])
]

# Option D: yellow only; forest and turquoise; olive and peach
opt_d_constr = [
    # Rug 0: yellow only
    And([
        rugs[0][5],  # yellow
        Not(rugs[0][0]), Not(rugs[0][1]), Not(rugs[0][2]), Not(rugs[0][3]), Not(rugs[0][4])
    ]),
    # Rug 1: forest and turquoise
    And([
        rugs[1][0], rugs[1][3],  # forest, turquoise
        Not(rugs[1][1]), Not(rugs[1][2]), Not(rugs[1][4]), Not(rugs[1][5])
    ]),
    # Rug 2: olive and peach
    And([
        rugs[2][1], rugs[2][2],  # olive, peach
        Not(rugs[2][0]), Not(rugs[2][3]), Not(rugs[2][4]), Not(rugs[2][5])
    ])
]

# Option E: yellow only; olive and peach; turquoise and white
opt_e_constr = [
    # Rug 0: yellow only
    And([
        rugs[0][5],  # yellow
        Not(rugs[0][0]), Not(rugs[0][1]), Not(rugs[0][2]), Not(rugs[0][3]), Not(rugs[0][4])
    ]),
    # Rug 1: olive and peach
    And([
        rugs[1][1], rugs[1][2],  # olive, peach
        Not(rugs[1][0]), Not(rugs[1][3]), Not(rugs[1][4]), Not(rugs[1][5])
    ]),
    # Rug 2: turquoise and white
    And([
        rugs[2][3], rugs[2][4],  # turquoise, white
        Not(rugs[2][0]), Not(rugs[2][1]), Not(rugs[2][2]), Not(rugs[2][5])
    ])
]

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