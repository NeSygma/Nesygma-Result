from z3 import *

solver = Solver()

# Variables for positions of each clue (1..7)
R = Int('R')
S = Int('S')
T = Int('T')
U = Int('U')
W = Int('W')
X = Int('X')
Z = Int('Z')

vars = [R, S, T, U, W, X, Z]

# Domain constraints
for v in vars:
    solver.add(v >= 1, v <= 7)

# All distinct
solver.add(Distinct(vars))

# Base constraints
solver.add(T != 1)                # T not in chapter 1
solver.add(W == T + 3)            # exactly two chapters between T and W
solver.add(Abs(S - Z) != 1)       # S and Z not adjacent
solver.add(Abs(W - X) != 1)       # W and X not adjacent
solver.add(Abs(U - X) == 1)       # U and X adjacent
solver.add(U == 3)                # Given condition

# Option constraints
opt_a_constr = (R == 1)
opt_b_constr = (R == 5)
opt_c_constr = (S == 7)
opt_d_constr = (W == 6)
opt_e_constr = (X == 4)

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