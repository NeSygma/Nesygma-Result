from z3 import *

# Employees
employees = ['M', 'O', 'P', 'S', 'T', 'W', 'Y', 'Z']
e = {name: Bool(name) for name in employees}

solver = Solver()

# Constraints
# 1. If Myers is on the team, neither Ortega nor Paine can be.
solver.add(Implies(e['M'], And(Not(e['O']), Not(e['P']))))

# 2. If Schmidt is on the team, both Paine and Thomson must also be.
solver.add(Implies(e['S'], And(e['P'], e['T'])))

# 3. If Wong is on the team, both Myers and Yoder must also be.
solver.add(Implies(e['W'], And(e['M'], e['Y'])))

# Team size: at least 4
solver.add(Sum([If(e[name], 1, 0) for name in employees]) >= 4)

# Options
options = {
    "A": ['M', 'P', 'S', 'T'],
    "B": ['O', 'P', 'T', 'Z'],
    "C": ['P', 'S', 'Y', 'Z'],
    "D": ['S', 'T', 'Y', 'Z'],
    "E": ['T', 'W', 'Y', 'Z']
}

found_options = []
for label, members in options.items():
    solver.push()
    # Add constraints for the specific option:
    # The listed members must be True, others must be False
    for name in employees:
        if name in members:
            solver.add(e[name] == True)
        else:
            solver.add(e[name] == False)
    
    if solver.check() == sat:
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