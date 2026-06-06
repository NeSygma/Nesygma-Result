from z3 import *

# Define variables for positions of each composition
pos = {c: Int(c) for c in ['F','H','L','O','P','R','S','T']}
solver = Solver()
# Domain 1..8 and all distinct
for c in pos:
    solver.add(pos[c] >= 1, pos[c] <= 8)
solver.add(Distinct([pos[c] for c in pos]))

# Base constraints
# T either immediately before F or immediately after R
solver.add(Or(pos['T'] + 1 == pos['F'], pos['T'] == pos['R'] + 1))
# At least two compositions between F and R
solver.add(Abs(pos['F'] - pos['R']) >= 3)
# O first or fifth
solver.add(Or(pos['O'] == 1, pos['O'] == 5))
# 8th is L or H
solver.add(Or(pos['L'] == 8, pos['H'] == 8))
# P before S
solver.add(pos['P'] < pos['S'])
# At least one composition between O and S
solver.add(Abs(pos['O'] - pos['S']) >= 2)

# Given condition: T fifth, F sixth
solver.add(pos['T'] == 5, pos['F'] == 6)

# Define option constraints for S position
options = {
    "A": Or(pos['S'] == 4, pos['S'] == 7),
    "B": Or(pos['S'] == 3, pos['S'] == 6),
    "C": Or(pos['S'] == 3, pos['S'] == 4),
    "D": Or(pos['S'] == 2, pos['S'] == 7),
    "E": Or(pos['S'] == 1, pos['S'] == 4)
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