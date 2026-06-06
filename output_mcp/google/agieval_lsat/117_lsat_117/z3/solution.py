from z3 import *

# Bands
bands = ['U', 'V', 'W', 'X', 'Y', 'Z']
pos = {b: Int(f'pos_{b}') for b in bands}

solver = Solver()

# Domain constraints
for b in bands:
    solver.add(pos[b] >= 1, pos[b] <= 6)

# All bands in distinct slots
solver.add(Distinct([pos[b] for b in bands]))

# General constraints
solver.add(pos['V'] < pos['Z'])
solver.add(pos['W'] < pos['X'])
solver.add(pos['Z'] < pos['X'])
solver.add(pos['U'] >= 4)
solver.add(pos['Y'] <= 3)

# Question-specific constraint
solver.add(pos['Z'] < pos['Y'])

# Test each option for the earliest slot for W
options = [
    ("A", 2),
    ("B", 3),
    ("C", 4),
    ("D", 5),
    ("E", 6)
]

found_options = []
for letter, slot in options:
    solver.push()
    solver.add(pos['W'] == slot)
    if solver.check() == sat:
        found_options.append(letter)
    solver.pop()

# Check if slot 1 is possible (not in options, but good to know)
solver.push()
solver.add(pos['W'] == 1)
if solver.check() == sat:
    print("Slot 1 is possible")
solver.pop()

if len(found_options) > 0:
    # The earliest slot is the one with the smallest number
    # We need to find the smallest slot number that is possible
    # The options are sorted by slot number (2, 3, 4, 5, 6)
    # So the first one in found_options is the answer.
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
else:
    print("STATUS: unsat")