from z3 import *

# Exactly eight compositions: F, H, L, O, P, R, S, T
# Performed exactly once each, consecutively, positions 1-8

# We'll use Int variables representing position (1-8) for each composition
F, H, L, O, P, R, S, T = Ints('F H L O P R S T')
compositions = [F, H, L, O, P, R, S, T]

solver = Solver()

# All positions are from 1 to 8
for c in compositions:
    solver.add(c >= 1, c <= 8)

# All positions are distinct
solver.add(Distinct(compositions))

# Constraint 1: T is performed either immediately before F or immediately after R
# T immediately before F: T + 1 == F
# T immediately after R: R + 1 == T
solver.add(Or(T + 1 == F, R + 1 == T))

# Constraint 2: At least two compositions are performed either after F and before R, or after R and before F.
# This means |F - R| > 2, i.e., |F - R| >= 3
solver.add(Or(F - R >= 3, R - F >= 3))

# Constraint 3: O is performed either first or fifth
solver.add(Or(O == 1, O == 5))

# Constraint 4: The eighth composition is either L or H
solver.add(Or(L == 8, H == 8))

# Constraint 5: P is performed at some time before S
solver.add(P < S)

# Constraint 6: At least one composition is performed either after O and before S, or after S and before O.
# This means O and S are not adjacent, i.e., |O - S| >= 2
solver.add(Or(O - S >= 2, S - O >= 2))

# Now define the specific order for each option
# Each option gives a list from position 1 to 8

# Option A: L, P, S, R, O, T, F, H
# Meaning: L=1, P=2, S=3, R=4, O=5, T=6, F=7, H=8
opt_a_constr = And(L == 1, P == 2, S == 3, R == 4, O == 5, T == 6, F == 7, H == 8)

# Option B: O, T, P, F, S, H, R, L
opt_b_constr = And(O == 1, T == 2, P == 3, F == 4, S == 5, H == 6, R == 7, L == 8)

# Option C: P, T, F, S, L, R, O, H
opt_c_constr = And(P == 1, T == 2, F == 3, S == 4, L == 5, R == 6, O == 7, H == 8)

# Option D: P, T, F, S, O, R, L, H
opt_d_constr = And(P == 1, T == 2, F == 3, S == 4, O == 5, R == 6, L == 7, H == 8)

# Option E: T, F, P, R, O, L, S, H
opt_e_constr = And(T == 1, F == 2, P == 3, R == 4, O == 5, L == 6, S == 7, H == 8)

found_options = []

for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
    solver.push()
    solver.add(constr)
    result = solver.check()
    print(f"Option {letter}: {result}")
    if result == sat:
        found_options.append(letter)
    solver.pop()

print()
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")