from z3 import *

solver = Solver()

# Colors
colors = ["forest", "olive", "peach", "turquoise", "white", "yellow"]
color_vars = {c: Bool(c) for c in colors}

# Rugs: 3 rugs, each can be solid (single color) or multicolored (multiple colors)
# We represent each rug as a list of colors used in it
rugs = [[Bool(f"rug_{i}_color_{c}") for c in colors] for i in range(3)]

# Exactly five colors are used in total
solver.add(Sum([If(color_vars[c], 1, 0) for c in colors]) == 5)

# Each color used is used in only one rug
for c in colors:
    solver.add(Or([rugs[i][colors.index(c)] for i in range(3)]) == color_vars[c])
    for i in range(3):
        for j in range(i + 1, 3):
            solver.add(Implies(rugs[i][colors.index(c)], Not(rugs[j][colors.index(c)])))

# Rule 1: In any rug in which white is used, two other colors are also used.
white_idx = colors.index("white")
for i in range(3):
    solver.add(Implies(rugs[i][white_idx], 
                       Sum([If(rugs[i][colors.index(c)], 1, 0) for c in colors]) >= 3))

# Rule 2: In any rug in which olive is used, peach is also used.
olive_idx = colors.index("olive")
peach_idx = colors.index("peach")
for i in range(3):
    solver.add(Implies(rugs[i][olive_idx], rugs[i][peach_idx]))

# Rule 3: Forest and turquoise are not used together in a rug.
forest_idx = colors.index("forest")
turquoise_idx = colors.index("turquoise")
for i in range(3):
    solver.add(Not(And(rugs[i][forest_idx], rugs[i][turquoise_idx])))

# Rule 4: Peach and turquoise are not used together in a rug.
for i in range(3):
    solver.add(Not(And(rugs[i][peach_idx], rugs[i][turquoise_idx])))

# Rule 5: Peach and yellow are not used together in a rug.
for i in range(3):
    solver.add(Not(And(rugs[i][peach_idx], rugs[i][colors.index("yellow")])))

# Exactly two solid rugs: a rug is solid if it has exactly one color
solid_rugs = [Int(f"solid_rug_{i}") for i in range(3)]
for i in range(3):
    # Count the number of colors in rug i
    color_count = Sum([If(rugs[i][colors.index(c)], 1, 0) for c in colors])
    # Solid rug: color_count == 1
    solver.add(Implies(color_count == 1, solid_rugs[i] == 1))
    solver.add(Implies(color_count > 1, solid_rugs[i] == 0))

# Exactly two solid rugs
total_solid = Sum(solid_rugs)
solver.add(total_solid == 2)

# Now, evaluate the answer choices
# We need to check which of the given pairs of colors cannot both be solid rugs

# Helper function to check if a pair of colors can both be solid rugs
found_options = []

# Option A: forest and peach
solver.push()
# Assume forest and peach are the two solid rugs
# Find the rugs that use forest and peach and set them as solid
solver.add(Or([And(solid_rugs[i] == 1, rugs[i][forest_idx]) for i in range(3)]))
solver.add(Or([And(solid_rugs[i] == 1, rugs[i][peach_idx]) for i in range(3)]))
# Ensure no other rug is solid
solver.add(Sum([If(solid_rugs[i] == 1, 1, 0) for i in range(3)]) == 2)
# Ensure forest and peach are not in the same rug
solver.add(Not(And([rugs[i][forest_idx] and rugs[i][peach_idx] for i in range(3)])))
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: forest and yellow
solver.push()
solver.add(Or([And(solid_rugs[i] == 1, rugs[i][forest_idx]) for i in range(3)]))
solver.add(Or([And(solid_rugs[i] == 1, rugs[i][colors.index("yellow")]) for i in range(3)]))
solver.add(Sum([If(solid_rugs[i] == 1, 1, 0) for i in range(3)]) == 2)
solver.add(Not(And([rugs[i][forest_idx] and rugs[i][colors.index("yellow")] for i in range(3)])))
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: peach and turquoise
solver.push()
solver.add(Or([And(solid_rugs[i] == 1, rugs[i][peach_idx]) for i in range(3)]))
solver.add(Or([And(solid_rugs[i] == 1, rugs[i][turquoise_idx]) for i in range(3)]))
solver.add(Sum([If(solid_rugs[i] == 1, 1, 0) for i in range(3)]) == 2)
solver.add(Not(And([rugs[i][peach_idx] and rugs[i][turquoise_idx] for i in range(3)])))
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: peach and yellow
solver.push()
solver.add(Or([And(solid_rugs[i] == 1, rugs[i][peach_idx]) for i in range(3)]))
solver.add(Or([And(solid_rugs[i] == 1, rugs[i][colors.index("yellow")]) for i in range(3)]))
solver.add(Sum([If(solid_rugs[i] == 1, 1, 0) for i in range(3)]) == 2)
solver.add(Not(And([rugs[i][peach_idx] and rugs[i][colors.index("yellow")] for i in range(3)])))
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: turquoise and yellow
solver.push()
solver.add(Or([And(solid_rugs[i] == 1, rugs[i][turquoise_idx]) for i in range(3)]))
solver.add(Or([And(solid_rugs[i] == 1, rugs[i][colors.index("yellow")]) for i in range(3)]))
solver.add(Sum([If(solid_rugs[i] == 1, 1, 0) for i in range(3)]) == 2)
solver.add(Not(And([rugs[i][turquoise_idx] and rugs[i][colors.index("yellow")] for i in range(3)])))
if solver.check() == sat:
    found_options.append("E")
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