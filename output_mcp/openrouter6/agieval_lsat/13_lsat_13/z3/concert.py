from z3 import *

solver = Solver()

# Define position variables for each composition
F = Int('F')
H = Int('H')
L = Int('L')
O = Int('O')
P = Int('P')
R = Int('R')
S = Int('S')
T = Int('T')

# All positions between 1 and 8
compositions = [F, H, L, O, P, R, S, T]
for comp in compositions:
    solver.add(comp >= 1, comp <= 8)

# All distinct
solver.add(Distinct(compositions))

# Constraint: T is performed either immediately before F or immediately after R
solver.add(Or(T == F - 1, T == R + 1))

# Constraint: At least two compositions between F and R
solver.add(Abs(F - R) >= 3)

# Constraint: O is first or fifth
solver.add(Or(O == 1, O == 5))

# Constraint: eighth composition is L or H
solver.add(Or(L == 8, H == 8))

# Constraint: P before S
solver.add(P < S)

# Constraint: At least one composition between O and S
solver.add(Abs(O - S) >= 2)

# Now test each option for P
options = [
    ("A", 2),  # second
    ("B", 3),  # third
    ("C", 4),  # fourth
    ("D", 6),  # sixth
    ("E", 7),  # seventh
]

found_options = []
for letter, pos in options:
    solver.push()
    solver.add(P == pos)
    if solver.check() == unsat:  # We are looking for impossible positions
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