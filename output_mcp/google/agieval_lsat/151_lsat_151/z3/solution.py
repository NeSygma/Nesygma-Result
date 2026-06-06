from z3 import *

# Colors
colors = ['F', 'O', 'P', 'T', 'W', 'Y']
# Rugs
rugs = [0, 1, 2]

# Variables
used = {c: Bool(f'used_{c}') for c in colors}
rug_of = {c: Int(f'rug_of_{c}') for c in colors}

solver = Solver()

# Exactly 5 colors used
solver.add(Sum([If(used[c], 1, 0) for c in colors]) == 5)

# Each color used is in a rug
for c in colors:
    solver.add(Implies(used[c], And(rug_of[c] >= 0, rug_of[c] <= 2)))

# Rule 1: If W is used, 2 other colors are also used (total 3+ in that rug)
for r in rugs:
    solver.add(Implies(And(used['W'], rug_of['W'] == r), 
                       Sum([If(And(used[c], rug_of[c] == r), 1, 0) for c in colors]) >= 3))

# Rule 2: If O is used, P is also used (in the same rug)
solver.add(Implies(used['O'], And(used['P'], rug_of['O'] == rug_of['P'])))

# Rule 3: Forest and turquoise are not used together
solver.add(Not(And(used['F'], used['T'], rug_of['F'] == rug_of['T'])))

# Rule 4: Peach and turquoise are not used together
solver.add(Not(And(used['P'], used['T'], rug_of['P'] == rug_of['T'])))

# Rule 5: Peach and yellow are not used together
solver.add(Not(And(used['P'], used['Y'], rug_of['P'] == rug_of['Y'])))

# Condition: One of the rugs is solid peach
# Let's define a variable for the rug that is solid peach
solid_peach_rug = Int('solid_peach_rug')
solver.add(And(used['P'], 
               Sum([If(And(used[c], rug_of[c] == solid_peach_rug), 1, 0) for c in colors]) == 1,
               rug_of['P'] == solid_peach_rug))

# Helper for solid rug
def is_solid(r):
    return Sum([If(And(used[c], rug_of[c] == r), 1, 0) for c in colors]) == 1

# Options
# (A) One of the rugs is solid forest.
opt_a = Or([And(is_solid(r), used['F'], rug_of['F'] == r) for r in rugs])
# (B) One of the rugs is solid turquoise.
opt_b = Or([And(is_solid(r), used['T'], rug_of['T'] == r) for r in rugs])
# (C) One of the rugs is solid yellow.
opt_c = Or([And(is_solid(r), used['Y'], rug_of['Y'] == r) for r in rugs])
# (D) Forest and white are used together in a rug.
opt_d = And(used['F'], used['W'], rug_of['F'] == rug_of['W'])
# (E) White and yellow are used together in a rug.
opt_e = And(used['W'], used['Y'], rug_of['W'] == rug_of['Y'])

options = [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]

valid_options = []
for letter, constr in options:
    solver.push()
    solver.add(Not(constr))
    if solver.check() == unsat:
        valid_options.append(letter)
    solver.pop()

if len(valid_options) == 1:
    print("STATUS: sat")
    print(f"answer:{valid_options[0]}")
elif len(valid_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {valid_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")