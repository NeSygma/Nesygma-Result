from z3 import *

# Colors indices
colors = ['F','O','P','T','W','Y']
F, O, P, T, W, Y = range(6)

# Rugs indices 0,1,2
R = 3

# Bool variables: rug_color[r][c]
rug_color = [[Bool(f"rc_{r}_{c}") for c in range(6)] for r in range(R)]

solver = Solver()

# Each color used at most once
for c in range(6):
    solver.add(Sum([If(rug_color[r][c], 1, 0) for r in range(R)]) <= 1)

# Exactly five colors used total
used = [Or([rug_color[r][c] for r in range(R)]) for c in range(6)]
solver.add(Sum([If(u, 1, 0) for u in used]) == 5)

# Each rug has at least one color
for r in range(R):
    solver.add(Sum([If(rug_color[r][c], 1, 0) for c in range(6)]) >= 1)

# Rules
for r in range(R):
    # If white used, exactly three colors in that rug (white + two others)
    solver.add(Implies(rug_color[r][W], Sum([If(rug_color[r][c], 1, 0) for c in range(6)]) == 3))
    # Olive implies peach in same rug
    solver.add(Implies(rug_color[r][O], rug_color[r][P]))
    # Forest and turquoise not together
    solver.add(Not(And(rug_color[r][F], rug_color[r][T])))
    # Peach and turquoise not together
    solver.add(Not(And(rug_color[r][P], rug_color[r][T])))
    # Peach and yellow not together
    solver.add(Not(And(rug_color[r][P], rug_color[r][Y])))

# One rug is solid peach
solid_peach = []
for r in range(R):
    solid = And(rug_color[r][P], And([Not(rug_color[r][c]) for c in range(6) if c != P]))
    solid_peach.append(solid)
solver.add(Or(solid_peach))

# Helper to build option constraints

def solid_color(color_idx):
    opts = []
    for r in range(R):
        solid = And(rug_color[r][color_idx], And([Not(rug_color[r][c]) for c in range(6) if c != color_idx]))
        opts.append(solid)
    return Or(opts)

def exists_pair(c1, c2):
    opts = []
    for r in range(R):
        opts.append(And(rug_color[r][c1], rug_color[r][c2]))
    return Or(opts)

# Option constraints (must be true)
opt_a_constr = solid_color(F)  # solid forest
opt_b_constr = solid_color(T)  # solid turquoise
opt_c_constr = solid_color(Y)  # solid yellow
opt_d_constr = exists_pair(F, W)  # forest and white together
opt_e_constr = exists_pair(W, Y)  # white and yellow together

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