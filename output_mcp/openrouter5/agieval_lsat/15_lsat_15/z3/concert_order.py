from z3 import *

# Eight compositions: F, H, L, O, P, R, S, T
# Positions 1 through 8 (1-indexed)
compositions = ['F', 'H', 'L', 'O', 'P', 'R', 'S', 'T']
n = 8

# Create position variables: each composition gets a position 1..8
F, H, L, O, P, R, S, T = Ints('F H L O P R S T')

solver = Solver()

# Domain: each position is between 1 and 8
for c in [F, H, L, O, P, R, S, T]:
    solver.add(c >= 1, c <= 8)

# All positions are distinct
solver.add(Distinct([F, H, L, O, P, R, S, T]))

# Constraint 1: T is performed either immediately before F or immediately after R.
# T immediately before F: T + 1 == F
# T immediately after R: R + 1 == T
solver.add(Or(T + 1 == F, R + 1 == T))

# Constraint 2: At least two compositions are performed either after F and before R, or after R and before F.
# |F - R| >= 3  (so at least 2 compositions between them)
solver.add(Or(F + 3 <= R, R + 3 <= F))

# Constraint 3: O is performed either first or fifth.
solver.add(Or(O == 1, O == 5))

# Constraint 4: The eighth composition performed is either L or H.
solver.add(Or(L == 8, H == 8))

# Constraint 5: P is performed at some time before S.
solver.add(P < S)

# Constraint 6: At least one composition is performed either after O and before S, or after S and before O.
# |O - S| >= 2  (at least one composition between them)
solver.add(Or(O + 2 <= S, S + 2 <= O))

# Additional condition from the question: O is performed immediately after T.
# So T + 1 == O
solver.add(T + 1 == O)

# Now evaluate each answer choice.
# Each choice gives two possible positions for F.

options = {
    "A": Or(F == 1, F == 2),
    "B": Or(F == 2, F == 3),
    "C": Or(F == 4, F == 6),
    "D": Or(F == 4, F == 7),
    "E": Or(F == 6, F == 7)
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