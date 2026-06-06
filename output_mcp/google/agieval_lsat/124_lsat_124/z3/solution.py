from z3 import *

# Employees
employees = ['M', 'O', 'P', 'S', 'T', 'W', 'Y', 'Z']
vars = {e: Bool(e) for e in employees}

# Constraints
solver = Solver()

# 1. If Myers is on the team, neither Ortega nor Paine can be.
solver.add(Implies(vars['M'], And(Not(vars['O']), Not(vars['P']))))

# 2. If Schmidt is on the team, both Paine and Thomson must also be.
solver.add(Implies(vars['S'], And(vars['P'], vars['T'])))

# 3. If Wong is on the team, both Myers and Yoder must also be.
solver.add(Implies(vars['W'], And(vars['M'], vars['Y'])))

# Team size: at least 4
solver.add(Sum([If(vars[e], 1, 0) for e in employees]) >= 4)

# Options
options = [
    ("A", And(vars['M'], vars['T'])),
    ("B", And(vars['O'], vars['Y'])),
    ("C", And(vars['P'], vars['Z'])),
    ("D", And(vars['S'], vars['W'])),
    ("E", And(vars['W'], vars['Y']))
]

found_options = []
for letter, constr in options:
    solver.push()
    solver.add(constr)
    if solver.check() == unsat:
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