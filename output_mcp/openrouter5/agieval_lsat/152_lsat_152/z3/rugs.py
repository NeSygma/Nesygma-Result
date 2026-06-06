from z3 import *

# Six colors: forest, olive, peach, turquoise, white, yellow
# Exactly 5 of the 6 colors are used.
# Each used color is used in exactly one rug.
# Three rugs: rug0, rug1, rug2
# Each rug is either solid (one color) or multicolored.
# If white is used in a rug, two other colors are also used => white cannot be in a solid rug.
# If olive is used in a rug, peach is also used in that rug.
# Forest and turquoise are not used together in a rug.
# Peach and turquoise are not used together in a rug.
# Peach and yellow are not used together in a rug.

# Q: If there are exactly two solid rugs, then the colors of those two rugs CANNOT be ...
# We need to find which pair of colors CANNOT be the two solid rugs.

# We'll model which colors are used, and which rug each used color goes to.
# Let's use Int variables for each color: value = rug index (0,1,2) if used, or -1 if not used.

colors = ['forest', 'olive', 'peach', 'turquoise', 'white', 'yellow']
c = {col: Int(col) for col in colors}

solver = Solver()

# Domain: each color's value is either -1 (unused) or 0,1,2 (rug index)
for col in colors:
    solver.add(Or(c[col] == -1, c[col] == 0, c[col] == 1, c[col] == 2))

# Exactly 5 of the 6 colors are used => exactly one color is unused (value -1)
solver.add(Sum([If(c[col] == -1, 1, 0) for col in colors]) == 1)

# Each used color is used in only one rug (already enforced by single assignment)

# Each rug is either solid or multicolored.
# We need to track which rugs are solid vs multicolored.
# A rug is solid if exactly one color is assigned to it.
# A rug is multicolored if more than one color is assigned to it.

# Count colors per rug
for rug in range(3):
    count_rug = Sum([If(c[col] == rug, 1, 0) for col in colors])
    # A rug can be solid (count=1) or multicolored (count>1)
    # No constraint on the exact count, just that it's at least 1 if any color is used there.
    # But we know exactly 5 colors used across 3 rugs, so each rug has at least 1 color.
    solver.add(count_rug >= 1)

# Rule: In any rug in which white is used, two other colors are also used.
# So if white is in a rug, that rug has at least 3 colors total.
for rug in range(3):
    solver.add(Implies(c['white'] == rug, Sum([If(c[col] == rug, 1, 0) for col in colors]) >= 3))

# Rule: In any rug in which olive is used, peach is also used.
for rug in range(3):
    solver.add(Implies(c['olive'] == rug, c['peach'] == rug))

# Rule: Forest and turquoise are not used together in a rug.
for rug in range(3):
    solver.add(Not(And(c['forest'] == rug, c['turquoise'] == rug)))

# Rule: Peach and turquoise are not used together in a rug.
for rug in range(3):
    solver.add(Not(And(c['peach'] == rug, c['turquoise'] == rug)))

# Rule: Peach and yellow are not used together in a rug.
for rug in range(3):
    solver.add(Not(And(c['peach'] == rug, c['yellow'] == rug)))

# Constraint: exactly two solid rugs.
# A rug is solid if exactly one color is assigned to it.
solid_rugs = [Bool(f'solid_{rug}') for rug in range(3)]
for rug in range(3):
    solver.add(solid_rugs[rug] == (Sum([If(c[col] == rug, 1, 0) for col in colors]) == 1))

solver.add(Sum([If(solid_rugs[rug], 1, 0) for rug in range(3)]) == 2)

# Now evaluate each option: the two solid rugs' colors are the given pair.
# We need to find which pair CANNOT be the two solid rugs.
# So we check if each pair is possible (sat) or impossible (unsat).

# Helper: for a pair of colors (col1, col2), check if they can be the two solid rugs.
# That means: col1 and col2 are each in a solid rug (different rugs), and those are the only solid rugs.

def check_pair(col1, col2):
    solver.push()
    # col1 and col2 must be in different rugs
    solver.add(c[col1] != c[col2])
    # Both must be in solid rugs
    for col in [col1, col2]:
        rug = c[col]
        solver.add(Sum([If(c[other] == rug, 1, 0) for other in colors]) == 1)
    solver.pop()
    return solver.check()

# Actually, let's do it more carefully with push/pop for each option.

options = [
    ("A", "forest", "peach"),
    ("B", "forest", "yellow"),
    ("C", "peach", "turquoise"),
    ("D", "peach", "yellow"),
    ("E", "turquoise", "yellow")
]

found_options = []
for letter, col1, col2 in options:
    solver.push()
    # The two solid rugs have colors col1 and col2
    # They must be in different rugs
    solver.add(c[col1] != c[col2])
    # Each must be in a solid rug (rug has exactly 1 color)
    for col in [col1, col2]:
        rug = c[col]
        solver.add(Sum([If(c[other] == rug, 1, 0) for other in colors]) == 1)
    # The third rug (the one that is not col1's rug and not col2's rug) must be multicolored
    # (has more than 1 color). But this is already enforced by exactly 2 solid rugs.
    
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