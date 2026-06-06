from z3 import *

# Define students
students = ['Juana', 'Kelly', 'Lateefah', 'Mei', 'Olga']
# Team assignment: True = Green, False = Red
isGreen = {s: Bool(f"{s}_green") for s in students}
# Facilitator status
isFac = {s: Bool(f"{s}_fac") for s in students}

solver = Solver()

# Base constraints
# Lateefah assigned to green team
solver.add(isGreen['Lateefah'] == True)
# Olga is a facilitator
solver.add(isFac['Olga'] == True)
# Kelly is not a facilitator
solver.add(isFac['Kelly'] == False)
# Juana different team than Olga
solver.add(isGreen['Juana'] != isGreen['Olga'])
# Team size: one team has 2 members, other has 3 members
num_green = Sum([If(isGreen[s], 1, 0) for s in students])
solver.add(Or(num_green == 2, num_green == 3))
# Exactly one facilitator per team
green_fac = Sum([If(And(isGreen[s], isFac[s]), 1, 0) for s in students])
red_fac = Sum([If(And(Not(isGreen[s]), isFac[s]), 1, 0) for s in students])
solver.add(green_fac == 1)
solver.add(red_fac == 1)
# Additional condition for the question: Lateefah is a facilitator
solver.add(isFac['Lateefah'] == True)

# Define option constraints
opt_constraints = {}
# A: Juana and Kelly both assigned to red team
opt_constraints['A'] = And(isGreen['Juana'] == False, isGreen['Kelly'] == False)
# B: Juana and Mei both assigned to red team
opt_constraints['B'] = And(isGreen['Juana'] == False, isGreen['Mei'] == False)
# C: Lateefah and Olga both assigned to green team
opt_constraints['C'] = And(isGreen['Lateefah'] == True, isGreen['Olga'] == True)
# D: Mei and Olga both assigned to green team
opt_constraints['D'] = And(isGreen['Mei'] == True, isGreen['Olga'] == True)
# E: Mei and Olga both assigned to red team
opt_constraints['E'] = And(isGreen['Mei'] == False, isGreen['Olga'] == False)

found_options = []
for letter, constr in [("A", opt_constraints['A']), ("B", opt_constraints['B']), ("C", opt_constraints['C']), ("D", opt_constraints['D']), ("E", opt_constraints['E'])]:
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