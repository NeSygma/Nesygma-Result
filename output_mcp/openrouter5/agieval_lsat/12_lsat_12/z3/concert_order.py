from z3 import *

# Eight compositions: F, H, L, O, P, R, S, T
# Positions 1 through 8 (first through eighth)
# We'll use Int variables for each composition's position (1-indexed)

F, H, L, O, P, R, S, T = Ints('F H L O P R S T')
compositions = [F, H, L, O, P, R, S, T]
names = ['F', 'H', 'L', 'O', 'P', 'R', 'S', 'T']

solver = Solver()

# Each composition gets a position from 1 to 8
for c in compositions:
    solver.add(c >= 1, c <= 8)

# All positions are distinct (exactly once each)
solver.add(Distinct(compositions))

# Condition 1: T is performed either immediately before F or immediately after R.
# immediately before F: T + 1 == F
# immediately after R: R + 1 == T
solver.add(Or(T + 1 == F, R + 1 == T))

# Condition 2: At least two compositions are performed either after F and before R, or after R and before F.
# Let count_between = number of compositions strictly between F and R.
# We can express: |F - R| - 1 >= 2  => |F - R| >= 3
# Since positions are integers 1..8, |F - R| >= 3 means F - R >= 3 or R - F >= 3
solver.add(Or(F - R >= 3, R - F >= 3))

# Condition 3: O is performed either first or fifth.
solver.add(Or(O == 1, O == 5))

# Condition 4: The eighth composition performed is either L or H.
solver.add(Or(L == 8, H == 8))

# Condition 5: P is performed at some time before S.
solver.add(P < S)

# Condition 6: At least one composition is performed either after O and before S, or after S and before O.
# This means |O - S| >= 2 (at least one composition strictly between them)
solver.add(Or(O - S >= 2, S - O >= 2))

# Now evaluate each option
# Each option gives a specific ordering from first (position 1) to eighth (position 8)
# We'll encode each option as constraints on the positions

options = {
    "A": ['L', 'P', 'S', 'R', 'O', 'T', 'F', 'H'],
    "B": ['O', 'T', 'P', 'F', 'S', 'H', 'R', 'L'],
    "C": ['P', 'T', 'F', 'S', 'L', 'R', 'O', 'H'],
    "D": ['P', 'T', 'F', 'S', 'O', 'R', 'L', 'H'],
    "E": ['T', 'F', 'P', 'R', 'O', 'L', 'S', 'H']
}

# Map name to Z3 variable
var_map = {'F': F, 'H': H, 'L': L, 'O': O, 'P': P, 'R': R, 'S': S, 'T': T}

found_options = []

for letter, order in options.items():
    solver.push()
    # For each position i (1-indexed), the composition at that position must be the given one
    for i, comp_name in enumerate(order, start=1):
        solver.add(var_map[comp_name] == i)
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