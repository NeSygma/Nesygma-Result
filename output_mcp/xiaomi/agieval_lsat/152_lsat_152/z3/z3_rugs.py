from z3 import *

solver = Solver()

# Colors: forest=0, olive=1, peach=2, turquoise=3, white=4, yellow=5
# Rugs: 0, 1, 2
# rug_color[r][c] = True if color c is used in rug r
rug_color = [[Bool(f"rug_{r}_color_{c}") for c in range(6)] for r in range(3)]

# Exactly 5 of the 6 colors are used (across all rugs)
# Each color used is used in exactly one rug
# solid[r] = True if rug r is solid (single color)
solid = [Bool(f"solid_{r}") for r in range(3)]

# Exactly two solid rugs
solver.add(Sum([If(solid[r], 1, 0) for r in range(3)]) == 2)

# Each color used in at most one rug
for c in range(6):
    solver.add(Sum([If(rug_color[r][c], 1, 0) for r in range(3)]) <= 1)

# Exactly 5 colors used total
solver.add(Sum([If(Or([rug_color[r][c] for r in range(3)]), 1, 0) for c in range(6)]) == 5)

# Solid rug: exactly one color
for r in range(3):
    solver.add(Implies(solid[r], Sum([If(rug_color[r][c], 1, 0) for c in range(6)]) == 1))
    # Non-solid rug: at least 2 colors
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

# Now test each option: the two solid rugs' colors CANNOT be the given pair
# We check if it's possible for the two solid rugs to have those colors
# If possible (sat), that option is NOT the answer
# If impossible (unsat), that option IS the answer

# Option A: forest and peach
def make_opt_a():
    # Two solid rugs are forest(0) and peach(2)
    # Find which two rugs are solid and assign colors
    constraints = []
    # At least one solid rug has forest, at least one has peach
    constraints.append(Or([And(solid[r], rug_color[r][0]) for r in range(3)]))
    constraints.append(Or([And(solid[r], rug_color[r][2]) for r in range(3)]))
    # The solid rug with forest has only forest
    for r in range(3):
        constraints.append(Implies(And(solid[r], rug_color[r][0]), 
                                   And(rug_color[r][0], *[Not(rug_color[r][c]) for c in range(6) if c != 0])))
        constraints.append(Implies(And(solid[r], rug_color[r][2]), 
                                   And(rug_color[r][2], *[Not(rug_color[r][c]) for c in range(6) if c != 2])))
    return And(constraints)

# Option B: forest and yellow
def make_opt_b():
    constraints = []
    constraints.append(Or([And(solid[r], rug_color[r][0]) for r in range(3)]))
    constraints.append(Or([And(solid[r], rug_color[r][5]) for r in range(3)]))
    for r in range(3):
        constraints.append(Implies(And(solid[r], rug_color[r][0]), 
                                   And(rug_color[r][0], *[Not(rug_color[r][c]) for c in range(6) if c != 0])))
        constraints.append(Implies(And(solid[r], rug_color[r][5]), 
                                   And(rug_color[r][5], *[Not(rug_color[r][c]) for c in range(6) if c != 5])))
    return And(constraints)

# Option C: peach and turquoise
def make_opt_c():
    constraints = []
    constraints.append(Or([And(solid[r], rug_color[r][2]) for r in range(3)]))
    constraints.append(Or([And(solid[r], rug_color[r][3]) for r in range(3)]))
    for r in range(3):
        constraints.append(Implies(And(solid[r], rug_color[r][2]), 
                                   And(rug_color[r][2], *[Not(rug_color[r][c]) for c in range(6) if c != 2])))
        constraints.append(Implies(And(solid[r], rug_color[r][3]), 
                                   And(rug_color[r][3], *[Not(rug_color[r][c]) for c in range(6) if c != 3])))
    return And(constraints)

# Option D: peach and yellow
def make_opt_d():
    constraints = []
    constraints.append(Or([And(solid[r], rug_color[r][2]) for r in range(3)]))
    constraints.append(Or([And(solid[r], rug_color[r][5]) for r in range(3)]))
    for r in range(3):
        constraints.append(Implies(And(solid[r], rug_color[r][2]), 
                                   And(rug_color[r][2], *[Not(rug_color[r][c]) for c in range(6) if c != 2])))
        constraints.append(Implies(And(solid[r], rug_color[r][5]), 
                                   And(rug_color[r][5], *[Not(rug_color[r][c]) for c in range(6) if c != 5])))
    return And(constraints)

# Option E: turquoise and yellow
def make_opt_e():
    constraints = []
    constraints.append(Or([And(solid[r], rug_color[r][3]) for r in range(3)]))
    constraints.append(Or([And(solid[r], rug_color[r][5]) for r in range(3)]))
    for r in range(3):
        constraints.append(Implies(And(solid[r], rug_color[r][3]), 
                                   And(rug_color[r][3], *[Not(rug_color[r][c]) for c in range(6) if c != 3])))
        constraints.append(Implies(And(solid[r], rug_color[r][5]), 
                                   And(rug_color[r][5], *[Not(rug_color[r][c]) for c in range(6) if c != 5])))
    return And(constraints)

options = [
    ("A", make_opt_a()),
    ("B", make_opt_b()),
    ("C", make_opt_c()),
    ("D", make_opt_d()),
    ("E", make_opt_e()),
]

found_options = []
for letter, constr in options:
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