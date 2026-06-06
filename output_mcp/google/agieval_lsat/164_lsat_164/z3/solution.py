from z3 import *

# Define variables for positions of each accomplice
accomplices = ['P', 'Q', 'R', 'S', 'T', 'V', 'W']
pos = {name: Int(f'pos_{name}') for name in accomplices}

solver = Solver()

# Domain constraints
for name in accomplices:
    solver.add(pos[name] >= 1, pos[name] <= 7)

# All positions are distinct
solver.add(Distinct([pos[name] for name in accomplices]))

# Constraints
solver.add(pos['P'] == 4)
solver.add(pos['T'] == 2)
# Stanton was recruited neither immediately before nor immediately after Tao.
solver.add(Abs(pos['S'] - pos['T']) != 1)
# Quinn was recruited earlier than Rovero.
solver.add(pos['Q'] < pos['R'])
# Villas was recruited immediately before White.
solver.add(pos['W'] == pos['V'] + 1)

# Options
options = [
    ("A", pos['Q'] == 3),
    ("B", pos['R'] == 5),
    ("C", pos['S'] == 6),
    ("D", pos['V'] == 6),
    ("E", pos['W'] == 3)
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