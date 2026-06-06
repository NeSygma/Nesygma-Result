from z3 import *

# Colors: Forest(F), Olive(O), Peach(P), Turquoise(T), White(W), Yellow(Y)
colors = ['F','O','P','T','W','Y']
assign = {c: Int(f'assign_{c}') for c in colors}
solver = Solver()

# Domain: -1 = not used, otherwise rug index 0,1,2
for c in colors:
    solver.add(Or(assign[c] == -1, And(assign[c] >= 0, assign[c] <= 2)))

# Exactly one color not used (since 5 of 6 used)
not_used = [If(assign[c] == -1, 1, 0) for c in colors]
solver.add(Sum(not_used) == 1)

# Each rug has at least one color
for i in range(3):
    cnt = Sum([If(assign[c] == i, 1, 0) for c in colors])
    solver.add(cnt >= 1)

# Rule: White rug must have exactly 3 colors (white + two others)
W_rug = assign['W']
size_W = Sum([If(assign[c] == W_rug, 1, 0) for c in colors])
solver.add(Implies(W_rug != -1, size_W == 3))

# Rule: Olive implies Peach in same rug
solver.add(Implies(assign['O'] != -1, And(assign['P'] != -1, assign['P'] == assign['O']))

# Not together constraints (cannot be in same rug if both used)
solver.add(Or(assign['F'] == -1, assign['T'] == -1, assign['F'] != assign['T']))
solver.add(Or(assign['P'] == -1, assign['T'] == -1, assign['P'] != assign['T']))
solver.add(Or(assign['P'] == -1, assign['Y'] == -1, assign['P'] != assign['Y']))

# Helper: size of each rug
size = [Sum([If(assign[c] == i, 1, 0) for c in colors]) for i in range(3)]

# Option statements
# A: No multicolored rug contains Forest => any rug with Forest has size 1
opt_a_constr = And([Implies(assign['F'] == i, size[i] == 1) for i in range(3)])
# B: No multicolored rug contains Turquoise
opt_b_constr = And([Implies(assign['T'] == i, size[i] == 1) for i in range(3)])
# C: Peach is used
opt_c_constr = assign['P'] != -1
# D: Turquoise is used
opt_d_constr = assign['T'] != -1
# E: Yellow is used
opt_e_constr = assign['Y'] != -1

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