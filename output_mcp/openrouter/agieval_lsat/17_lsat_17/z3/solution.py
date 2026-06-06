from z3 import *

solver = Solver()
# Declare position variables for each composition
F = Int('F')
H = Int('H')
L = Int('L')
O = Int('O')
P = Int('P')
R = Int('R')
S = Int('S')
T = Int('T')
positions = [F, H, L, O, P, R, S, T]
# Domain constraints
for var in positions:
    solver.add(var >= 1, var <= 8)
# All distinct
solver.add(Distinct(positions))
# Base constraints
# T is immediately before F OR immediately after R
solver.add(Or(T + 1 == F, T == R + 1))
# At least two compositions between F and R => distance >=3
solver.add(Abs(F - R) >= 3)
# O is first or fifth
solver.add(Or(O == 1, O == 5))
# Eighth composition is L or H
solver.add(Or(L == 8, H == 8))
# P before S
solver.add(P < S)
# At least one composition between O and S
solver.add(Abs(O - S) >= 2)
# Given condition: P is third, S is sixth
solver.add(P == 3, S == 6)

# Define option constraints
opt_a = Or(F == 5, H == 5)          # (A) F or H
opt_b = Or(F == 5, O == 5)          # (B) F or O
opt_c = Or(F == 5, T == 5)          # (C) F or T
opt_d = Or(H == 5, L == 5)          # (D) H or L
opt_e = Or(O == 5, R == 5)          # (E) O or R

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