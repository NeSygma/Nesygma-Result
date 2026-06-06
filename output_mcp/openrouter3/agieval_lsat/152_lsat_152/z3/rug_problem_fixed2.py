from z3 import *

# Colors: forest, olive, peach, turquoise, white, yellow
# We'll use indices: 0=forest, 1=olive, 2=peach, 3=turquoise, 4=white, 5=yellow
colors = ["forest", "olive", "peach", "turquoise", "white", "yellow"]

# Variables: which rug each color belongs to (0, 1, 2) or -1 if unused
color_rug = [Int(f"rug_{c}") for c in colors]

solver = Solver()

# Exactly 5 colors are used (one is unused)
used_colors = [If(color_rug[i] != -1, 1, 0) for i in range(6)]
solver.add(Sum(used_colors) == 5)

# Rule 1: If white (index 4) is used, it must be in a rug with exactly 3 colors
white_rug = color_rug[4]

# For each rug (0,1,2), count how many colors are in it
for rug in range(3):
    count = Sum([If(color_rug[i] == rug, 1, 0) for i in range(6)])
    # If white is in this rug, then count must be 3
    solver.add(Implies(white_rug == rug, count == 3))

# Rule 2: If olive (index 1) is used, peach (index 2) must also be used in same rug
olive_rug = color_rug[1]
peach_rug = color_rug[2]
solver.add(Implies(olive_rug != -1, olive_rug == peach_rug))

# Rule 3: Forest (0) and turquoise (3) cannot be together
solver.add(Or(color_rug[0] == -1, color_rug[3] == -1, color_rug[0] != color_rug[3]))

# Rule 4: Peach (2) and turquoise (3) cannot be together
solver.add(Or(color_rug[2] == -1, color_rug[3] == -1, color_rug[2] != color_rug[3]))

# Rule 5: Peach (2) and yellow (5) cannot be together
solver.add(Or(color_rug[2] == -1, color_rug[5] == -1, color_rug[2] != color_rug[5]))

# Additional constraint: exactly two rugs are solid (have exactly one color)
# Count colors per rug
rug_color_count = []
for rug in range(3):
    count = Sum([If(color_rug[i] == rug, 1, 0) for i in range(6)])
    rug_color_count.append(count)

solid_rugs = [If(rug_color_count[r] == 1, 1, 0) for r in range(3)]
solver.add(Sum(solid_rugs) == 2)

# Now test each answer choice
found_options = []

# Helper function to check if a color's rug is solid
def is_rug_solid(color_idx):
    # Returns a constraint that the rug containing color_idx has exactly 1 color
    # Using Or-Loop pattern
    return Or([And(color_rug[color_idx] == rug, rug_color_count[rug] == 1) for rug in range(3)])

# Option A: forest and peach
solver.push()
# Forest and peach are solid, meaning each is alone in its rug
# Also, they must be in different rugs (since they're two different solid rugs)
solver.add(color_rug[0] != -1)  # forest used
solver.add(color_rug[2] != -1)  # peach used
solver.add(is_rug_solid(0))  # forest's rug is solid
solver.add(is_rug_solid(2))  # peach's rug is solid
solver.add(color_rug[0] != color_rug[2])  # different rugs
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: forest and yellow
solver.push()
solver.add(color_rug[0] != -1)  # forest used
solver.add(color_rug[5] != -1)  # yellow used
solver.add(is_rug_solid(0))  # forest's rug is solid
solver.add(is_rug_solid(5))  # yellow's rug is solid
solver.add(color_rug[0] != color_rug[5])  # different rugs
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: peach and turquoise
solver.push()
solver.add(color_rug[2] != -1)  # peach used
solver.add(color_rug[3] != -1)  # turquoise used
solver.add(is_rug_solid(2))  # peach's rug is solid
solver.add(is_rug_solid(3))  # turquoise's rug is solid
solver.add(color_rug[2] != color_rug[3])  # different rugs
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: peach and yellow
solver.push()
solver.add(color_rug[2] != -1)  # peach used
solver.add(color_rug[5] != -1)  # yellow used
solver.add(is_rug_solid(2))  # peach's rug is solid
solver.add(is_rug_solid(5))  # yellow's rug is solid
solver.add(color_rug[2] != color_rug[5])  # different rugs
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: turquoise and yellow
solver.push()
solver.add(color_rug[3] != -1)  # turquoise used
solver.add(color_rug[5] != -1)  # yellow used
solver.add(is_rug_solid(3))  # turquoise's rug is solid
solver.add(is_rug_solid(5))  # yellow's rug is solid
solver.add(color_rug[3] != color_rug[5])  # different rugs
if solver.check() == sat:
    found_options.append("E")
solver.pop()

# Output results
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")