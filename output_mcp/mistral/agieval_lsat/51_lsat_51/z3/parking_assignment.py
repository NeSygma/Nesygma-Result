from z3 import *

# Declare variables for each employee
robertson = Int('robertson')
souza = Int('souza')
togowa = Int('togowa')
vaughn = Int('vaughn')
xu = Int('xu')
young = Int('young')

solver = Solver()

# Base constraints: all spaces are between 1 and 6 and distinct
solver.add(Distinct(robertson, souza, togowa, vaughn, xu, young))
solver.add(robertson >= 1, robertson <= 6)
solver.add(souza >= 1, souza <= 6)
solver.add(togowa >= 1, togowa <= 6)
solver.add(vaughn >= 1, vaughn <= 6)
solver.add(xu >= 1, xu <= 6)
solver.add(young >= 1, young <= 6)

# Rule constraints
solver.add(young > togowa)
solver.add(xu > souza)
solver.add(robertson > young)
solver.add(robertson <= 4)

# List of employees and their names
employees = [robertson, souza, togowa, vaughn, xu, young]
employee_names = ['robertson', 'souza', 'togowa', 'vaughn', 'xu', 'young']

# For each employee, determine the set of possible spaces
possible_spaces = {}
for e, name in zip(employees, employee_names):
    possible = []
    for s in range(1, 7):
        s_solver = Solver()
        s_solver.add(solver.assertions())
        s_solver.add(e == s)
        if s_solver.check() == sat:
            possible.append(s)
    possible_spaces[name] = possible

# Count how many employees have exactly two possible spaces
count = 0
for name, spaces in possible_spaces.items():
    if len(spaces) == 2:
        count += 1

# Evaluate multiple choice options
found_options = []
for letter, value in [("A", 0), ("B", 2), ("C", 3), ("D", 4), ("E", 5)]:
    if count == value:
        found_options.append(letter)

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")