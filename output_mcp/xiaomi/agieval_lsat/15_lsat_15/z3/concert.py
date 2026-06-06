from z3 import *

solver = Solver()

# Variables: position of each composition (1..8)
F = Int('F')
H = Int('H')
L = Int('L')
O = Int('O')
P = Int('P')
R = Int('R')
S = Int('S')
T = Int('T')

comps = [F, H, L, O, P, R, S, T]
names = ['F', 'H', 'L', 'O', 'P', 'R', 'S', 'T']

# Each composition is in position 1..8, all distinct
for c in comps:
    solver.add(c >= 1, c <= 8)
solver.add(Distinct(comps))

# Condition 1: T is performed either immediately before F or immediately after R
solver.add(Or(T + 1 == F, R + 1 == T))

# Condition 2: At least two compositions are performed either after F and before R, or after R and before F
# This means |F - R| >= 3 (there are at least 2 compositions between F and R)
solver.add(Or(F - R >= 3, R - F >= 3))

# Condition 3: O is performed either first or fifth
solver.add(Or(O == 1, O == 5))

# Condition 4: The eighth composition performed is either L or H
solver.add(Or(L == 8, H == 8))

# Condition 5: P is performed at some time before S
solver.add(P < S)

# Condition 6: At least one composition is performed either after O and before S, or after S and before O
# This means |O - S| >= 2
solver.add(Or(O - S >= 2, S - O >= 2))

# Additional condition: O is performed immediately after T
solver.add(T + 1 == O)

# Now check each answer option for F's position
# (A) first or second: F == 1 or F == 2
# (B) second or third: F == 2 or F == 3
# (C) fourth or sixth: F == 4 or F == 6
# (D) fourth or seventh: F == 4 or F == 7
# (E) sixth or seventh: F == 6 or F == 7

options = [
    ("A", Or(F == 1, F == 2)),
    ("B", Or(F == 2, F == 3)),
    ("C", Or(F == 4, F == 6)),
    ("D", Or(F == 4, F == 7)),
    ("E", Or(F == 6, F == 7)),
]

found_options = []
for letter, constr in options:
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