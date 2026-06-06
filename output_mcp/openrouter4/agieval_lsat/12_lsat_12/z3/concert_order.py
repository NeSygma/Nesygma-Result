from z3 import *

solver = Solver()

# Compositions
F, H, L, O, P, R, S, T = Ints('F H L O P R S T')
compositions = [F, H, L, O, P, R, S, T]

# Domain: positions 1..8
for comp in compositions:
    solver.add(comp >= 1, comp <= 8)

# All distinct positions
solver.add(Distinct(compositions))

# Constraint 1: T is performed either immediately before F or immediately after R.
solver.add(Or(T + 1 == F, T == R + 1))

# Constraint 2: At least two compositions are performed either after F and before R, or after R and before F.
# Number of compositions between F and R >= 2 => |F - R| >= 3
solver.add(Or(F + 3 <= R, R + 3 <= F))

# Constraint 3: O is performed either first or fifth.
solver.add(Or(O == 1, O == 5))

# Constraint 4: The eighth composition performed is either L or H.
solver.add(Or(L == 8, H == 8))

# Constraint 5: P is performed at some time before S.
solver.add(P < S)

# Constraint 6: At least one composition is performed either after O and before S, or after S and before O.
# Number of compositions between O and S >= 1 => |O - S| >= 2
solver.add(Or(O + 2 <= S, S + 2 <= O))

# Now test each option
# Option A: L, P, S, R, O, T, F, H
opt_a = [L == 1, P == 2, S == 3, R == 4, O == 5, T == 6, F == 7, H == 8]

# Option B: O, T, P, F, S, H, R, L
opt_b = [O == 1, T == 2, P == 3, F == 4, S == 5, H == 6, R == 7, L == 8]

# Option C: P, T, F, S, L, R, O, H
opt_c = [P == 1, T == 2, F == 3, S == 4, L == 5, R == 6, O == 7, H == 8]

# Option D: P, T, F, S, O, R, L, H
opt_d = [P == 1, T == 2, F == 3, S == 4, O == 5, R == 6, L == 7, H == 8]

# Option E: T, F, P, R, O, L, S, H
opt_e = [T == 1, F == 2, P == 3, R == 4, O == 5, L == 6, S == 7, H == 8]

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