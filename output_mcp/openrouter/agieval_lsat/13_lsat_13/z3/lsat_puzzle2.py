from z3 import *

solver = Solver()
# Variables for positions of each composition (1..8)
comps = ['F','H','L','O','P','R','S','T']
pos = {c: Int(c) for c in comps}
# Domain constraints
for c in comps:
    solver.add(pos[c] >= 1, pos[c] <= 8)
# All distinct
solver.add(Distinct([pos[c] for c in comps]))
# Constraint 1: T either immediately before F or immediately after R
solver.add(Or(pos['T'] == pos['F'] - 1, pos['T'] == pos['R'] + 1))
# Constraint 2: At least two compositions between F and R
solver.add(Abs(pos['F'] - pos['R']) >= 3)
# Constraint 3: O is first or fifth
solver.add(Or(pos['O'] == 1, pos['O'] == 5))
# Constraint 4: 8th composition is L or H
solver.add(Or(pos['L'] == 8, pos['H'] == 8))
# Constraint 5: P before S
solver.add(pos['P'] < pos['S'])
# Constraint 6: At least one composition between O and S
solver.add(Abs(pos['O'] - pos['S']) >= 2)

# Options mapping (position numbers)
option_positions = {
    'A': 2,
    'B': 3,
    'C': 4,
    'D': 6,
    'E': 7,
}
impossible = []
for letter, ppos in option_positions.items():
    solver.push()
    solver.add(pos['P'] == ppos)
    res = solver.check()
    if res == unsat:
        impossible.append(letter)
    solver.pop()

if len(impossible) == 1:
    print("STATUS: sat")
    print(f"answer:{impossible[0]}")
elif len(impossible) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple impossible options {impossible}")
else:
    print("STATUS: unsat")
    print("Refine: No impossible option found")