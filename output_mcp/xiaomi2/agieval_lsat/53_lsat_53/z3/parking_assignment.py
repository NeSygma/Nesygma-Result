from z3 import *

solver = Solver()

# Declare variables for each employee's parking space
Robertson = Int('Robertson')
Souza = Int('Souza')
Togowa = Int('Togowa')
Vaughn = Int('Vaughn')
Xu = Int('Xu')
Young = Int('Young')

employees = [Robertson, Souza, Togowa, Vaughn, Xu, Young]

# Each assigned a space from 1 to 6
for e in employees:
    solver.add(e >= 1, e <= 6)

# All different
solver.add(Distinct(employees))

# Constraints from problem
solver.add(Young > Togowa)        # Young higher than Togowa
solver.add(Xu > Souza)            # Xu higher than Souza
solver.add(Robertson > Young)     # Robertson higher than Young
solver.add(Robertson >= 1, Robertson <= 4)  # Robertson in {1,2,3,4}

# Additional condition: Robertson is assigned parking space #3
solver.add(Robertson == 3)

# Define each option
opt_a = (Souza == 4)
opt_b = (Togowa == 2)
opt_c = (Vaughn == 5)
opt_d = (Xu == 6)
opt_e = (Young == 2)

found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
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