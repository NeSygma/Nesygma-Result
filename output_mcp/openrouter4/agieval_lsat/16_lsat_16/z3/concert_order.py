from z3 import *

solver = Solver()

# Compositions
compositions = ['F','H','L','O','P','R','S','T']
pos = {c: Int(f'pos_{c}') for c in compositions}

# Domain: each position is 1..8
for c in compositions:
    solver.add(pos[c] >= 1, pos[c] <= 8)

# All distinct
solver.add(Distinct([pos[c] for c in compositions]))

# Constraint 1: T immediately before F OR T immediately after R
solver.add(Or(pos['T'] == pos['F'] - 1, pos['T'] == pos['R'] + 1))

# Constraint 2: At least two compositions between F and R
# |pos[F] - pos[R]| >= 3
solver.add(Or(pos['F'] >= pos['R'] + 3, pos['R'] >= pos['F'] + 3))

# Constraint 3: O is first or fifth
solver.add(Or(pos['O'] == 1, pos['O'] == 5))

# Constraint 4: Eighth composition is L or H
solver.add(Or(pos['L'] == 8, pos['H'] == 8))

# Constraint 5: P before S
solver.add(pos['P'] < pos['S'])

# Constraint 6: At least one composition between O and S
# |pos[O] - pos[S]| >= 2
solver.add(Or(pos['O'] <= pos['S'] - 2, pos['O'] >= pos['S'] + 2))

# Additional: S is fourth
solver.add(pos['S'] == 4)

# Now check each option
options = {
    "A": [("F",1), ("H",2), ("P",3)],
    "B": [("H",1), ("P",2), ("L",3)],
    "C": [("O",1), ("P",2), ("R",3)],
    "D": [("O",1), ("P",2), ("T",3)],
    "E": [("P",1), ("R",2), ("T",3)]
}

found_options = []

for letter, assignments in options.items():
    solver.push()
    for comp, pos_val in assignments:
        solver.add(pos[comp] == pos_val)
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