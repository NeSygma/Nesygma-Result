from z3 import *

solver = Solver()

# Variables for positions of each composition
F, H, L, O, P, R, S, T = Ints('F H L O P R S T')

# All positions between 1 and 8
solver.add(F >= 1, F <= 8)
solver.add(H >= 1, H <= 8)
solver.add(L >= 1, L <= 8)
solver.add(O >= 1, O <= 8)
solver.add(P >= 1, P <= 8)
solver.add(R >= 1, R <= 8)
solver.add(S >= 1, S <= 8)
solver.add(T >= 1, T <= 8)

# All distinct
solver.add(Distinct(F, H, L, O, P, R, S, T))

# Base constraints
# 1. T is performed either immediately before F or immediately after R.
solver.add(Or(T == F - 1, T == R + 1))

# 2. At least two compositions between F and R (exclusive)
solver.add(Abs(F - R) >= 3)

# 3. O is performed either first or fifth.
solver.add(Or(O == 1, O == 5))

# 4. The eighth composition is either L or H.
solver.add(Or(L == 8, H == 8))

# 5. P is performed before S.
solver.add(P < S)

# 6. At least one composition between O and S (exclusive)
solver.add(Abs(O - S) >= 2)

# Additional condition: O is performed immediately after T.
solver.add(O == T + 1)

# Now evaluate each answer choice
found_options = []
for letter, constr in [
    ("A", Or(F == 1, F == 2)),
    ("B", Or(F == 2, F == 3)),
    ("C", Or(F == 4, F == 6)),
    ("D", Or(F == 4, F == 7)),
    ("E", Or(F == 6, F == 7))
]:
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