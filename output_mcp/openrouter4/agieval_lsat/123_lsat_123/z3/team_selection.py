from z3 import *

# Define boolean variables for each employee
Myers, Ortega, Paine, Schmidt, Thomson, Wong, Yoder, Zayre = Bools('Myers Ortega Paine Schmidt Thomson Wong Yoder Zayre')
employees = [Myers, Ortega, Paine, Schmidt, Thomson, Wong, Yoder, Zayre]

solver = Solver()

# Base constraint: at least 4 employees selected
solver.add(Sum([If(e, 1, 0) for e in employees]) >= 4)

# Constraint: If Myers is on the team, neither Ortega nor Paine can be
solver.add(Implies(Myers, And(Not(Ortega), Not(Paine))))

# Constraint: If Schmidt is on the team, both Paine and Thomson must also be
solver.add(Implies(Schmidt, And(Paine, Thomson)))

# Constraint: If Wong is on the team, both Myers and Yoder must also be
solver.add(Implies(Wong, And(Myers, Yoder)))

# Define the options
options = {
    "A": [Myers, Paine, Schmidt, Thomson],
    "B": [Ortega, Paine, Thomson, Zayre],
    "C": [Paine, Schmidt, Yoder, Zayre],
    "D": [Schmidt, Thomson, Yoder, Zayre],
    "E": [Thomson, Wong, Yoder, Zayre]
}

# For each option, we need to enforce that exactly those employees are selected
# and the rest are not selected.
found_options = []
for letter, selected_list in options.items():
    solver.push()
    # Add constraints that selected employees are True and non-selected are False
    for e in employees:
        if e in selected_list:
            solver.add(e == True)
        else:
            solver.add(e == False)
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