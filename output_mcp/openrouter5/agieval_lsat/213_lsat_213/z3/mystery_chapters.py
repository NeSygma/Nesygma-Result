from z3 import *

# Seven chapters, seven clues
# We'll model each clue's chapter position as an integer 1..7
clues = ['R', 'S', 'T', 'U', 'W', 'X', 'Z']
pos = {c: Int(f'pos_{c}') for c in clues}

solver = Solver()

# Each clue gets a distinct chapter 1..7
solver.add(Distinct([pos[c] for c in clues]))
for c in clues:
    solver.add(pos[c] >= 1, pos[c] <= 7)

# Constraints:
# 1. T cannot be in chapter 1
solver.add(pos['T'] != 1)

# 2. T must be before W, and exactly two chapters between them
#    So if T is at position p, W is at p+3 (since exactly 2 chapters separate them)
solver.add(pos['W'] == pos['T'] + 3)

# 3. S and Z cannot be adjacent
solver.add(Abs(pos['S'] - pos['Z']) != 1)

# 4. W and X cannot be adjacent
solver.add(Abs(pos['W'] - pos['X']) != 1)

# 5. U and X must be adjacent
solver.add(Abs(pos['U'] - pos['X']) == 1)

# Now evaluate each option
# Each option is a specific ordering from chapter 1 to 7
options = {
    'A': ['S', 'T', 'Z', 'X', 'U', 'W', 'R'],
    'B': ['T', 'X', 'U', 'W', 'S', 'R', 'Z'],
    'C': ['U', 'S', 'X', 'T', 'Z', 'R', 'W'],
    'D': ['X', 'U', 'T', 'Z', 'R', 'W', 'S'],
    'E': ['Z', 'R', 'T', 'U', 'X', 'W', 'S']
}

found_options = []
for letter, order in options.items():
    solver.push()
    # For each chapter i (1-indexed), the clue at that position must be order[i-1]
    for i, clue in enumerate(order, start=1):
        solver.add(pos[clue] == i)
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