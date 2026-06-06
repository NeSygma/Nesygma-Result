from z3 import *

# Define colors as integer constants for simplicity
forest_c, olive_c, peach_c, turquoise_c, white_c, yellow_c = 1, 2, 3, 4, 5, 6

# Rugs: each rug is a list of 3 symbolic constants (Int)
# A value of 0 means unused; otherwise, it represents the color used.
rug0 = [Int(f'rug0_{i}') for i in range(3)]
rug1 = [Int(f'rug1_{i}') for i in range(3)]
rug2 = [Int(f'rug2_{i}') for i in range(3)]

# Initialize solver
solver = Solver()

# Set each rug's variables to be 0 (unused) or one of the color constants
for i in range(3):
    solver.add(Or(rug0[i] == 0, rug0[i] == forest_c, rug0[i] == olive_c, rug0[i] == peach_c, rug0[i] == turquoise_c, rug0[i] == white_c, rug0[i] == yellow_c))
    solver.add(Or(rug1[i] == 0, rug1[i] == forest_c, rug1[i] == olive_c, rug1[i] == peach_c, rug1[i] == turquoise_c, rug1[i] == white_c, rug1[i] == yellow_c))
    solver.add(Or(rug2[i] == 0, rug2[i] == forest_c, rug2[i] == olive_c, rug2[i] == peach_c, rug2[i] == turquoise_c, rug2[i] == white_c, rug2[i] == yellow_c))

# Helper to count non-zero colors in a rug (zero means unused)
def count_colors(rug):
    return Sum([If(c != 0, 1, 0) for c in rug])

# Helper to check if a rug contains a specific color
colors_list = [forest_c, olive_c, peach_c, turquoise_c, white_c, yellow_c]

def rug_has_color(rug, color):
    return Or([And(c != 0, c == color) for c in rug])

# Exactly two rugs are solid (count == 1), one is multicolored (count >= 2)
# We'll enforce this by adding constraints on the count of non-zero colors.
count_rug0 = count_colors(rug0)
count_rug1 = count_colors(rug1)
count_rug2 = count_colors(rug2)

solver.add(count_rug0 == 1)
solver.add(count_rug1 == 1)
solver.add(count_rug2 >= 2)

# Exactly five colors are used in total (one color is unused)
# Track which colors are used
used_colors = [Bool(f'used_{c}') for c in colors_list]

# For each color, it is used if it appears in any rug (non-zero)
for i, c in enumerate(colors_list):
    solver.add(used_colors[i] == Or(
        Or([And(rug0[j] != 0, rug0[j] == c) for j in range(3)]),
        Or([And(rug1[j] != 0, rug1[j] == c) for j in range(3)]),
        Or([And(rug2[j] != 0, rug2[j] == c) for j in range(3)])
    ))

# Exactly one color is not used
solver.add(Sum([If(used, 1, 0) for used in used_colors]) == 5)

# Rules:
# 1. In any rug in which white is used, two other colors are also used.
#    => If a rug contains white, it must have at least 3 colors (white + 2 others)
for rug in [rug0, rug1, rug2]:
    has_white = rug_has_color(rug, white_c)
    count = count_colors(rug)
    solver.add(Implies(has_white, count >= 3))

# 2. In any rug in which olive is used, peach is also used.
for rug in [rug0, rug1, rug2]:
    has_olive = rug_has_color(rug, olive_c)
    has_peach = rug_has_color(rug, peach_c)
    solver.add(Implies(has_olive, has_peach))

# 3. Forest and turquoise are not used together in a rug.
for rug in [rug0, rug1, rug2]:
    has_forest = rug_has_color(rug, forest_c)
    has_turquoise = rug_has_color(rug, turquoise_c)
    solver.add(Not(And(has_forest, has_turquoise)))

# 4. Peach and turquoise are not used together in a rug.
for rug in [rug0, rug1, rug2]:
    has_peach = rug_has_color(rug, peach_c)
    has_turquoise = rug_has_color(rug, turquoise_c)
    solver.add(Not(And(has_peach, has_turquoise)))

# 5. Peach and yellow are not used together in a rug.
for rug in [rug0, rug1, rug2]:
    has_peach = rug_has_color(rug, peach_c)
    has_yellow = rug_has_color(rug, yellow_c)
    solver.add(Not(And(has_peach, has_yellow)))

# For each color, it can appear in at most one rug (since each color used is in only one rug)
for c in colors_list:
    count_c_in_rugs = Sum([If(rug_has_color(rug, c), 1, 0) for rug in [rug0, rug1, rug2]])
    solver.add(count_c_in_rugs <= 1)

# Now, evaluate the multiple-choice options
# For each option, assume the two solid rugs are rug0 and rug1 with the colors in the option
# The third rug (rug2) must be multicolored and use the remaining colors, respecting all rules

# Define the options as pairs of colors for the two solid rugs
options = [
    ("A", [forest_c, peach_c]),
    ("B", [forest_c, yellow_c]),
    ("C", [peach_c, turquoise_c]),
    ("D", [peach_c, yellow_c]),
    ("E", [turquoise_c, yellow_c])
]

found_options = []
for letter, solid_colors in options:
    solver.push()
    # Assign the two solid rugs to have exactly one color each, and those colors are in solid_colors
    # rug0: one color = solid_colors[0], others 0
    solver.add(And(rug0[0] == solid_colors[0], rug0[1] == 0, rug0[2] == 0))
    
    # rug1: one color = solid_colors[1], others 0
    solver.add(And(rug1[0] == solid_colors[1], rug1[1] == 0, rug1[2] == 0))
    
    # Ensure the two solid colors are not reused in rug2
    solver.add(And(rug2[0] != solid_colors[0], rug2[1] != solid_colors[0], rug2[2] != solid_colors[0]))
    solver.add(And(rug2[0] != solid_colors[1], rug2[1] != solid_colors[1], rug2[2] != solid_colors[1]))
    
    # Check if this assignment is possible
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