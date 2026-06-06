from z3 import *

solver = Solver()

# Variables for each employee's parking space (1-6)
Robertson = Int('Robertson')
Souza = Int('Souza')
Togowa = Int('Togowa')
Vaughn = Int('Vaughn')
Xu = Int('Xu')
Young = Int('Young')

employees = [Robertson, Souza, Togowa, Vaughn, Xu, Young]
names = ['Robertson', 'Souza', 'Togowa', 'Vaughn', 'Xu', 'Young']

# Domain constraints: each space is 1 through 6
for e in employees:
    solver.add(e >= 1, e <= 6)

# All different
solver.add(Distinct(employees))

# Rule 1: Young > Togowa
solver.add(Young > Togowa)

# Rule 2: Xu > Souza
solver.add(Xu > Souza)

# Rule 3: Robertson > Young
solver.add(Robertson > Young)

# Rule 4: Robertson in {1,2,3,4}
solver.add(Robertson >= 1, Robertson <= 4)

# Additional condition for this question: Young > Souza
solver.add(Young > Souza)

# Now evaluate each option
options = [
    ("A", Togowa == 1),
    ("B", Young == 2),
    ("C", Robertson == 3),
    ("D", Souza == 3),
    ("E", Vaughn == 4)
]

found_options = []
for letter, constr in options:
    solver.push()
    solver.add(constr)
    result = solver.check()
    if result == sat:
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