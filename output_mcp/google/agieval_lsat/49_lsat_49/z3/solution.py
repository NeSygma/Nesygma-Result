from z3 import *

# Employees
employees = ['R', 'S', 'T', 'V', 'X', 'Y']
# Variables for parking spaces
vars = {e: Int(e) for e in employees}

solver = Solver()

# Each employee gets one unique space (1-6)
solver.add(Distinct([vars[e] for e in employees]))
for e in employees:
    solver.add(vars[e] >= 1, vars[e] <= 6)

# Rules
solver.add(vars['Y'] > vars['T'])
solver.add(vars['X'] > vars['S'])
solver.add(vars['R'] > vars['Y'])
solver.add(vars['R'] <= 4)

# Condition: Togowa > Souza
solver.add(vars['T'] > vars['S'])

# Options
options = [
    ("A", vars['Y'] == 2),
    ("B", vars['V'] == 5),
    ("C", vars['T'] == 3),
    ("D", vars['S'] == 2),
    ("E", vars['R'] == 3)
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