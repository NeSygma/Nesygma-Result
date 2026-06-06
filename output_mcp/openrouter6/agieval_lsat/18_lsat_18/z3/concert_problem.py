from z3 import *

solver = Solver()

# Compositions
compositions = ['F', 'H', 'L', 'O', 'P', 'R', 'S', 'T']
pos = {c: Int(f'pos_{c}') for c in compositions}

# Domain constraints: positions between 1 and 8
for c in compositions:
    solver.add(pos[c] >= 1, pos[c] <= 8)

# All positions distinct
solver.add(Distinct([pos[c] for c in compositions]))

# Condition 2: T is performed either immediately before F or immediately after R
solver.add(Or(pos['T'] == pos['F'] - 1, pos['T'] == pos['R'] + 1))

# Condition 3: At least two compositions between F and R (in either order)
# Compute min and max of F and R
min_FR = If(pos['F'] < pos['R'], pos['F'], pos['R'])
max_FR = If(pos['F'] > pos['R'], pos['F'], pos['R'])
# Count compositions between F and R (excluding F and R)
other_positions = [pos[c] for c in compositions if c not in ['F', 'R']]
count_between_FR = Sum([If(And(p > min_FR, p < max_FR), 1, 0) for p in other_positions])
solver.add(count_between_FR >= 2)

# Condition 4: O is first or fifth
solver.add(Or(pos['O'] == 1, pos['O'] == 5))

# Condition 5: eighth composition is L or H
solver.add(Or(pos['L'] == 8, pos['H'] == 8))

# Condition 6: P before S
solver.add(pos['P'] < pos['S'])

# Condition 7: At least one composition between O and S
min_OS = If(pos['O'] < pos['S'], pos['O'], pos['S'])
max_OS = If(pos['O'] > pos['S'], pos['O'], pos['S'])
other_positions_OS = [pos[c] for c in compositions if c not in ['O', 'S']]
count_between_OS = Sum([If(And(p > min_OS, p < max_OS), 1, 0) for p in other_positions_OS])
solver.add(count_between_OS >= 1)

# Additional condition for the question: exactly two compositions after F but before O
# This implies F before O, and exactly two compositions between them
solver.add(pos['F'] < pos['O'])
min_FO = pos['F']
max_FO = pos['O']
other_positions_FO = [pos[c] for c in compositions if c not in ['F', 'O']]
count_between_FO = Sum([If(And(p > min_FO, p < max_FO), 1, 0) for p in other_positions_FO])
solver.add(count_between_FO == 2)

# Now evaluate multiple choice options
# Options: A: first (1), B: third (3), C: fourth (4), D: sixth (6), E: seventh (7)
found_options = []
for letter, target_pos in [("A", 1), ("B", 3), ("C", 4), ("D", 6), ("E", 7)]:
    solver.push()
    # Check if R can be at this position given the constraints
    solver.add(pos['R'] == target_pos)
    if solver.check() == sat:
        found_options.append(letter)
    solver.pop()

# Determine which position is forced (i.e., only one possible)
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")