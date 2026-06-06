from z3 import *

# Colors indices
colors = ['F','O','P','T','W','Y']
vars = {c: Int(f'c_{c}') for c in colors}
solver = Solver()
# Domain constraints
for v in vars.values():
    solver.add(Or(v == -1, v == 0, v == 1, v == 2))
# Exactly five colors used
used_cnt = Sum([If(v != -1, 1, 0) for v in vars.values()])
solver.add(used_cnt == 5)
# Each rug has at least one color
for i in range(3):
    cnt_i = Sum([If(v == i, 1, 0) for v in vars.values()])
    solver.add(cnt_i >= 1)
# Solid yellow condition
Y = vars['Y']
solver.add(Y != -1)
for c, v in vars.items():
    if c == 'Y':
        continue
    solver.add(Or(v != Y, v == -1))
# White rule: if white in rug i then that rug has at least 3 colors
W = vars['W']
for i in range(3):
    cnt_i = Sum([If(v == i, 1, 0) for v in vars.values()])
    solver.add(Implies(W == i, cnt_i >= 3))
# Olive implies peach same rug and both used
O = vars['O']
P = vars['P']
solver.add(Implies(O != -1, And(P != -1, P == O)))
# Not together constraints
F = vars['F']
T = vars['T']
solver.add(Or(F == -1, T == -1, F != T))
solver.add(Or(P == -1, T == -1, P != T))
solver.add(Or(P == -1, Y == -1, P != Y))

# Option constraints
option_constraints = {}
# A: Exactly one solid color rug (yellow is the only solid)
A_constr = []
for i in range(3):
    cnt_i = Sum([If(v == i, 1, 0) for v in vars.values()])
    A_constr.append(Or(i == Y, cnt_i != 1))
option_constraints['A'] = And(*A_constr)
# B: One rug is solid forest
F_rug = F
cnt_F = Sum([If(v == F_rug, 1, 0) for v in vars.values()])
option_constraints['B'] = And(F != -1, cnt_F == 1)
# C: Turquoise not used
option_constraints['C'] = T == -1
# D: Forest and olive used together in a rug
option_constraints['D'] = And(F != -1, O != -1, F == O)
# E: Peach and white used together in a rug
option_constraints['E'] = And(P != -1, W != -1, P == W)

unsat_options = []
for letter, constr in [("A", option_constraints["A"]), ("B", option_constraints["B"]), ("C", option_constraints["C"]), ("D", option_constraints["D"]), ("E", option_constraints["E"])]:
    solver.push()
    solver.add(constr)
    if solver.check() == unsat:
        unsat_options.append(letter)
    solver.pop()

if len(unsat_options) == 1:
    print("STATUS: sat")
    print(f"answer:{unsat_options[0]}")
elif len(unsat_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple unsat options {unsat_options}")
else:
    print("STATUS: unsat")
    print("Refine: No unsat options found")