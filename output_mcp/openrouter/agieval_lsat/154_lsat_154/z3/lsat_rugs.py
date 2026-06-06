from z3 import *

# Colors indices
colors = ['F','O','P','T','W','Y']
# Create variables for each color's rug assignment: -1 = unused, 0,1,2 = rug index
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
# Solid yellow condition: yellow rug is solid (only Y)
Y = vars['Y']
solver.add(Y != -1)  # yellow used
# No other color shares rug with Y
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
# Forest and turquoise not together
solver.add(Or(F == -1, T == -1, F != T))
# Peach and turquoise not together
solver.add(Or(P == -1, T == -1, P != T))
# Peach and yellow not together
solver.add(Or(P == -1, Y == -1, P != Y))

# Define option constraints
option_constraints = {}
# A: Exactly one solid color rug (yellow is the only solid)
# Ensure no other rug has count == 1
A_constr = []
for i in range(3):
    # count of colors in rug i
    cnt_i = Sum([If(v == i, 1, 0) for v in vars.values()])
    # If i is not the yellow rug, then cnt_i != 1
    A_constr.append(Or(i == Y, cnt_i != 1))
option_constraints['A'] = And(*A_constr)
# B: One rug is solid forest
# Forest's rug count ==1
F_rug = F
cnt_F = Sum([If(v == F_rug, 1, 0) for v in vars.values()])
option_constraints['B'] = And(F != -1, cnt_F == 1)
# C: Turquoise not used
option_constraints['C'] = T == -1
# D: Forest and olive used together in a rug
option_constraints['D'] = And(F != -1, O != -1, F == O)
# E: Peach and white used together in a rug
cnt_PW = Sum([If(v == P, 1, 0) for v in vars.values()])  # not needed
option_constraints['E'] = And(P != -1, W != -1, P == W)

found_options = []
for letter, constr in [("A", option_constraints["A"]), ("B", option_constraints["B"]), ("C", option_constraints["C"]), ("D", option_constraints["D"]), ("E", option_constraints["E"])]:
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