from z3 import *

# Bands
bands = ['U', 'V', 'W', 'X', 'Y', 'Z']
pos = {b: Int(f'pos_{b}') for b in bands}

solver = Solver()

# Domain constraints
for b in bands:
    solver.add(pos[b] >= 1, pos[b] <= 6)

# All bands in distinct slots
solver.add(Distinct([pos[b] for b in bands]))

# Constraints
solver.add(pos['V'] < pos['Z'])
solver.add(pos['W'] < pos['X'])
solver.add(pos['Z'] < pos['X'])
solver.add(pos['U'] >= 4)
solver.add(pos['Y'] <= 3)

# Question condition: Wellspring performs immediately before Xpert
solver.add(pos['W'] == pos['X'] - 1)

# Options
options = [
    ("A", pos['U'] == 5),
    ("B", pos['V'] == 3),
    ("C", pos['W'] == 3),
    ("D", pos['Z'] == 2),
    ("E", pos['Z'] == 4)
]

found_options = []
for letter, constr in options:
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