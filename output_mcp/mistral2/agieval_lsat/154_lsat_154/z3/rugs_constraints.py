from z3 import *

# BENCHMARK_MODE: ON (model-finding mode)
BENCHMARK_MODE = True

# Declare colors as integers for indexing
colors = {
    "forest": 0,
    "olive": 1,
    "peach": 2,
    "turquoise": 3,
    "white": 4,
    "yellow": 5
}

# Total colors available
num_colors = len(colors)

# Number of rugs
num_rugs = 3

# Create a solver
solver = Solver()

# Each rug is represented as a set of colors used in it
# We use a list of BitVecs to represent the presence of each color in each rug
rugs = [[Bool(f"rug_{i}_color_{c}") for c in range(num_colors)] for i in range(num_rugs)]

# Helper function to get the set of colors used in a rug
def get_rug_colors(rug_idx):
    return [rugs[rug_idx][c] for c in range(num_colors)]

# Helper function to count the number of colors used in a rug
def count_colors_in_rug(rug_idx):
    return Sum([If(Or(rugs[rug_idx][c] for c in range(num_colors)), 1, 0)])

# Helper function to check if a rug is solid (exactly one color)
def is_solid_rug(rug_idx):
    # A rug is solid if exactly one color is used
    return And(
        count_colors_in_rug(rug_idx) == 1,
        Or([And(rugs[rug_idx][c], *[Not(rugs[rug_idx][k]) for k in range(num_colors) if k != c]) for c in range(num_colors)])
    )

# Helper function to get the single color in a solid rug
def get_solid_color(rug_idx):
    return [If(rugs[rug_idx][c], c, -1) for c in range(num_colors)]

# Constraint: Exactly 5 colors are used in total across all rugs
total_colors_used = Sum([
    If(Or([rugs[i][c] for i in range(num_rugs)]), 1, 0) for c in range(num_colors)
])
solver.add(total_colors_used == 5)

# Constraint: One rug is solid yellow
# Find the rug that is solid yellow
solid_yellow_rug = Int("solid_yellow_rug")
solver.add(solid_yellow_rug >= 0, solid_yellow_rug < num_rugs)
solver.add(is_solid_rug(solid_yellow_rug))
solver.add(rugs[solid_yellow_rug][colors["yellow"]])

# Constraint: In any rug in which white is used, two other colors are also used
for i in range(num_rugs):
    white_used = rugs[i][colors["white"]]
    other_colors_used = Sum([If(rugs[i][c], 1, 0) for c in range(num_colors) if c != colors["white"]])
    solver.add(Implies(white_used, other_colors_used >= 2))

# Constraint: In any rug in which olive is used, peach is also used
for i in range(num_rugs):
    olive_used = rugs[i][colors["olive"]]
    peach_used = rugs[i][colors["peach"]]
    solver.add(Implies(olive_used, peach_used))

# Constraint: Forest and turquoise are not used together in a rug
for i in range(num_rugs):
    forest_used = rugs[i][colors["forest"]]
    turquoise_used = rugs[i][colors["turquoise"]]
    solver.add(Not(And(forest_used, turquoise_used)))

# Constraint: Peach and turquoise are not used together in a rug
for i in range(num_rugs):
    peach_used = rugs[i][colors["peach"]]
    turquoise_used = rugs[i][colors["turquoise"]]
    solver.add(Not(And(peach_used, turquoise_used)))

# Constraint: Peach and yellow are not used together in a rug
for i in range(num_rugs):
    peach_used = rugs[i][colors["peach"]]
    yellow_used = rugs[i][colors["yellow"]]
    solver.add(Not(And(peach_used, yellow_used)))

# Now, evaluate each option to see if it is possible
found_options = []

# Option A: There is exactly one solid color rug
solver.push()
# Count the number of solid rugs
num_solid_rugs = Sum([If(is_solid_rug(i), 1, 0) for i in range(num_rugs)])
solver.add(num_solid_rugs == 1)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: One of the rugs is solid forest
solver.push()
# Find a rug that is solid forest
solid_forest_rug = Int("solid_forest_rug")
solver.add(solid_forest_rug >= 0, solid_forest_rug < num_rugs)
solver.add(is_solid_rug(solid_forest_rug))
solver.add(rugs[solid_forest_rug][colors["forest"]])
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: Turquoise is not used in any of the rugs
solver.push()
for i in range(num_rugs):
    solver.add(Not(rugs[i][colors["turquoise"]]))
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: Forest and olive are used together in a rug
solver.push()
for i in range(num_rugs):
    forest_used = rugs[i][colors["forest"]]
    olive_used = rugs[i][colors["olive"]]
    solver.add(And(forest_used, olive_used))
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: Peach and white are used together in a rug
solver.push()
for i in range(num_rugs):
    peach_used = rugs[i][colors["peach"]]
    white_used = rugs[i][colors["white"]]
    solver.add(And(peach_used, white_used))
if solver.check() == sat:
    found_options.append("E")
solver.pop()

# Output the result
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")