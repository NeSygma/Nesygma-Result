from z3 import *

# Define color constants
forest, olive, peach, turquoise, white, yellow = Ints('forest olive peach turquoise white yellow')
color_constants = [forest, olive, peach, turquoise, white, yellow]

# Helper function to create a color sort
ColorSort = Datatype('ColorSort')
ColorSort.declare('forest')
ColorSort.declare('olive')
ColorSort.declare('peach')
ColorSort.declare('turquoise')
ColorSort.declare('white')
ColorSort.declare('yellow')
ColorSort = ColorSort.create()

forest_c, olive_c, peach_c, turquoise_c, white_c, yellow_c = [
    ColorSort.forest,
    ColorSort.olive,
    ColorSort.peach,
    ColorSort.turquoise,
    ColorSort.white,
    ColorSort.yellow
]

# Rugs: each rug is a list of colors it uses
# rug0, rug1, rug2 = [ColorSort], [ColorSort], [ColorSort]
rug0_colors = Const('rug0_colors', ArraySort(IntSort(), ColorSort))
rug1_colors = Const('rug1_colors', ArraySort(IntSort(), ColorSort))
rug2_colors = Const('rug2_colors', ArraySort(IntSort(), ColorSort))

# Helper to get the length of a rug's colors
# Since we can't directly get the length of an array, we'll model rugs as lists with a sentinel value
# Alternative: model rugs as a list of optional colors, with a special "none" value
# For simplicity, we'll use a list of 3 colors per rug, with unused slots marked as a special value
# But this complicates things. Instead, we'll model rugs as a set of colors used, with a fixed max size.

# Simpler approach: model each rug as a list of up to 3 colors, with unused slots as None
rug0 = [Const(f'rug0_{i}', ColorSort) for i in range(3)]
rug1 = [Const(f'rug1_{i}', ColorSort) for i in range(3)]
rug2 = [Const(f'rug2_{i}', ColorSort) for i in range(3)]

# Sentinel value to represent "no color"
none_color = Const('none_color', ColorSort)
none_color = ColorSort.peach  # dummy assignment, will be constrained to be unique

# Each rug's colors are either a color or none_color
# We'll add constraints to ensure that the first k elements are colors, and the rest are none_color

solver = Solver()

# Each rug is either solid (one color) or multicolored (multiple colors)
# We'll enforce that exactly two rugs have exactly one color, and one rug has at least two colors

# Helper to count non-none colors in a rug
def count_colors(rug):
    return Sum([If(c != none_color, 1, 0) for c in rug])

# Exactly two rugs are solid (count == 1), one is multicolored (count >= 2)
solver.add(count_colors(rug0) == 1)
solver.add(count_colors(rug1) == 1)
solver.add(count_colors(rug2) >= 2)

# Exactly five colors are used in total (one color is unused)
# We'll track which colors are used
used_colors = [Bool(f'used_{c}') for c in [forest_c, olive_c, peach_c, turquoise_c, white_c, yellow_c]]

# For each color, it is used if it appears in any rug
for i, c in enumerate([forest_c, olive_c, peach_c, turquoise_c, white_c, yellow_c]):
    solver.add(used_colors[i] == Or(
        Or([rug0[j] == c for j in range(3)]),
        Or([rug1[j] == c for j in range(3)]),
        Or([rug2[j] == c for j in range(3)])
    ))

# Exactly one color is not used
solver.add(Sum([If(used, 1, 0) for used in used_colors]) == 5)

# Rules:
# 1. In any rug in which white is used, two other colors are also used.
#    => If a rug contains white, it must have at least 3 colors (white + 2 others)
for rug in [rug0, rug1, rug2]:
    has_white = Or([c == white_c for c in rug])
    count = count_colors(rug)
    solver.add(Implies(has_white, count >= 3))

# 2. In any rug in which olive is used, peach is also used.
for rug in [rug0, rug1, rug2]:
    has_olive = Or([c == olive_c for c in rug])
    has_peach = Or([c == peach_c for c in rug])
    solver.add(Implies(has_olive, has_peach))

# 3. Forest and turquoise are not used together in a rug.
for rug in [rug0, rug1, rug2]:
    has_forest = Or([c == forest_c for c in rug])
    has_turquoise = Or([c == turquoise_c for c in rug])
    solver.add(Not(And(has_forest, has_turquoise)))

# 4. Peach and turquoise are not used together in a rug.
for rug in [rug0, rug1, rug2]:
    has_peach = Or([c == peach_c for c in rug])
    has_turquoise = Or([c == turquoise_c for c in rug])
    solver.add(Not(And(has_peach, has_turquoise)))

# 5. Peach and yellow are not used together in a rug.
for rug in [rug0, rug1, rug2]:
    has_peach = Or([c == peach_c for c in rug])
    has_yellow = Or([c == yellow_c for c in rug])
    solver.add(Not(And(has_peach, has_yellow)))

# Ensure none_color is unique and not equal to any real color
solver.add(none_color != forest_c)
solver.add(none_color != olive_c)
solver.add(none_color != peach_c)
solver.add(none_color != turquoise_c)
solver.add(none_color != white_c)
solver.add(none_color != yellow_c)

# Ensure that in each rug, the colors are either a real color or none_color, and that none_color only appears after all real colors
for rug in [rug0, rug1, rug2]:
    for i in range(2):
        solver.add(Or(rug[i] == none_color, rug[i+1] == none_color))
        solver.add(Implies(rug[i] == none_color, rug[i+1] == none_color))

# Now, evaluate the multiple-choice options
# For each option, assume the two solid rugs are the pair given in the option
# The third rug must be multicolored and use the remaining colors, respecting all rules

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
    # Assign the two solid rugs to the colors in the option
    # We need to assign two rugs to be solid and use exactly the colors in solid_colors
    # The third rug will be multicolored
    # We'll try to assign the two solid colors to two rugs, and the third rug will use the remaining colors
    # To do this, we'll enforce that two rugs have exactly one color, and those colors are in solid_colors
    # The third rug will have the remaining colors
    
    # Enforce that two rugs have exactly one color, and those colors are in solid_colors
    # We'll try all combinations of assigning the two solid colors to two rugs
    # Since the rugs are symmetric, we can just assign the two solid colors to any two rugs
    # For simplicity, assign rug0 and rug1 to be solid with the two colors in solid_colors
    # rug2 will be multicolored
    
    # Assign rug0 and rug1 to be solid with the two colors in solid_colors
    # rug0 has exactly one color, which is solid_colors[0]
    # rug1 has exactly one color, which is solid_colors[1]
    # rug2 has at least two colors
    
    # Assign rug0 to have exactly one color: solid_colors[0]
    solver.add(rug0[0] == solid_colors[0])
    solver.add(rug0[1] == none_color)
    solver.add(rug0[2] == none_color)
    
    # Assign rug1 to have exactly one color: solid_colors[1]
    solver.add(rug1[0] == solid_colors[1])
    solver.add(rug1[1] == none_color)
    solver.add(rug1[2] == none_color)
    
    # rug2 must have at least two colors
    # We don't assign specific colors here; the solver will find a valid assignment
    
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