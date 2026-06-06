from z3 import *

# Employees
employees = ['M', 'O', 'P', 'S', 'T', 'W', 'Y', 'Z']
vars = {e: Bool(e) for e in employees}

solver = Solver()

# Constraints
# 1. If Myers is on the team, neither Ortega nor Paine can be.
solver.add(Implies(vars['M'], And(Not(vars['O']), Not(vars['P']))))
# 2. If Schmidt is on the team, both Paine and Thomson must also be.
solver.add(Implies(vars['S'], And(vars['P'], vars['T'])))
# 3. If Wong is on the team, both Myers and Yoder must also be.
solver.add(Implies(vars['W'], And(vars['M'], vars['Y'])))

# Team size: at least 4
solver.add(Sum([If(vars[e], 1, 0) for e in employees]) >= 4)

# Condition: Yoder is not on the team
solver.add(vars['Y'] == False)

# Check each option
options = {
    'A': 'Z',
    'B': 'T',
    'C': 'P',
    'D': 'O',
    'E': 'M'
}

found_options = []
for letter, emp in options.items():
    solver.push()
    solver.add(vars[emp] == True)
    if solver.check() == sat:
        # This person CAN be on the team
        pass
    else:
        # This person CANNOT be on the team
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