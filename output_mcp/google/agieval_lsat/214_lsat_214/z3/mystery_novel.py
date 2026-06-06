from z3 import *

# Define variables for the position of each clue
clues = ['R', 'S', 'T', 'U', 'W', 'X', 'Z']
pos = {c: Int(f'pos_{c}') for c in clues}

solver = Solver()

# Each clue is in a chapter from 1 to 7
for c in clues:
    solver.add(pos[c] >= 1, pos[c] <= 7)

# Each clue is mentioned exactly once
solver.add(Distinct([pos[c] for c in clues]))

# Constraints
# 1. T cannot be mentioned in chapter 1.
solver.add(pos['T'] != 1)

# 2. T must be mentioned before W, and there must be exactly two chapters separating them.
# |pos(T) - pos(W)| = 3, and pos(T) < pos(W)
solver.add(pos['W'] == pos['T'] + 3)

# 3. S and Z cannot be mentioned in adjacent chapters.
solver.add(Abs(pos['S'] - pos['Z']) > 1)

# 4. W and X cannot be mentioned in adjacent chapters.
solver.add(Abs(pos['W'] - pos['X']) > 1)

# 5. U and X must be mentioned in adjacent chapters.
solver.add(Abs(pos['U'] - pos['X']) == 1)

# Question: If X is mentioned in chapter 1
solver.add(pos['X'] == 1)

# Test each option
options = {
    "A": pos['R'] == 3,
    "B": pos['R'] == 7,
    "C": pos['S'] == 2,
    "D": pos['W'] == 5,
    "E": pos['Z'] == 3
}

found_options = []
for letter, constr in options.items():
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