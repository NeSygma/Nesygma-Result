from z3 import *
solver = Solver()
# Define variables for each employee
Robertson = Int('Robertson')
Souza = Int('Souza')
Togowa = Int('Togowa')
Vaughn = Int('Vaughn')
Xu = Int('Xu')
Young = Int('Young')
# Domain constraints
for var in [Robertson, Souza, Togowa, Vaughn, Xu, Young]:
    solver.add(var >= 1, var <= 6)
# All distinct
solver.add(Distinct([Robertson, Souza, Togowa, Vaughn, Xu, Young]))
# Base rules
solver.add(Young > Togowa)
solver.add(Xu > Souza)
solver.add(Robertson > Young)
solver.add(Robertson <= 4)
# Option constraints
opt_a_constr = And(Young == 1, Souza == 2, Vaughn == 3, Robertson == 4, Togowa == 5, Xu == 6)
opt_b_constr = And(Vaughn == 1, Togowa == 2, Young == 3, Souza == 4, Robertson == 5, Xu == 6)
opt_c_constr = And(Togowa == 1, Young == 2, Xu == 3, Robertson == 4, Souza == 5, Vaughn == 6)
opt_d_constr = And(Togowa == 1, Robertson == 2, Young == 3, Souza == 4, Vaughn == 5, Xu == 6)
opt_e_constr = And(Souza == 1, Togowa == 2, Young == 3, Robertson == 4, Xu == 5, Vaughn == 6)
# Evaluate options
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