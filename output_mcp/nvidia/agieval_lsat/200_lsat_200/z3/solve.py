from z3 import *

solver = Solver()

# Declare variables
H = Int('H')
L = Int('L')
M = Int('M')
S = Int('S')
T = Int('T')
V = Int('V')

# Domain constraints
for var in [H, L, M, S, T, V]:
    solver.add(var >= 1, var <= 6)

# AllDifferent
solver.add(Distinct([H, L, M, S, T, V]))

# Base constraints
solver.add(S != 1)
solver.add(Implies(H < L, M < L))
solver.add(S < M)
solver.add(S < V)
solver.add((T < H) != (T < V))

# Options
opt_a_constr = (M == 2)
opt_b_constr = (L == 2)
opt_c_constr = (V == 2)
opt_d_constr = (L == 3)
opt_e_constr = (M == 5)

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