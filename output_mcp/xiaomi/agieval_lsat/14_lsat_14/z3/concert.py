from z3 import *

solver = Solver()

# Eight compositions: F, H, L, O, P, R, S, T
# Each gets a position 1-8
F, H, L, O, P, R, S, T = Ints('F H L O P R S T')
positions = [F, H, L, O, P, R, S, T]
names = ['F', 'H', 'L', 'O', 'P', 'R', 'S', 'T']

# Each position is 1-8, all distinct
for p in positions:
    solver.add(p >= 1, p <= 8)
solver.add(Distinct(positions))

# Given: T is performed fifth and F is performed sixth
solver.add(T == 5)
solver.add(F == 6)

# Condition 1: T is performed either immediately before F or immediately after R
# T immediately before F: T + 1 == F
# T immediately after R: R + 1 == T
solver.add(Or(T + 1 == F, R + 1 == T))

# Condition 2: At least two compositions are performed either after F and before R,
# or after R and before F.
# This means |F - R| >= 3 (at least 2 compositions between them)
solver.add(Or(F - R >= 3, R - F >= 3))

# Condition 3: O is performed either first or fifth
solver.add(Or(O == 1, O == 5))

# Condition 4: The eighth composition performed is either L or H
solver.add(Or(L == 8, H == 8))

# Condition 5: P is performed at some time before S
solver.add(P < S)

# Condition 6: At least one composition is performed either after O and before S,
# or after S and before O.
# This means |O - S| >= 2
solver.add(Or(O - S >= 2, S - O >= 2))

# Now check each answer choice for S
# (A) fourth or seventh: S == 4 or S == 7
# (B) third or sixth: S == 3 or S == 6
# (C) third or fourth: S == 3 or S == 4
# (D) second or seventh: S == 2 or S == 7
# (E) first or fourth: S == 1 or S == 4

options = {
    "A": Or(S == 4, S == 7),
    "B": Or(S == 3, S == 6),
    "C": Or(S == 3, S == 4),
    "D": Or(S == 2, S == 7),
    "E": Or(S == 1, S == 4),
}

found_options = []
for letter, constr in options.items():
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