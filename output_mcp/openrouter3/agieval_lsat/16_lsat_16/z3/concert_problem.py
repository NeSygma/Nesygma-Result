from z3 import *

# Create solver
solver = Solver()

# Define compositions
compositions = ['F', 'H', 'L', 'O', 'P', 'R', 'S', 'T']
# Create position variables for each composition (1 to 8)
pos = {c: Int(f'pos_{c}') for c in compositions}

# All positions are between 1 and 8
for c in compositions:
    solver.add(pos[c] >= 1, pos[c] <= 8)

# All positions are distinct
solver.add(Distinct([pos[c] for c in compositions]))

# Constraint: S is performed fourth
solver.add(pos['S'] == 4)

# Constraint 1: T is performed either immediately before F or immediately after R
solver.add(Or(pos['T'] + 1 == pos['F'], pos['R'] + 1 == pos['T']))

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

# Now test each multiple choice option
# Each option gives the first three compositions in order
# We need to check if there exists a valid assignment where:
# - The first three positions match the option
# - All constraints are satisfied

# Define options
options = [
    ("A", ["F", "H", "P"]),
    ("B", ["H", "P", "L"]),
    ("C", ["O", "P", "R"]),
    ("D", ["O", "P", "T"]),
    ("E", ["P", "R", "T"])
]

found_options = []

for letter, first_three in options:
    solver.push()
    # Add constraints for this option
    solver.add(pos[first_three[0]] == 1)
    solver.add(pos[first_three[1]] == 2)
    solver.add(pos[first_three[2]] == 3)
    
    if solver.check() == sat:
        found_options.append(letter)
    solver.pop()

# Print results
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")