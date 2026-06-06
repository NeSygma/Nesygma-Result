from z3 import *

# Houses
houses = ['J', 'K', 'L', 'M', 'N', 'O', 'P']
pos = {h: Int(f'pos_{h}') for h in houses}

solver = Solver()

# Domain constraints
for h in houses:
    solver.add(pos[h] >= 1, pos[h] <= 7)

# All houses shown at different times
solver.add(Distinct([pos[h] for h in houses]))

# Rule 1: J must be shown in the evening (6 or 7)
solver.add(Or(pos['J'] == 6, pos['J'] == 7))

# Rule 2: K cannot be shown in the morning (K > 2)
solver.add(pos['K'] > 2)

# Rule 3: L must be shown after K and before M (K < L < M)
solver.add(pos['K'] < pos['L'])
solver.add(pos['L'] < pos['M'])

# Options
options = {
    "A": pos['K'] > pos['J'],
    "B": pos['L'] > pos['J'],
    "C": pos['P'] > pos['J'],
    "D": And(pos['N'] > pos['M'], pos['O'] > pos['M']),
    "E": And(pos['N'] > pos['K'], pos['P'] > pos['K'])
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