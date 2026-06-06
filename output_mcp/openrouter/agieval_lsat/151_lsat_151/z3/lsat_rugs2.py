from z3 import *

# Colors indices
F, O, P, T, W, Y = range(6)
R = 3

# Bool variables: rug_color[r][c]
rug_color = [[Bool(f"rc_{r}_{c}") for c in range(6)] for r in range(R)]

base = Solver()
# Each color used at most once
for c in range(6):
    base.add(Sum([If(rug_color[r][c], 1, 0) for r in range(R)]) <= 1)
# Exactly five colors used total
used = [Or([rug_color[r][c] for r in range(R)]) for c in range(6)]
base.add(Sum([If(u, 1, 0) for u in used]) == 5)
# Each rug has at least one color
for r in range(R):
    base.add(Sum([If(rug_color[r][c], 1, 0) for c in range(6)]) >= 1)
# Rules per rug
for r in range(R):
    # white rule
    base.add(Implies(rug_color[r][W], Sum([If(rug_color[r][c], 1, 0) for c in range(6)]) == 3))
    # olive implies peach
    base.add(Implies(rug_color[r][O], rug_color[r][P]))
    # forest and turquoise not together
    base.add(Not(And(rug_color[r][F], rug_color[r][T])))
    # peach and turquoise not together
    base.add(Not(And(rug_color[r][P], rug_color[r][T])))
    # peach and yellow not together
    base.add(Not(And(rug_color[r][P], rug_color[r][Y])))
# One rug solid peach
solid_peach = []
for r in range(R):
    solid = And(rug_color[r][P], And([Not(rug_color[r][c]) for c in range(6) if c != P]))
    solid_peach.append(solid)
base.add(Or(solid_peach))

# Helper functions for option constraints
def solid_color(color_idx):
    opts = []
    for r in range(R):
        solid = And(rug_color[r][color_idx], And([Not(rug_color[r][c]) for c in range(6) if c != color_idx]))
        opts.append(solid)
    return Or(opts)

def exists_pair(c1, c2):
    return Or([And(rug_color[r][c1], rug_color[r][c2]) for r in range(R)])

# Option constraints (must be true)
opt_a = solid_color(F)  # solid forest
opt_b = solid_color(T)  # solid turquoise
opt_c = solid_color(Y)  # solid yellow
opt_d = exists_pair(F, W)  # forest and white together
opt_e = exists_pair(W, Y)  # white and yellow together

options = [
    ("A", opt_a),
    ("B", opt_b),
    ("C", opt_c),
    ("D", opt_d),
    ("E", opt_e)
]

forced = []
for letter, constr in options:
    s = Solver()
    s.add(base.assertions())
    # add negation of the option (i.e., option must be false)
    s.add(Not(constr))
    if s.check() == unsat:
        forced.append(letter)

if len(forced) == 1:
    print("STATUS: sat")
    print(f"answer:{forced[0]}")
elif len(forced) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple forced options {forced}")
else:
    print("STATUS: unsat")
    print("Refine: No forced option found")