from z3 import *
solver = Solver()
# Variables for parking spaces assigned to each employee
R, S, T, V, X, Y = Ints('R S T V X Y')
# Domain constraints: each parking space is between 1 and 6
for var in [R, S, T, V, X, Y]:
    solver.add(var >= 1, var <= 6)
# All distinct parking spaces
solver.add(Distinct([R, S, T, V, X, Y]))
# Base constraints from the problem
solver.add(Y > T)   # Young > Togowa
solver.add(X > S)   # Xu > Souza
solver.add(R > Y)   # Robertson > Young
solver.add(Or(R == 1, R == 2, R == 3, R == 4))  # Robertson in {1,2,3,4}
# Premise: Young > Souza
solver.add(Y > S)
# Option constraints
opt_a_constr = T == 1
opt_b_constr = Y == 2
opt_c_constr = R == 3
opt_d_constr = S == 3
opt_e_constr = V == 4

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