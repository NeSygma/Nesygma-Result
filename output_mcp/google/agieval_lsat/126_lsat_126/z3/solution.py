from z3 import *

# Employees
employees = ['M', 'O', 'P', 'S', 'T', 'W', 'Y', 'Z']
vars = {e: Bool(e) for e in employees}

solver = Solver()

# Constraint 1: If Myers is on the team, neither Ortega nor Paine can be.
solver.add(Implies(vars['M'], And(Not(vars['O']), Not(vars['P']))))

# Constraint 2: If Schmidt is on the team, both Paine and Thomson must also be.
solver.add(Implies(vars['S'], And(vars['P'], vars['T'])))

# Constraint 3: If Wong is on the team, both Myers and Yoder must also be.
solver.add(Implies(vars['W'], And(vars['M'], vars['Y'])))

# Team size: at least four
solver.add(Sum([If(vars[e], 1, 0) for e in employees]) >= 4)

# Condition: Paine is not on the team
solver.add(Not(vars['P']))

# Answer Choices
options = {
    "A": And(Not(vars['M']), Not(vars['O'])),
    "B": And(Not(vars['M']), Not(vars['T'])),
    "C": And(Not(vars['M']), Not(vars['Z'])),
    "D": And(Not(vars['O']), Not(vars['T'])),
    "E": And(Not(vars['O']), Not(vars['Y']))
}

found_options = []
for letter, constr in options.items():
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
    solver.pop()

print(f"Found options: {found_options}")