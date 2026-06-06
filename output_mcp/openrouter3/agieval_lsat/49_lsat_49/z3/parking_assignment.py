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

# All employees must have distinct parking spaces (1-6)
employees = [Robertson, Souza, Togowa, Vaughn, Xu, Young]
solver.add(Distinct(employees))

# Domain constraints: each parking space is between 1 and 6
for emp in employees:
    solver.add(emp >= 1, emp <= 6)

# Base constraints from problem statement
solver.add(Young > Togowa)  # Young must be higher-numbered than Togowa
solver.add(Xu > Souza)      # Xu must be higher-numbered than Souza
solver.add(Robertson > Young)  # Robertson must be higher-numbered than Young
solver.add(Or([Robertson == 1, Robertson == 2, Robertson == 3, Robertson == 4]))  # Robertson in {1,2,3,4}

# Additional condition from the question: "If Togowa is assigned a higher-numbered parking space than Souza"
# This is the "if" part, so we add it as a base constraint for this scenario
solver.add(Togowa > Souza)

# Define option constraints
opt_a_constr = (Young == 2)
opt_b_constr = (Vaughn == 5)
opt_c_constr = (Togowa == 3)
opt_d_constr = (Souza == 2)
opt_e_constr = (Robertson == 3)

# Test each option using the exact skeleton
found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
    solver.pop()

# Output results
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")