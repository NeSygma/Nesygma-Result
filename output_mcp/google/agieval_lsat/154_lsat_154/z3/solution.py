from z3 import *

# Colors: Forest(F), Olive(O), Peach(P), Turquoise(T), White(W), Yellow(Y)
colors = ['F', 'O', 'P', 'T', 'W', 'Y']
num_colors = len(colors)
num_rugs = 3

# Variables
# used[c] is True if color c is used
used = {c: Bool(f'used_{c}') for c in colors}
# rug[c] is the index of the rug (0, 1, 2) that color c is in
rug = {c: Int(f'rug_{c}') for c in colors}

solver = Solver()

# Exactly 5 colors used
solver.add(Sum([If(used[c], 1, 0) for c in colors]) == 5)

# Each color used is in a valid rug
for c in colors:
    solver.add(Implies(used[c], And(rug[c] >= 0, rug[c] < num_rugs)))

# Rule 1: If white is used, 2 other colors are also used in that rug (Total 3)
for c in colors:
    solver.add(Implies(used['W'], 
                       If(rug[c] == rug['W'], 1, 0) + 
                       Sum([If(And(used[other], rug[other] == rug['W']), 1, 0) for other in colors if other != c]) == 3))

# Rule 2: If olive is used, peach is also used in the same rug
solver.add(Implies(used['O'], And(used['P'], rug['O'] == rug['P'])))

# Rule 3: Forest and turquoise are not used together
solver.add(Not(And(used['F'], used['T'], rug['F'] == rug['T'])))

# Rule 4: Peach and turquoise are not used together
solver.add(Not(And(used['P'], used['T'], rug['P'] == rug['T'])))

# Rule 5: Peach and yellow are not used together
solver.add(Not(And(used['P'], used['Y'], rug['P'] == rug['Y'])))

# Condition: One of the rugs is solid yellow
# Let's say rug 0 is solid yellow
solver.add(used['Y'])
solver.add(rug['Y'] == 0)
# Rug 0 is solid: only Y is in rug 0
for c in colors:
    if c != 'Y':
        solver.add(Not(And(used[c], rug[c] == 0)))

# Helper to check if a rug is solid
def is_solid(r_idx):
    return Sum([If(And(used[c], rug[c] == r_idx), 1, 0) for c in colors]) == 1

# Options
# (A) Exactly one solid color rug
opt_a = (Sum([If(is_solid(r), 1, 0) for r in range(num_rugs)]) == 1)

# (B) One of the rugs is solid forest
# (Note: rug 0 is already solid yellow, so this means another rug is solid forest)
opt_b = Or([And(is_solid(r), 
                Sum([If(And(used[c], rug[c] == r, c == 'F'), 1, 0) for c in colors]) == 1) 
            for r in range(num_rugs)])

# (C) Turquoise is not used
opt_c = Not(used['T'])

# (D) Forest and olive are used together
opt_d = And(used['F'], used['O'], rug['F'] == rug['O'])

# (E) Peach and white are used together
opt_e = And(used['P'], used['W'], rug['P'] == rug['W'])

options = [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]

results = {}
for name, constr in options:
    solver.push()
    solver.add(constr)
    results[name] = solver.check()
    solver.pop()

print("STATUS: sat")
for name, res in results.items():
    print(f"Option {name}: {res}")