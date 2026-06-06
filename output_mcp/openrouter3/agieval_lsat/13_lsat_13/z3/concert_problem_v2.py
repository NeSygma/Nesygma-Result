from z3 import *

# Create solver
solver = Solver()

# Define compositions
compositions = ['F', 'H', 'L', 'O', 'P', 'R', 'S', 'T']
# Create position variables for each composition
pos = {c: Int(f'pos_{c}') for c in compositions}

# Domain constraints: each position is between 1 and 8
for c in compositions:
    solver.add(pos[c] >= 1, pos[c] <= 8)

# All positions must be distinct (exactly one composition per position)
solver.add(Distinct([pos[c] for c in compositions]))

# Constraint 1: T is performed either immediately before F or immediately after R
solver.add(Or(pos['T'] == pos['F'] - 1, pos['T'] == pos['R'] + 1))

# Constraint 2: At least two compositions between F and R
solver.add(Or(pos['F'] - pos['R'] >= 3, pos['R'] - pos['F'] >= 3))

# Constraint 3: O is first or fifth
solver.add(Or(pos['O'] == 1, pos['O'] == 5))

# Constraint 4: Eighth composition is L or H
solver.add(Or(pos['L'] == 8, pos['H'] == 8))

# Constraint 5: P before S
solver.add(pos['P'] < pos['S'])

# Constraint 6: At least one composition between O and S
solver.add(Or(pos['O'] - pos['S'] >= 2, pos['S'] - pos['O'] >= 2))

# Now test each option for P's position
# We want to find which position makes the problem UNSAT
# Options: (A) second, (B) third, (C) fourth, (D) sixth, (E) seventh
# Note: positions are 1-indexed, so second=2, third=3, etc.

impossible_options = []
for letter, position in [("A", 2), ("B", 3), ("C", 4), ("D", 6), ("E", 7)]:
    solver.push()
    # Add constraint that P is at this position
    solver.add(pos['P'] == position)
    result = solver.check()
    if result == unsat:
        impossible_options.append(letter)
    solver.pop()

if len(impossible_options) == 1:
    print("STATUS: sat")
    print(f"answer:{impossible_options[0]}")
elif len(impossible_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple impossible options found {impossible_options}")
else:
    print("STATUS: unsat")
    print("Refine: No impossible options found")