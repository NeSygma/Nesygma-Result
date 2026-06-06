from z3 import *

solver = Solver()

# Declare the compositions as a list of Int variables representing their positions (1 to 8)
# Use a dictionary to map composition names to their positions for clarity
composers = ['F', 'H', 'L', 'O', 'P', 'R', 'S', 'T']
positions = {c: Int(f'pos_{c}') for c in composers}

# Each composition is assigned a unique position from 1 to 8
solver.add(Distinct(list(positions.values())))
for c in composers:
    solver.add(positions[c] >= 1, positions[c] <= 8)

# T is performed either immediately before F or immediately after R
# Case 1: T immediately before F
solver.add(Or(
    positions['T'] + 1 == positions['F'],
    positions['R'] + 1 == positions['T']
))

# At least two compositions are performed either after F and before R, or after R and before F
# This means the absolute difference between F and R positions is at least 3
solver.add(Or(
    And(positions['F'] < positions['R'], positions['R'] - positions['F'] >= 3),
    And(positions['R'] < positions['F'], positions['F'] - positions['R'] >= 3)
))

# O is performed either first or fifth
solver.add(Or(positions['O'] == 1, positions['O'] == 5))

# The eighth composition performed is either L or H
solver.add(Or(positions['L'] == 8, positions['H'] == 8))

# P is performed at some time before S
solver.add(positions['P'] < positions['S'])

# At least one composition is performed either after O and before S, or after S and before O
solver.add(Or(
    And(positions['O'] < positions['S'], positions['S'] - positions['O'] >= 2),
    And(positions['S'] < positions['O'], positions['O'] - positions['S'] >= 2)
))

# Base constraints are set. Now evaluate the multiple-choice options for P's position
found_options = []

# Option A: P is second
solver.push()
solver.add(positions['P'] == 2)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: P is third
solver.push()
solver.add(positions['P'] == 3)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: P is fourth
solver.push()
solver.add(positions['P'] == 4)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: P is sixth
solver.push()
solver.add(positions['P'] == 6)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: P is seventh
solver.push()
solver.add(positions['P'] == 7)
if solver.check() == sat:
    found_options.append("E")
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