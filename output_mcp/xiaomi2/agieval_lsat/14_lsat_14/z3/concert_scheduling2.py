from z3 import *

# Find all possible positions for S
possible_s_positions = []

for s_val in range(1, 9):
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
        solver.add(And(c >= 1, c <= 8))
    solver.add(Distinct(comps))
    
    # Given: T=5, F=6
    solver.add(T == 5)
    solver.add(F == 6)
    solver.add(S == s_val)
    
    # Constraint 1: T immediately before F or immediately after R
    solver.add(Or(T + 1 == F, R + 1 == T))
    
    # Constraint 2: At least two compositions between F and R
    solver.add(Or(F - R >= 3, R - F >= 3))
    
    # Constraint 3: O is first or fifth
    solver.add(Or(O == 1, O == 5))
    
    # Constraint 4: 8th is L or H
    solver.add(Or(L == 8, H == 8))
    
    # Constraint 5: P before S
    solver.add(P < S)
    
    # Constraint 6: At least one composition between O and S
    solver.add(Or(S - O >= 2, O - S >= 2))
    
    if solver.check() == sat:
        m = solver.model()
        possible_s_positions.append(s_val)
        print(f"S={s_val} is possible: F={m[F]}, H={m[H]}, L={m[L]}, O={m[O]}, P={m[P]}, R={m[R]}, S={m[S]}, T={m[T]}")
    else:
        print(f"S={s_val} is NOT possible")

print(f"\nAll possible S positions: {possible_s_positions}")

# Now check which answer choice exactly matches
options = {
    "A": [4, 7],
    "B": [3, 6],
    "C": [3, 4],
    "D": [2, 7],
    "E": [1, 4],
}

for letter, positions in options.items():
    if set(positions) == set(possible_s_positions):
        print(f"\nExact match: Option {letter} = {positions}")
    elif set(positions).issubset(set(possible_s_positions)):
        print(f"Option {letter} = {positions} is a subset (not complete)")
    else:
        print(f"Option {letter} = {positions} does not match")

# The answer is the option that exactly covers all possible S positions
matching = [letter for letter, positions in options.items() if set(positions) == set(possible_s_positions)]
if len(matching) == 1:
    print(f"\nSTATUS: sat")
    print(f"answer:{matching[0]}")
elif len(matching) > 1:
    print(f"\nSTATUS: unsat")
    print(f"Refine: Multiple matches {matching}")
else:
    # If no exact match, check which options are subsets (S must be in those positions)
    # Actually, the question says "S must be performed either X or Y"
    # This means S is always one of those two values
    # So we need: possible_s_positions ⊆ answer_positions
    # AND answer_positions ⊆ possible_s_positions (exact match)
    # But if no exact match, find the option where all possible positions are covered
    covering = [letter for letter, positions in options.items() if set(possible_s_positions).issubset(set(positions))]
    if len(covering) == 1:
        print(f"\nSTATUS: sat")
        print(f"answer:{covering[0]}")
    else:
        print(f"\nSTATUS: unsat")
        print(f"Refine: No exact match. Covering options: {covering}")