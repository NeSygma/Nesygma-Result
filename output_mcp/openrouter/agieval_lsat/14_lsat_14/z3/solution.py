from z3 import *

# Create solver and variables
solver = Solver()

# Variables for positions of each composition
F = Int('F')
H = Int('H')
L = Int('L')
O = Int('O')
P = Int('P')
R = Int('R')
S = Int('S')
T = Int('T')

comps = [F,H,L,O,P,R,S,T]
# Domain constraints: positions 1..8
for v in comps:
    solver.add(v >= 1, v <= 8)
# All distinct
solver.add(Distinct(comps))

# Base constraints
# 1. T is immediately before F or immediately after R
solver.add(Or(T + 1 == F, T == R + 1))
# 2. At least two compositions between F and R => |F - R| >= 3
solver.add(Or(F - R >= 3, R - F >= 3))
# 3. O is first or fifth
solver.add(Or(O == 1, O == 5))
# 4. Eighth composition is L or H => position 8 occupied by L or H
solver.add(Or(L == 8, H == 8))
# 5. P before S
solver.add(P < S)
# 6. At least one composition between O and S => |O - S| >= 2
solver.add(Or(O - S >= 2, S - O >= 2))

# Given condition: T is fifth and F is sixth
solver.add(T == 5, F == 6)

# Define option constraints for S position
options = [
    ("A", Or(S == 4, S == 7)),
    ("B", Or(S == 3, S == 6)),
    ("C", Or(S == 3, S == 4)),
    ("D", Or(S == 2, S == 7)),
    ("E", Or(S == 1, S == 4))
]

found_options = []
for letter, opt_constr in options:
    solver.push()
    solver.add(opt_constr)
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