from z3 import *

solver = Solver()

# Positions for each composition (1-8)
F = Int('F')
H = Int('H')
L = Int('L')
O = Int('O')
P = Int('P')
R = Int('R')
S = Int('S')
T = Int('T')

positions = [F, H, L, O, P, R, S, T]

# Each position is between 1 and 8
for p in positions:
    solver.add(p >= 1, p <= 8)

# All different positions
solver.add(Distinct(positions))

# Constraint 1: T is performed either immediately before F or immediately after R
solver.add(Or(T + 1 == F, R + 1 == T))

# Constraint 2: At least two compositions are performed either after F and before R, or after R and before F
# This means |F - R| >= 3 (at least 2 compositions between them)
solver.add(Or(F - R >= 3, R - F >= 3))

# Constraint 3: O is performed either first or fifth
solver.add(Or(O == 1, O == 5))

# Constraint 4: The eighth composition performed is either L or H
solver.add(Or(L == 8, H == 8))

# Constraint 5: P is performed at some time before S
solver.add(P < S)

# Constraint 6: At least one composition is performed either after O and before S, or after S and before O
# This means |O - S| >= 2 (at least 1 composition between them)
solver.add(Or(O - S >= 2, S - O >= 2))

# Additional condition: Exactly two compositions are performed after F but before O
# This means O - F == 3 (F at position x, then 2 compositions, then O at position x+3)
solver.add(O - F == 3)

# Now check each option for R
found_options = []

# Option A: R is first
solver.push()
solver.add(R == 1)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: R is third
solver.push()
solver.add(R == 3)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: R is fourth
solver.push()
solver.add(R == 4)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: R is sixth
solver.push()
solver.add(R == 6)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: R is seventh
solver.push()
solver.add(R == 7)
if solver.check() == sat:
    found_options.append("E")
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

# Also print a sample solution for verification
solver.push()
if solver.check() == sat:
    m = solver.model()
    print("\nSample solution:")
    for p in positions:
        print(f"{p} = {m[p]}")
solver.pop()