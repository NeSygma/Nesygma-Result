from z3 import *

solver = Solver()

# Declare variables for each employee's parking space (1-6)
Robertson = Int('Robertson')
Souza = Int('Souza')
Togowa = Int('Togowa')
Vaughn = Int('Vaughn')
Xu = Int('Xu')
Young = Int('Young')

employees = [Robertson, Souza, Togowa, Vaughn, Xu, Young]

# Each employee gets a parking space between 1 and 6
for e in employees:
    solver.add(e >= 1, e <= 6)

# All different parking spaces
solver.add(Distinct(employees))

# Base constraints from the problem
solver.add(Young > Togowa)          # Young must be assigned a higher-numbered parking space than Togowa
solver.add(Xu > Souza)              # Xu must be assigned a higher-numbered parking space than Souza
solver.add(Robertson > Young)       # Robertson must be assigned a higher-numbered parking space than Young
solver.add(Or(Robertson == 1, Robertson == 2, Robertson == 3, Robertson == 4))  # Robertson must be assigned parking space #1, #2, #3, or #4

# Additional condition: Togowa is assigned a higher-numbered parking space than Souza
solver.add(Togowa > Souza)

# Define the options
opt_a = (Young == 2)                # (A) Young is assigned parking space #2
opt_b = (Vaughn == 5)               # (B) Vaughn is assigned parking space #5
opt_c = (Togowa == 3)               # (C) Togowa is assigned parking space #3
opt_d = (Souza == 2)                # (D) Souza is assigned parking space #2
opt_e = (Robertson == 3)            # (E) Robertson is assigned parking space #3

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