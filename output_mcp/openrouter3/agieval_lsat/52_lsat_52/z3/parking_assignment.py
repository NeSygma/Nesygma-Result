from z3 import *

# Create solver
solver = Solver()

# Declare variables for each employee's parking space (1-6)
Robertson = Int('Robertson')
Souza = Int('Souza')
Togowa = Int('Togowa')
Vaughn = Int('Vaughn')
Xu = Int('Xu')
Young = Int('Young')

employees = [Robertson, Souza, Togowa, Vaughn, Xu, Young]

# Base constraints
# 1. All parking spaces are between 1 and 6
for emp in employees:
    solver.add(emp >= 1, emp <= 6)

# 2. All employees have distinct parking spaces
solver.add(Distinct(employees))

# 3. Young > Togowa
solver.add(Young > Togowa)

# 4. Xu > Souza
solver.add(Xu > Souza)

# 5. Robertson > Young
solver.add(Robertson > Young)

# 6. Robertson must be assigned parking space #1, #2, #3, or #4
solver.add(Or(Robertson == 1, Robertson == 2, Robertson == 3, Robertson == 4))

# Additional condition from question: Young > Souza
solver.add(Young > Souza)

# Define option constraints
opt_a_constr = (Togowa == 1)
opt_b_constr = (Young == 2)
opt_c_constr = (Robertson == 3)
opt_d_constr = (Souza == 3)
opt_e_constr = (Vaughn == 4)

# Test each option using the exact skeleton
found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
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