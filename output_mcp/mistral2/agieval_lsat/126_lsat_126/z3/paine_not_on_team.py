from z3 import *

# Declare employees as Bool variables
employees = ['Myers', 'Ortega', 'Paine', 'Schmidt', 'Thomson', 'Wong', 'Yoder', 'Zayre']
selected = {e: Bool(f'selected_{e}') for e in employees}

# Base constraints
solver = Solver()

# At least four employees must be selected
solver.add(Sum([If(selected[e], 1, 0) for e in employees]) >= 4)

# Constraints from the problem statement
# 1. If Myers is on the team, neither Ortega nor Paine can be.
solver.add(Implies(selected['Myers'], And(Not(selected['Ortega']), Not(selected['Paine']))))

# 2. If Schmidt is on the team, both Paine and Thomson must also be.
solver.add(Implies(selected['Schmidt'], And(selected['Paine'], selected['Thomson'])))

# 3. If Wong is on the team, both Myers and Yoder must also be.
solver.add(Implies(selected['Wong'], And(selected['Myers'], selected['Yoder'])))

# Additional constraint: Paine is NOT on the team
solver.add(Not(selected['Paine']))

# Evaluate each option
found_options = []

# Option A: Neither Myers nor Ortega is on the team.
solver.push()
solver.add(And(Not(selected['Myers']), Not(selected['Ortega'])))
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: Neither Myers nor Thomson is on the team.
solver.push()
solver.add(And(Not(selected['Myers']), Not(selected['Thomson'])))
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: Neither Myers nor Zayre is on the team.
solver.push()
solver.add(And(Not(selected['Myers']), Not(selected['Zayre'])))
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: Neither Ortega nor Thomson is on the team.
solver.push()
solver.add(And(Not(selected['Ortega']), Not(selected['Thomson'])))
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: Neither Ortega nor Yoder is on the team.
solver.push()
solver.add(And(Not(selected['Ortega']), Not(selected['Yoder'])))
if solver.check() == sat:
    found_options.append("E")
solver.pop()

# Output the result
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")