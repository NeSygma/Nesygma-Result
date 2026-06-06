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

# White rug must have exactly 3 colors (white + two others)
W_rug = assign['W']
size_W = Sum([If(assign[c] == W_rug, 1, 0) for c in colors])
solver.add(Implies(W_rug != -1, size_W == 3))

# Olive implies Peach in same rug
solver.add(Implies(assign['O'] != -1, assign['P'] == assign['O']))

# Not together constraints (cannot be in same rug if both used)
solver.add(Or(assign['F'] == -1, assign['T'] == -1, assign['F'] != assign['T']))
solver.add(Or(assign['P'] == -1, assign['T'] == -1, assign['P'] != assign['T']))
solver.add(Or(assign['P'] == -1, assign['Y'] == -1, assign['P'] != assign['Y']))

# Helper: size of each rug
size = [Sum([If(assign[c] == i, 1, 0) for c in colors]) for i in range(3)]

# Option constraints (as statements)
opt_a = And([Implies(assign['F'] == i, size[i] == 1) for i in range(3)])  # No multicolored rug contains forest
opt_b = And([Implies(assign['T'] == i, size[i] == 1) for i in range(3)])  # No multicolored rug contains turquoise
opt_c = assign['P'] != -1  # Peach is used
opt_d = assign['T'] != -1  # Turquoise is used
opt_e = assign['Y'] != -1  # Yellow is used

options = [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]
forced = []
for letter, constr in options:
    solver.push()
    # Add negation of the option; if unsat, then option must be true
    solver.add(Not(constr))
    res = solver.check()
    if res == unsat:
        forced.append(letter)
    solver.pop()

if len(forced) == 1:
    print("STATUS: sat")
    print(f"answer:{forced[0]}")
else:
    print("STATUS: unsat")
    print(f"Refine: forced options = {forced}")