from z3 import *

# Compositions
comps = ['F', 'H', 'L', 'O', 'P', 'R', 'S', 'T']
pos = {c: Int(f'pos_{c}') for c in comps}

solver = Solver()

# Each position is 1-8
for c in comps:
    solver.add(pos[c] >= 1, pos[c] <= 8)

# All positions are distinct
solver.add(Distinct([pos[c] for c in comps]))

# C1: T is immediately before F OR T is immediately after R
solver.add(Or(pos['T'] + 1 == pos['F'], pos['T'] == pos['R'] + 1))

# C2: At least two compositions between F and R
solver.add(Abs(pos['F'] - pos['R']) >= 3)

# C3: O is 1st or 5th
solver.add(Or(pos['O'] == 1, pos['O'] == 5))

# C4: 8th is L or H
solver.add(Or(pos['L'] == 8, pos['H'] == 8))

# C5: P is before S
solver.add(pos['P'] < pos['S'])

# C6: At least one composition between O and S
solver.add(Abs(pos['O'] - pos['S']) >= 2)

# Question constraint: Exactly two compositions after F but before O
# This phrasing "after F but before O" usually implies F is before O.
# Let's test if pos[O] = pos[F] + 3.
solver.add(pos['O'] == pos['F'] + 3)

# Test options for R's position
options = {
    "A": 1,
    "B": 3,
    "C": 4,
    "D": 6,
    "E": 7
}

found_options = []
for label, r_pos in options.items():
    solver.push()
    solver.add(pos['R'] == r_pos)
    if solver.check() == sat:
        found_options.append(label)
    solver.pop()

print(f"Found options: {found_options}")
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")