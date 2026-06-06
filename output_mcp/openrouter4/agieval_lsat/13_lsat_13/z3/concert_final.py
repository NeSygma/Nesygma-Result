from z3 import *

solver = Solver()

# Variables for positions (1-indexed)
F, H, L, O, P, R, S, T = Ints('F H L O P R S T')
compositions = [F, H, L, O, P, R, S, T]

# Domain constraints: each position between 1 and 8
for c in compositions:
    solver.add(c >= 1, c <= 8)

# All distinct positions
solver.add(Distinct(compositions))

# Condition 1: T is either immediately before F or immediately after R
solver.add(Or(T + 1 == F, R + 1 == T))

# Condition 2: At least two compositions between F and R => |F-R| >= 3
solver.add(Or(F - R >= 3, R - F >= 3))

# Condition 3: O is first or fifth
solver.add(Or(O == 1, O == 5))

# Condition 4: Eighth is L or H
solver.add(Or(L == 8, H == 8))

# Condition 5: P before S
solver.add(P < S)

# Condition 6: At least one composition between O and S => |O-S| >= 2
solver.add(Or(O - S >= 2, S - O >= 2))

# The question: "P CANNOT be performed" - find which position is impossible
# Test each option: if adding P == pos is UNSAT, that position is impossible
found_valid = []  # positions where P CAN be placed
found_invalid = []  # positions where P CANNOT be placed

options = [("A", 2), ("B", 3), ("C", 4), ("D", 6), ("E", 7)]

for letter, pos_val in options:
    solver.push()
    solver.add(P == pos_val)
    if solver.check() == sat:
        found_valid.append(letter)
    else:
        found_invalid.append(letter)
    solver.pop()

# We expect exactly one position where P cannot be placed
if len(found_invalid) == 1:
    print("STATUS: sat")
    print(f"answer:{found_invalid[0]}")
elif len(found_valid) == 4 and len(found_invalid) == 1:
    print("STATUS: sat")
    print(f"answer:{found_invalid[0]}")
else:
    print("STATUS: unsat")
    print(f"Refine: found_valid={found_valid}, found_invalid={found_invalid}")