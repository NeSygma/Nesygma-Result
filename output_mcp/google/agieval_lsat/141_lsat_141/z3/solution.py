from z3 import *

# Define members
members = ['G', 'K', 'P', 'S', 'T', 'V']
# pos[m] is the position of member m (1-6)
pos = {m: Int(f'pos_{m}') for m in members}

solver = Solver()

# Each member performs exactly one solo at a unique position 1-6
for m in members:
    solver.add(pos[m] >= 1, pos[m] <= 6)
solver.add(Distinct([pos[m] for m in members]))

# Constraints
# 1. The guitarist does not perform the fourth solo.
solver.add(pos['G'] != 4)

# 2. The percussionist performs a solo at some time before the keyboard player does.
solver.add(pos['P'] < pos['K'])

# 3. The keyboard player performs a solo at some time after the violinist does
solver.add(pos['V'] < pos['K'])

# 4. and at some time before the guitarist does.
solver.add(pos['K'] < pos['G'])

# 5. The saxophonist performs a solo at some time after either the percussionist does or the trumpeter does, but not both.
# XOR(pos[S] > pos[P], pos[S] > pos[T])
solver.add(Xor(pos['S'] > pos['P'], pos['S'] > pos['T']))

# Options to test (which one CAN be true?)
options = [
    ("A", pos['K'] == 1),
    ("B", pos['G'] == 2),
    ("C", pos['G'] < pos['S']),
    ("D", pos['G'] < pos['P']),
    ("E", pos['K'] < pos['S'])
]

found_options = []
for letter, constr in options:
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