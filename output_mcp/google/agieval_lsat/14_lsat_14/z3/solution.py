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
# |pos[F] - pos[R]| - 1 >= 2  => |pos[F] - pos[R]| >= 3
solver.add(Or(pos['F'] - pos['R'] >= 3, pos['R'] - pos['F'] >= 3))

# C3: O is 1st or 5th
solver.add(Or(pos['O'] == 1, pos['O'] == 5))

# C4: 8th is L or H
solver.add(Or(pos['L'] == 8, pos['H'] == 8))

# C5: P is before S
solver.add(pos['P'] < pos['S'])

# C6: At least one composition between O and S
# |pos[O] - pos[S]| - 1 >= 1 => |pos[O] - pos[S]| >= 2
solver.add(Or(pos['O'] - pos['S'] >= 2, pos['S'] - pos['O'] >= 2))

# Question constraints
solver.add(pos['T'] == 5)
solver.add(pos['F'] == 6)

# We want to find which option (X or Y) is NECESSARY.
# This means: (Base Constraints AND T=5 AND F=6 AND Not(S=X OR S=Y)) is UNSAT.

options = [
    ("A", 4, 7),
    ("B", 3, 6),
    ("C", 3, 4),
    ("D", 2, 7),
    ("E", 1, 4)
]

found_options = []
for letter, x, y in options:
    solver.push()
    # Add the negation of the option
    solver.add(Not(Or(pos['S'] == x, pos['S'] == y)))
    
    # If it's unsat, then the option is necessary
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