from z3 import *

solver = Solver()

# Declare variables
R, S, T, V, X, Y = Ints('R S T V X Y')

# Base constraints
solver.add(Distinct([R, S, T, V, X, Y]))
solver.add(Y > T)
solver.add(X > S)
solver.add(R > Y)
solver.add(Or(R == 1, R == 2, R == 3, R == 4))

# Option constraints
opt_a_constr = And(Y == 1, S == 2, V == 3, R == 4, T == 5, X == 6)
opt_b_constr = And(V == 1, T == 2, Y == 3, S == 4, R == 5, X == 6)
opt_c_constr = And(T == 1, Y == 2, X == 3, R == 4, S == 5, V == 6)
opt_d_constr = And(T == 1, R == 2, Y == 3, S == 4, V == 5, X == 6)
opt_e_constr = And(S == 1, T == 2, Y == 3, R == 4, X == 5, V == 6)

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