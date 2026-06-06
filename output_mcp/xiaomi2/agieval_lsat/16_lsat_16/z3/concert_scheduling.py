from z3 import *

solver = Solver()

# Each composition gets a position 1-8
compositions = ['F', 'H', 'L', 'O', 'P', 'R', 'S', 'T']
pos = {c: Int(f'pos_{c}') for c in compositions}

# All positions are between 1 and 8, all distinct
for c in compositions:
    solver.add(pos[c] >= 1, pos[c] <= 8)
solver.add(Distinct([pos[c] for c in compositions]))

# S is performed fourth
solver.add(pos['S'] == 4)

# Constraint 1: T is performed either immediately before F or immediately after R
solver.add(Or(pos['T'] + 1 == pos['F'], pos['R'] + 1 == pos['T']))

# Constraint 2: At least two compositions between F and R
# |F_pos - R_pos| >= 3
solver.add(Or(pos['F'] - pos['R'] >= 3, pos['R'] - pos['F'] >= 3))

# Constraint 3: O is performed either first or fifth
solver.add(Or(pos['O'] == 1, pos['O'] == 5))

# Constraint 4: The eighth composition is either L or H
solver.add(Or(pos['L'] == 8, pos['H'] == 8))

# Constraint 5: P is performed before S
solver.add(pos['P'] < pos['S'])

# Constraint 6: At least one composition between O and S
# |O_pos - S_pos| >= 2
solver.add(Or(pos['O'] - pos['S'] >= 2, pos['S'] - pos['O'] >= 2))

# Since S is at position 4, constraint 6 means O must be at position 1 or position >= 6
# But constraint 3 says O is 1 or 5. With S=4, |O-S|>=2 means O != 5 (|5-4|=1 < 2)
# So O must be 1. Let's let Z3 figure this out.

# Now test each answer choice for positions 1, 2, 3
# (A) F=1, H=2, P=3
# (B) H=1, P=2, L=3
# (C) O=1, P=2, R=3
# (D) O=1, P=2, T=3
# (E) P=1, R=2, T=3

options = {
    "A": And(pos['F'] == 1, pos['H'] == 2, pos['P'] == 3),
    "B": And(pos['H'] == 1, pos['P'] == 2, pos['L'] == 3),
    "C": And(pos['O'] == 1, pos['P'] == 2, pos['R'] == 3),
    "D": And(pos['O'] == 1, pos['P'] == 2, pos['T'] == 3),
    "E": And(pos['P'] == 1, pos['R'] == 2, pos['T'] == 3),
}

found_options = []
for letter, constr in options.items():
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
        m = solver.model()
        print(f"Option {letter} is SAT:")
        for c in compositions:
            print(f"  {c} = {m[pos[c]]}")
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