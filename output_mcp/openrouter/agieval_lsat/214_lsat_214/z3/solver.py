from z3 import *

solver = Solver()
# Declare variables for each clue
R = Int('R')
S = Int('S')
T = Int('T')
U = Int('U')
W = Int('W')
X = Int('X')
Z = Int('Z')
vars = [R, S, T, U, W, X, Z]
# Domain constraints: chapters 1..7
for v in vars:
    solver.add(v >= 1, v <= 7)
# All distinct
solver.add(Distinct(vars))
# Base constraints
solver.add(X == 1)               # X in chapter 1
solver.add(T != 1)               # T not in chapter 1
solver.add(W == T + 3)           # exactly two chapters between T and W, T before W
solver.add(Abs(S - Z) != 1)     # S and Z not adjacent
solver.add(Abs(W - X) != 1)     # W and X not adjacent
solver.add(Abs(U - X) == 1)     # U and X adjacent

# Option constraints
opt_a = (R == 3)   # A: R in chapter 3
opt_b = (R == 7)   # B: R in chapter 7
opt_c = (S == 2)   # C: S in chapter 2
opt_d = (W == 5)   # D: W in chapter 5
opt_e = (Z == 3)   # E: Z in chapter 3

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