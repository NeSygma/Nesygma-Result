from z3 import *

solver = Solver()

# Compositions
comps = ['F', 'H', 'L', 'O', 'P', 'R', 'S', 'T']
pos = {c: Int(f'pos_{c}') for c in comps}

for c in comps:
    solver.add(pos[c] >= 1, pos[c] <= 8)
solver.add(Distinct([pos[c] for c in comps]))

# Constraints
solver.add(Or(pos['T'] == pos['F'] - 1, pos['T'] == pos['R'] + 1))
solver.add(Or(pos['F'] - pos['R'] >= 3, pos['R'] - pos['F'] >= 3))
solver.add(Or(pos['O'] == 1, pos['O'] == 5))
solver.add(Or(pos['L'] == 8, pos['H'] == 8))
solver.add(pos['P'] < pos['S'])
solver.add(Or(pos['O'] - pos['S'] >= 2, pos['S'] - pos['O'] >= 2))

# Question constraints
solver.add(pos['P'] == 3)
solver.add(pos['S'] == 6)

# Find all possible compositions at position 5
possible_at_5 = []
for c in comps:
    solver.push()
    solver.add(pos[c] == 5)
    if solver.check() == sat:
        possible_at_5.append(c)
    solver.pop()

print(f"Possible compositions at position 5: {possible_at_5}")