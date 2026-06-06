from z3 import *

solver = Solver()
# Declare variables for each clue representing chapter number (1..7)
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
# All clues distinct
solver.add(Distinct(vars))
# Base constraints
solver.add(T != 1)                # T not in chapter 1
solver.add(W == T + 3)            # exactly two chapters between T and W (i.e., W = T+3)
solver.add(Abs(S - Z) != 1)       # S and Z not adjacent
solver.add(Abs(W - X) != 1)       # W and X not adjacent
solver.add(Abs(U - X) == 1)       # U and X adjacent

# Option-specific constraints
opt_a = (R == 7)
opt_b = (T == 5)
opt_c = (U == 7)
opt_d = (W == 3)
opt_e = (X == 6)

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