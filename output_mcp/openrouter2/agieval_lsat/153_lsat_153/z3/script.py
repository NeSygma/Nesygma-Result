from z3 import *

solver = Solver()

# Variables for each color: assigned rug index 0,1,2 or 3 for unused
rug_F = Int('rug_F')
rug_O = Int('rug_O')
rug_P = Int('rug_P')
rug_T = Int('rug_T')
rug_W = Int('rug_W')
rug_Y = Int('rug_Y')

colors = [rug_F, rug_O, rug_P, rug_T, rug_W, rug_Y]

# Domain constraints
for v in colors:
    solver.add(v >= 0, v <= 3)

# Exactly one color unused
solver.add(Sum([If(v == 3, 1, 0) for v in colors]) == 1)

# Each rug has at least one color
for r in range(3):
    solver.add(Or([v == r for v in colors]))

# F and P together, both used
solver.add(rug_F == rug_P)
solver.add(rug_F != 3)

# Olive rule: if O used, P same rug
solver.add(Implies(rug_O != 3, rug_P == rug_O))

# F and T not together
solver.add(rug_F != rug_T)

# P and T not together
solver.add(rug_P != rug_T)

# P and Y not together
solver.add(rug_P != rug_Y)

# Count of colors per rug
counts = []
for r in range(3):
    cnt = Sum([If(v == r, 1, 0) for v in colors])
    counts.append(cnt)

# White rule: if W used, rug must have at least 3 colors
for r in range(3):
    solver.add(Implies(rug_W == r, counts[r] >= 3))

# Option constraints
opt_a_constr = Sum([If(counts[r] == 1, 1, 0) for r in range(3)]) == 1
opt_b_constr = (rug_W == 3)
opt_c_constr = (rug_Y == 3)
opt_d_constr = Or([And(rug_T == r, rug_W == r) for r in range(3)])
opt_e_constr = Or([And(rug_T == r, rug_Y == r) for r in range(3)])

# Evaluate options
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