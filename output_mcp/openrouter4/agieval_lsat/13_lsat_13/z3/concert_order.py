from z3 import *

solver = Solver()

# Variables for positions (1-indexed)
F, H, L, O, P, R, S, T = Ints('F H L O P R S T')
compositions = [F, H, L, O, P, R, S, T]

# Domain constraints: each position between 1 and 8
for c in compositions:
    solver.add(c >= 1, c <= 8)

# All distinct positions
solver.add(Distinct(compositions))

# Condition 1: T is either immediately before F or immediately after R
# T immediately before F: T + 1 == F
# T immediately after R: R + 1 == T
solver.add(Or(T + 1 == F, R + 1 == T))

# Condition 2: At least two compositions are performed either after F and before R, or after R and before F.
# i.e., |F - R| - 1 >= 2  => |F - R| >= 3
solver.add(Or(F - R >= 3, R - F >= 3))

# Condition 3: O is performed either first or fifth.
solver.add(Or(O == 1, O == 5))

# Condition 4: The eighth composition performed is either L or H.
solver.add(Or(L == 8, H == 8))

# Condition 5: P is performed at some time before S.
solver.add(P < S)

# Condition 6: At least one composition is performed either after O and before S, or after S and before O.
# i.e., |O - S| >= 2
solver.add(Or(O - S >= 2, S - O >= 2))

# Now test each option for P's position
options = [
    ("A", 2),
    ("B", 3),
    ("C", 4),
    ("D", 6),
    ("E", 7)
]

found_options = []
for letter, pos_val in options:
    solver.push()
    solver.add(P == pos_val)
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