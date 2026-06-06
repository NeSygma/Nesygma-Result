from z3 import *

solver = Solver()

# Compositions
comps = ['F', 'H', 'L', 'O', 'P', 'R', 'S', 'T']
pos = {c: Int(f'pos_{c}') for c in comps}

# Positions are 1-8
for c in comps:
    solver.add(pos[c] >= 1, pos[c] <= 8)

# All positions are distinct
solver.add(Distinct([pos[c] for c in comps]))

# C1: T is immediately before F OR T is immediately after R
solver.add(Or(pos['T'] == pos['F'] - 1, pos['T'] == pos['R'] + 1))

# C2: At least two compositions between F and R
# abs(pos[F] - pos[R]) >= 3
solver.add(Or(pos['F'] - pos['R'] >= 3, pos['R'] - pos['F'] >= 3))

# C3: O is 1st or 5th
solver.add(Or(pos['O'] == 1, pos['O'] == 5))

# C4: 8th is L or H
solver.add(Or(pos['L'] == 8, pos['H'] == 8))

# C5: P is before S
solver.add(pos['P'] < pos['S'])

# C6: At least one composition between O and S
# abs(pos[O] - pos[S]) >= 2
solver.add(Or(pos['O'] - pos['S'] >= 2, pos['S'] - pos['O'] >= 2))

# Question constraints
solver.add(pos['P'] == 3)
solver.add(pos['S'] == 6)

# Options for 5th position
# (A) F or H
# (B) F or O
# (C) F or T
# (D) H or L
# (E) O or R

opt_a_constr = Or(pos['F'] == 5, pos['H'] == 5)
opt_b_constr = Or(pos['F'] == 5, pos['O'] == 5)
opt_c_constr = Or(pos['F'] == 5, pos['T'] == 5)
opt_d_constr = Or(pos['H'] == 5, pos['L'] == 5)
opt_e_constr = Or(pos['O'] == 5, pos['R'] == 5)

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