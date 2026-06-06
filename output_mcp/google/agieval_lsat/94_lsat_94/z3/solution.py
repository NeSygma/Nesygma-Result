from z3 import *

# Houses
houses = ['J', 'K', 'L', 'M', 'N', 'O', 'P']
pos = {h: Int(f'pos_{h}') for h in houses}

solver = Solver()

# Positions are 1 to 7
for h in houses:
    solver.add(pos[h] >= 1, pos[h] <= 7)

# All positions are distinct
solver.add(Distinct([pos[h] for h in houses]))

# Rule 1: J must be shown in the evening (6 or 7)
solver.add(Or(pos['J'] == 6, pos['J'] == 7))

# Rule 2: K cannot be shown in the morning (K must be 3, 4, 5, 6, or 7)
solver.add(pos['K'] >= 3)

# Rule 3: L must be shown after K and before M (K < L < M)
solver.add(pos['K'] < pos['L'])
solver.add(pos['L'] < pos['M'])

# Check each option
options = [
    ("A", ('J', 'K')),
    ("B", ('J', 'M')),
    ("C", ('J', 'O')),
    ("D", ('J', 'P')),
    ("E", ('M', 'P'))
]

found_options = []
for label, (h1, h2) in options:
    solver.push()
    # Add constraint that they ARE consecutive
    solver.add(Or(pos[h1] - pos[h2] == 1, pos[h2] - pos[h1] == 1))
    
    if solver.check() == unsat:
        found_options.append(label)
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