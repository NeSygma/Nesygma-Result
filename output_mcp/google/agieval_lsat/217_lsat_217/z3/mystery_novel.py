from z3 import *

# Define the clues
clues = ['R', 'S', 'T', 'U', 'W', 'X', 'Z']
pos = {c: Int(f'pos_{c}') for c in clues}

solver = Solver()

# Each clue is in a chapter 1-7
for c in clues:
    solver.add(pos[c] >= 1, pos[c] <= 7)

# Each clue is in a unique chapter
solver.add(Distinct([pos[c] for c in clues]))

# Constraints:
# 1. T cannot be mentioned in chapter 1.
solver.add(pos['T'] != 1)

# 2. T must be mentioned before W, and there must be exactly two chapters separating them.
# W = T + 3
solver.add(pos['W'] == pos['T'] + 3)

# 3. S and Z cannot be mentioned in adjacent chapters.
solver.add(Abs(pos['S'] - pos['Z']) > 1)

# 4. W and X cannot be mentioned in adjacent chapters.
solver.add(Abs(pos['W'] - pos['X']) > 1)

# 5. U and X must be mentioned in adjacent chapters.
solver.add(Abs(pos['U'] - pos['X']) == 1)

# Test each option
options = [
    ("A", pos['R'] == 7),
    ("B", pos['T'] == 5),
    ("C", pos['U'] == 7),
    ("D", pos['W'] == 3),
    ("E", pos['X'] == 6)
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