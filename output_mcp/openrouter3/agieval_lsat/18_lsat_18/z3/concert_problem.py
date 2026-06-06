from z3 import *

# Create solver
solver = Solver()

# Variables for positions of each composition
compositions = ['F', 'H', 'L', 'O', 'P', 'R', 'S', 'T']
pos = {c: Int(f'pos_{c}') for c in compositions}

# Domain constraints: positions 1 to 8, all distinct
for c in compositions:
    solver.add(pos[c] >= 1, pos[c] <= 8)
solver.add(Distinct([pos[c] for c in compositions]))

# Constraint 1: T is performed either immediately before F or immediately after R
solver.add(Or(pos['T'] == pos['F'] - 1, pos['T'] == pos['R'] + 1))

# Constraint 2: At least two compositions between F and R
solver.add(Abs(pos['F'] - pos['R']) >= 3)

# Constraint 3: O is first or fifth
solver.add(Or(pos['O'] == 1, pos['O'] == 5))

# Constraint 4: Eighth composition is L or H
solver.add(Or(pos['L'] == 8, pos['H'] == 8))

# Constraint 5: P before S
solver.add(pos['P'] < pos['S'])

# Constraint 6: At least one composition between O and S
solver.add(Abs(pos['O'] - pos['S']) >= 2)

# Additional condition from question: exactly two compositions after F but before O
# This means pos_O - pos_F = 3 (since exactly two between them)
solver.add(pos['O'] - pos['F'] == 3)

# Now test each answer choice
found_options = []

# Answer choices: A: first (1), B: third (3), C: fourth (4), D: sixth (6), E: seventh (7)
choices = [("A", 1), ("B", 3), ("C", 4), ("D", 6), ("E", 7)]

for letter, r_pos in choices:
    solver.push()
    solver.add(pos['R'] == r_pos)
    if solver.check() == sat:
        found_options.append(letter)
    solver.pop()

# Output results
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")