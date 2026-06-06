from z3 import *

# Define variables
names = ['P', 'Q', 'R', 'S', 'T', 'V', 'W']
pos = {name: Int(f'pos_{name}') for name in names}

solver = Solver()

# Domain constraints
for name in names:
    solver.add(pos[name] >= 1, pos[name] <= 7)

# All positions are distinct
solver.add(Distinct([pos[name] for name in names]))

# Constraint 4: Peters was recruited fourth
solver.add(pos['P'] == 4)

# Constraint 3: Villas was recruited immediately before White
solver.add(pos['W'] == pos['V'] + 1)

# Constraint 2: Quinn was recruited earlier than Rovero
solver.add(pos['Q'] < pos['R'])

# Constraint 1: Stanton was recruited neither immediately before nor immediately after Tao
solver.add(Abs(pos['S'] - pos['T']) > 1)

# Additional conditions for the question:
# W < R and R < T
solver.add(pos['W'] < pos['R'])
solver.add(pos['R'] < pos['T'])

# Options
options = [
    ("A", pos['Q'] == 1),
    ("B", pos['R'] == 3),
    ("C", pos['S'] == 2),
    ("D", pos['T'] == 6),
    ("E", pos['V'] == 6)
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