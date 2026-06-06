from z3 import *

# Colors
colors = ['F', 'O', 'P', 'T', 'W', 'Y']
# Rugs
rugs = [0, 1, 2]

solver = Solver()

# Variables
used = {c: Bool(f'used_{c}') for c in colors}
rug = {c: Int(f'rug_{c}') for c in colors}

# Exactly 5 colors used
solver.add(Sum([If(used[c], 1, 0) for c in colors]) == 5)

# Each color used is in a valid rug
for c in colors:
    solver.add(And(rug[c] >= 0, rug[c] <= 2))

# rug_colors[r][c] is True if color c is in rug r
# Use a dictionary or function to map (r, c) to a Bool
rug_colors = {}
for r in rugs:
    for c in colors:
        rug_colors[(r, c)] = Bool(f'rug_{r}_color_{c}')
        solver.add(rug_colors[(r, c)] == And(used[c], rug[c] == r))

# rug_size[r] is the number of colors in rug r
rug_size = [Sum([If(rug_colors[(r, c)], 1, 0) for c in colors]) for r in rugs]

# Rule 1: In any rug in which white is used, two other colors are also used (total 3)
solver.add(Implies(used['W'], Or([And(rug['W'] == r, rug_size[r] == 3) for r in rugs])))

# Rule 2: In any rug in which olive is used, peach is also used
solver.add(Implies(used['O'], And(used['P'], rug['O'] == rug['P'])))

# Rule 3: Forest and turquoise are not used together
solver.add(Not(And(used['F'], used['T'], rug['F'] == rug['T'])))

# Rule 4: Peach and turquoise are not used together
solver.add(Not(And(used['P'], used['T'], rug['P'] == rug['T'])))

# Rule 5: Peach and yellow are not used together
solver.add(Not(And(used['P'], used['Y'], rug['P'] == rug['Y'])))

# Define options
# (A) There are no multicolored rugs in which forest is used.
opt_a_constr = Not(Exists([Int('r')], And(Or([rug['F'] == r for r in rugs]), Or([And(rug['F'] == r, rug_size[r] > 1) for r in rugs]))))
# Simplified: If F is used, the rug it's in must have size 1.
opt_a_constr = Implies(used['F'], Or([And(rug['F'] == r, rug_size[r] == 1) for r in rugs]))

# (B) There are no multicolored rugs in which turquoise is used.
opt_b_constr = Implies(used['T'], Or([And(rug['T'] == r, rug_size[r] == 1) for r in rugs]))

# (C) Peach is used in one of the rugs.
opt_c_constr = used['P']

# (D) Turquoise is used in one of the rugs.
opt_d_constr = used['T']

# (E) Yellow is used in one of the rugs.
opt_e_constr = used['Y']

# We want to find which one MUST be true.
# An option MUST be true if its negation is UNSAT.
found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
    solver.push()
    solver.add(Not(constr))
    if solver.check() == unsat:
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