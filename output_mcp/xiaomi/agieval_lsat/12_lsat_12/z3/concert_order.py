from z3 import *

solver = Solver()

# Eight compositions: F, H, L, O, P, R, S, T
# Positions 1-8 (using Int variables)
F, H, L, O, P, R, S, T = Ints('F H L O P R S T')
comps = [F, H, L, O, P, R, S, T]

# All positions are between 1 and 8
for c in comps:
    solver.add(c >= 1, c <= 8)

# All distinct
solver.add(Distinct(comps))

# Condition 1: T is performed either immediately before F or immediately after R
solver.add(Or(T + 1 == F, R + 1 == T))

# Condition 2: At least two compositions are performed either after F and before R, or after R and before F
# This means |F - R| >= 3 (at least 2 compositions between them)
solver.add(Or(F - R >= 3, R - F >= 3))

# Condition 3: O is performed either first or fifth
solver.add(Or(O == 1, O == 5))

# Condition 4: The eighth composition performed is either L or H
solver.add(Or(L == 8, H == 8))

# Condition 5: P is performed at some time before S
solver.add(P < S)

# Condition 6: At least one composition is performed either after O and before S, or after S and before O
# This means |O - S| >= 2 (at least 1 composition between them)
solver.add(Or(O - S >= 2, S - O >= 2))

# Now test each option
options = {
    "A": [3, 8, 1, 5, 2, 4, 6, 7],  # L=1, P=2, S=3, R=4, O=5, T=6, F=7, H=8
    "B": [4, 7, 8, 1, 3, 6, 5, 2],  # O=1, T=2, P=3, F=4, S=5, H=6, R=7, L=8
    "C": [3, 8, 6, 7, 1, 5, 4, 2],  # P=1, T=2, F=3, S=4, L=5, R=6, O=7, H=8
    "D": [3, 7, 6, 5, 1, 4, 8, 2],  # P=1, T=2, F=3, S=4, O=5, R=6, L=7, H=8
    "E": [2, 7, 6, 5, 3, 4, 8, 1],  # T=1, F=2, P=3, R=4, O=5, L=6, S=7, H=8
}

# Map: F, H, L, O, P, R, S, T
option_letters = ["A", "B", "C", "D", "E"]
option_positions = [
    # A: L, P, S, R, O, T, F, H
    [7, 8, 1, 5, 2, 4, 3, 6],  # F=7, H=8, L=1, O=5, P=2, R=4, S=3, T=6
    # B: O, T, P, F, S, H, R, L
    [4, 6, 8, 1, 3, 7, 5, 2],  # F=4, H=6, L=8, O=1, P=3, R=7, S=5, T=2
    # C: P, T, F, S, L, R, O, H
    [3, 8, 5, 7, 1, 6, 4, 2],  # F=3, H=8, L=5, O=7, P=1, R=6, S=4, T=2
    # D: P, T, F, S, O, R, L, H
    [3, 8, 7, 5, 1, 6, 4, 2],  # F=3, H=8, L=7, O=5, P=1, R=6, S=4, T=2
    # E: T, F, P, R, O, L, S, H
    [2, 8, 6, 5, 3, 4, 7, 1],  # F=2, H=8, L=6, O=5, P=3, R=4, S=7, T=1
]

found_options = []
for i, letter in enumerate(option_letters):
    solver.push()
    pos = option_positions[i]
    solver.add(F == pos[0])
    solver.add(H == pos[1])
    solver.add(L == pos[2])
    solver.add(O == pos[3])
    solver.add(P == pos[4])
    solver.add(R == pos[5])
    solver.add(S == pos[6])
    solver.add(T == pos[7])
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