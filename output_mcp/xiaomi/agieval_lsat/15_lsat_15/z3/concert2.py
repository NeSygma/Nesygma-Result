from z3 import *

# First, let's find ALL possible positions for F given the constraints
# Then see which answer option matches exactly

comps_names = ['F', 'H', 'L', 'O', 'P', 'R', 'S', 'T']

possible_f_positions = set()

for f_pos in range(1, 9):
    solver = Solver()
    
    F = Int('F')
    H = Int('H')
    L = Int('L')
    O = Int('O')
    P = Int('P')
    R = Int('R')
    S = Int('S')
    T = Int('T')
    
    comps = [F, H, L, O, P, R, S, T]
    
    for c in comps:
        solver.add(c >= 1, c <= 8)
    solver.add(Distinct(comps))
    
    # Condition 1: T is performed either immediately before F or immediately after R
    solver.add(Or(T + 1 == F, R + 1 == T))
    
    # Condition 2: At least two compositions are performed either after F and before R, or after R and before F
    solver.add(Or(F - R >= 3, R - F >= 3))
    
    # Condition 3: O is performed either first or fifth
    solver.add(Or(O == 1, O == 5))
    
    # Condition 4: The eighth composition performed is either L or H
    solver.add(Or(L == 8, H == 8))
    
    # Condition 5: P is performed at some time before S
    solver.add(P < S)
    
    # Condition 6: At least one composition is performed either after O and before S, or after S and before O
    solver.add(Or(O - S >= 2, S - O >= 2))
    
    # Additional condition: O is performed immediately after T
    solver.add(T + 1 == O)
    
    # Fix F to this position
    solver.add(F == f_pos)
    
    if solver.check() == sat:
        possible_f_positions.add(f_pos)
        m = solver.model()
        print(f"F={f_pos} is SAT: ", end="")
        for name, var in zip(comps_names, comps):
            print(f"{name}={m[var]}", end=" ")
        print()

print(f"\nPossible positions for F: {sorted(possible_f_positions)}")

# Now check which answer option covers exactly the possible positions
options = {
    "A": {1, 2},
    "B": {2, 3},
    "C": {4, 6},
    "D": {4, 7},
    "E": {6, 7},
}

for letter, positions in options.items():
    if positions == possible_f_positions:
        print(f"\nExact match: Option {letter}")
    elif positions.issubset(possible_f_positions):
        print(f"Option {letter} is a subset of possible positions")
    elif positions.issuperset(possible_f_positions):
        print(f"Option {letter} is a superset of possible positions")
    else:
        print(f"Option {letter} doesn't match")

# The question says "F must be performed either X or Y"
# This means F can ONLY be in those positions
# Find the option that exactly matches possible_f_positions
matching = [letter for letter, positions in options.items() if positions == possible_f_positions]
if len(matching) == 1:
    print(f"\nSTATUS: sat")
    print(f"answer:{matching[0]}")
elif len(matching) > 1:
    print(f"\nSTATUS: unsat")
    print(f"Refine: Multiple matches {matching}")
else:
    # If no exact match, check if any option is a superset that covers all possibilities
    # The answer should be the option whose positions are exactly the possible ones
    print(f"\nSTATUS: unsat")
    print(f"Refine: No exact match. Possible positions: {sorted(possible_f_positions)}")