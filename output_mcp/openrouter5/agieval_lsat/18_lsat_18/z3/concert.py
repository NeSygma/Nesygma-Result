from z3 import *

# Eight compositions: F, H, L, O, P, R, S, T
# Positions 1 through 8
# We'll use Int variables for each composition's position (1-indexed)

solver = Solver()

F, H, L, O, P, R, S, T = Ints('F H L O P R S T')
compositions = [F, H, L, O, P, R, S, T]
names = ['F', 'H', 'L', 'O', 'P', 'R', 'S', 'T']

# Each position is between 1 and 8
for c in compositions:
    solver.add(c >= 1, c <= 8)

# All positions are distinct
solver.add(Distinct(compositions))

# Condition 1: T is performed either immediately before F or immediately after R.
# immediately before F: T + 1 == F
# immediately after R: R + 1 == T
solver.add(Or(T + 1 == F, R + 1 == T))

# Condition 2: At least two compositions are performed either after F and before R, or after R and before F.
# Let's define: |pos(F) - pos(R)| > 2, and there are at least 2 compositions strictly between them.
# Actually: at least two compositions are performed either after F and before R, or after R and before F.
# This means the number of positions strictly between F and R is >= 2.
# So |F - R| >= 3 (since if they are 3 apart, there are 2 between them)
solver.add(Or(F + 3 <= R, R + 3 <= F))

# Condition 3: O is performed either first or fifth.
solver.add(Or(O == 1, O == 5))

# Condition 4: The eighth composition performed is either L or H.
solver.add(Or(L == 8, H == 8))

# Condition 5: P is performed at some time before S.
solver.add(P < S)

# Condition 6: At least one composition is performed either after O and before S, or after S and before O.
# This means |O - S| >= 2 (at least one composition strictly between them)
solver.add(Or(O + 2 <= S, S + 2 <= O))

# Additional condition from the question: exactly two compositions are performed after F but before O.
# So positions strictly between F and O: O - F - 1 == 2, meaning O = F + 3, and F < O.
solver.add(F < O)
solver.add(O - F - 1 == 2)

# Now we need to determine which position R must be in.
# Let's evaluate each option.

found_options = []

# Option A: R == 1
opt_a = (R == 1)
# Option B: R == 3
opt_b = (R == 3)
# Option C: R == 4
opt_c = (R == 4)
# Option D: R == 6
opt_d = (R == 6)
# Option E: R == 7
opt_e = (R == 7)

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