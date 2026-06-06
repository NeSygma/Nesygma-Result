from z3 import *

# BENCHMARK_MODE: ON (model-finding mode)
BENCHMARK_MODE = True

# Declare symbolic variables for rugs and colors
# Colors: forest=0, olive=1, peach=2, turquoise=3, white=4, yellow=5
# Rugs: each rug is a list of 3 Int variables (for up to 3 colors)
rug1 = [Int(f"rug1_color_{i}") for i in range(3)]
rug2 = [Int(f"rug2_color_{i}") for i in range(3)]
rug3 = [Int(f"rug3_color_{i}") for i in range(3)]

solver = Solver()

# Helper: all colors in a rug are within 0-5 or -1 (no color)
for rug in [rug1, rug2, rug3]:
    for c in rug:
        solver.add(Or([c == i for i in range(6)] + [c == -1]))
    # Distinctness within a rug (ignoring -1)
    for i in range(3):
        for j in range(i+1, 3):
            solver.add(Not(And(rug[i] != -1, rug[j] != -1, rug[i] == rug[j])))

# Exactly five colors are used in total (out of six available)
# We count the number of distinct colors used across all rugs
all_colors_used = []
for color in range(6):
    used = Bool(f"color_{color}_used")
    # A color is used if it appears in any rug
    solver.add(used == Or([Or([c == color for c in rug]) for rug in [rug1, rug2, rug3]]))
    all_colors_used.append(used)
solver.add(Sum([If(used, 1, 0) for used in all_colors_used]) == 5)

# Each color used is used in only one rug
for color in range(6):
    # For each color, it can appear in at most one rug
    appears_in = []
    for rug in [rug1, rug2, rug3]:
        appears_in.append(Or([c == color for c in rug]))
    solver.add(Sum([If(a, 1, 0) for a in appears_in]) <= 1)

# Rules:
# 1. In any rug in which white (4) is used, two other colors are also used.
#    => If white is in a rug, the rug must have at least 3 colors (white + 2 others)
for rug in [rug1, rug2, rug3]:
    has_white = Or([c == 4 for c in rug])
    num_colors = Sum([If(Or([c == i for i in range(6)]), 1, 0) for c in rug])
    solver.add(Implies(has_white, num_colors >= 3))

# 2. In any rug in which olive (1) is used, peach (2) is also used.
for rug in [rug1, rug2, rug3]:
    has_olive = Or([c == 1 for c in rug])
    has_peach = Or([c == 2 for c in rug])
    solver.add(Implies(has_olive, has_peach))

# 3. Forest (0) and turquoise (3) are not used together in a rug.
for rug in [rug1, rug2, rug3]:
    has_forest = Or([c == 0 for c in rug])
    has_turquoise = Or([c == 3 for c in rug])
    solver.add(Not(And(has_forest, has_turquoise)))

# 4. Peach (2) and turquoise (3) are not used together in a rug.
for rug in [rug1, rug2, rug3]:
    has_peach = Or([c == 2 for c in rug])
    has_turquoise = Or([c == 3 for c in rug])
    solver.add(Not(And(has_peach, has_turquoise)))

# 5. Peach (2) and yellow (5) are not used together in a rug.
for rug in [rug1, rug2, rug3]:
    has_peach = Or([c == 2 for c in rug])
    has_yellow = Or([c == 5 for c in rug])
    solver.add(Not(And(has_peach, has_yellow)))

# Additional constraint: One of the rugs is solid peach.
# A solid rug has exactly one color (peach=2) and no other colors.
rug1_is_solid_peach = And(
    Sum([If(c == 2, 1, 0) for c in rug1]) == 1,
    Sum([If(Or([c == i for i in range(6) if i != 2]), 1, 0) for c in rug1]) == 0
)
rug2_is_solid_peach = And(
    Sum([If(c == 2, 1, 0) for c in rug2]) == 1,
    Sum([If(Or([c == i for i in range(6) if i != 2]), 1, 0) for c in rug2]) == 0
)
rug3_is_solid_peach = And(
    Sum([If(c == 2, 1, 0) for c in rug3]) == 1,
    Sum([If(Or([c == i for i in range(6) if i != 2]), 1, 0) for c in rug3]) == 0
)
solver.add(Or(rug1_is_solid_peach, rug2_is_solid_peach, rug3_is_solid_peach))

# Now, evaluate each option to see which must be true
# We will check each option in turn, assuming the base constraints and the solid peach rug

# Option A: One of the rugs is solid forest.
opt_a_constr = Or(
    And(
        Sum([If(c == 0, 1, 0) for c in rug1]) == 1,
        Sum([If(Or([c == i for i in range(6) if i != 0]), 1, 0) for c in rug1]) == 0
    ),
    And(
        Sum([If(c == 0, 1, 0) for c in rug2]) == 1,
        Sum([If(Or([c == i for i in range(6) if i != 0]), 1, 0) for c in rug2]) == 0
    ),
    And(
        Sum([If(c == 0, 1, 0) for c in rug3]) == 1,
        Sum([If(Or([c == i for i in range(6) if i != 0]), 1, 0) for c in rug3]) == 0
    )
)

# Option B: One of the rugs is solid turquoise.
opt_b_constr = Or(
    And(
        Sum([If(c == 3, 1, 0) for c in rug1]) == 1,
        Sum([If(Or([c == i for i in range(6) if i != 3]), 1, 0) for c in rug1]) == 0
    ),
    And(
        Sum([If(c == 3, 1, 0) for c in rug2]) == 1,
        Sum([If(Or([c == i for i in range(6) if i != 3]), 1, 0) for c in rug2]) == 0
    ),
    And(
        Sum([If(c == 3, 1, 0) for c in rug3]) == 1,
        Sum([If(Or([c == i for i in range(6) if i != 3]), 1, 0) for c in rug3]) == 0
    )
)

# Option C: One of the rugs is solid yellow.
opt_c_constr = Or(
    And(
        Sum([If(c == 5, 1, 0) for c in rug1]) == 1,
        Sum([If(Or([c == i for i in range(6) if i != 5]), 1, 0) for c in rug1]) == 0
    ),
    And(
        Sum([If(c == 5, 1, 0) for c in rug2]) == 1,
        Sum([If(Or([c == i for i in range(6) if i != 5]), 1, 0) for c in rug2]) == 0
    ),
    And(
        Sum([If(c == 5, 1, 0) for c in rug3]) == 1,
        Sum([If(Or([c == i for i in range(6) if i != 5]), 1, 0) for c in rug3]) == 0
    )
)

# Option D: Forest and white are used together in a rug.
opt_d_constr = Or(
    And(Or([c == 0 for c in rug1]), Or([c == 4 for c in rug1])),
    And(Or([c == 0 for c in rug2]), Or([c == 4 for c in rug2])),
    And(Or([c == 0 for c in rug3]), Or([c == 4 for c in rug3]))
)

# Option E: White and yellow are used together in a rug.
opt_e_constr = Or(
    And(Or([c == 4 for c in rug1]), Or([c == 5 for c in rug1])),
    And(Or([c == 4 for c in rug2]), Or([c == 5 for c in rug2])),
    And(Or([c == 4 for c in rug3]), Or([c == 5 for c in rug3]))
)

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