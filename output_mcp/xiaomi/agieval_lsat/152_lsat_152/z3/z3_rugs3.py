from z3 import *

solver = Solver()

# Colors: forest=0, olive=1, peach=2, turquoise=3, white=4, yellow=5
# Rugs: 0, 1, 2
# rug_color[r][c] = True if color c is used in rug r
rug_color = [[Bool(f"rug_{r}_color_{c}") for c in range(6)] for r in range(3)]

# solid[r] = True if rug r is solid (single color)
solid = [Bool(f"solid_{r}") for r in range(3)]

# Exactly two solid rugs
solver.add(Sum([If(solid[r], 1, 0) for r in range(3)]) == 2)

# Each color used in at most one rug
for c in range(6):
    solver.add(Sum([If(rug_color[r][c], 1, 0) for r in range(3)]) <= 1)

# Exactly 5 colors used total
solver.add(Sum([If(Or([rug_color[r][c] for r in range(3)]), 1, 0) for c in range(6)]) == 5)

# Solid rug: exactly one color; Non-solid rug: at least 2 colors
for r in range(3):
    solver.add(Implies(solid[r], Sum([If(rug_color[r][c], 1, 0) for c in range(6)]) == 1))
    solver.add(Implies(Not(solid[r]), Sum([If(rug_color[r][c], 1, 0) for c in range(6)]) >= 2))

# Rule 1: If white is used in a rug, two other colors are also used (total 3)
for r in range(3):
    solver.add(Implies(rug_color[r][4], Sum([If(rug_color[r][c], 1, 0) for c in range(6)]) == 3))

# Rule 2: If olive is used in a rug, peach is also used
for r in range(3):
    solver.add(Implies(rug_color[r][1], rug_color[r][2]))

# Rule 3: Forest and turquoise not together
for r in range(3):
    solver.add(Not(And(rug_color[r][0], rug_color[r][3])))

# Rule 4: Peach and turquoise not together
for r in range(3):
    solver.add(Not(And(rug_color[r][2], rug_color[r][3])))

# Rule 5: Peach and yellow not together
for r in range(3):
    solver.add(Not(And(rug_color[r][2], rug_color[r][5])))

# Each rug must have at least one color
for r in range(3):
    solver.add(Sum([If(rug_color[r][c], 1, 0) for c in range(6)]) >= 1)

# The question asks: "the colors of those two rugs CANNOT be"
# This means: which pair is IMPOSSIBLE for the two solid rugs?
# We check each option: is it possible? If NOT possible, that's the answer.

def make_opt(color1, color2):
    """Two solid rugs have color1 and color2 respectively."""
    constraints = []
    for r1 in range(3):
        for r2 in range(3):
            if r1 != r2:
                c = []
                c.append(solid[r1])
                c.append(rug_color[r1][color1])
                for cc in range(6):
                    if cc != color1:
                        c.append(Not(rug_color[r1][cc]))
                c.append(solid[r2])
                c.append(rug_color[r2][color2])
                for cc in range(6):
                    if cc != color2:
                        c.append(Not(rug_color[r2][cc]))
                constraints.append(And(c))
    return Or(constraints)

options = [
    ("A", make_opt(0, 2)),  # forest and peach
    ("B", make_opt(0, 5)),  # forest and yellow
    ("C", make_opt(2, 3)),  # peach and turquoise
    ("D", make_opt(2, 5)),  # peach and yellow
    ("E", make_opt(3, 5)),  # turquoise and yellow
]

# The answer is the one that CANNOT happen (unsat when we try it)
impossible_options = []
for letter, constr in options:
    solver.push()
    solver.add(constr)
    result = solver.check()
    if result == unsat:
        impossible_options.append(letter)
    solver.pop()

print(f"Impossible options: {impossible_options}")

if len(impossible_options) == 1:
    print("STATUS: sat")
    print(f"answer:{impossible_options[0]}")
elif len(impossible_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple impossible options found {impossible_options}")
else:
    print("STATUS: unsat")
    print("Refine: No impossible options found")