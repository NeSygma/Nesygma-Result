from z3 import *

solver = Solver()

# Define variables for each employee's parking space
Robertson = Int('Robertson')
Souza = Int('Souza')
Togowa = Int('Togowa')
Vaughn = Int('Vaughn')
Xu = Int('Xu')
Young = Int('Young')

# Domain constraints: each parking space is between 1 and 6
for var in [Robertson, Souza, Togowa, Vaughn, Xu, Young]:
    solver.add(var >= 1, var <= 6)

# All employees must have distinct parking spaces
solver.add(Distinct([Robertson, Souza, Togowa, Vaughn, Xu, Young]))

# Given constraints
solver.add(Young > Togowa)          # Young must be assigned a higher-numbered parking space than Togowa
solver.add(Xu > Souza)              # Xu must be assigned a higher-numbered parking space than Souza
solver.add(Robertson > Young)       # Robertson must be assigned a higher-numbered parking space than Young
solver.add(Robertson <= 4)          # Robertson must be assigned parking space #1, #2, #3, or #4

# Premise for the question: Togowa is assigned a higher-numbered parking space than Souza
solver.add(Togowa > Souza)

# Define option constraints
opt_a_constr = (Young == 2)
opt_b_constr = (Vaughn == 5)
opt_c_constr = (Togowa == 3)
opt_d_constr = (Souza == 2)
opt_e_constr = (Robertson == 3)

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