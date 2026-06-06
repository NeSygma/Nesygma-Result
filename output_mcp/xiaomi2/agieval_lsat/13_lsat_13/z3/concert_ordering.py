from z3 import *

# Each composition gets a position (1-8), all distinct
F, H, L, O, P, R, S, T = Ints('F H L O P R S T')
comps = [F, H, L, O, P, R, S, T]

solver = Solver()

# All positions are between 1 and 8
for c in comps:
    solver.add(c >= 1, c <= 8)

# All distinct
solver.add(Distinct(comps))

# Constraint 1: T is performed either immediately before F or immediately after R
solver.add(Or(T + 1 == F, R + 1 == T))

# Constraint 2: At least two compositions between F and R (|F-R| >= 3)
solver.add(Or(F - R >= 3, R - F >= 3))

# Constraint 3: O is performed either first or fifth
solver.add(Or(O == 1, O == 5))

# Constraint 4: The eighth composition is either L or H
solver.add(Or(L == 8, H == 8))

# Constraint 5: P is performed before S
solver.add(P < S)

# Constraint 6: At least one composition between O and S (|O-S| >= 2)
solver.add(Or(O - S >= 2, S - O >= 2))

# Now test each answer choice: which position CANNOT P be at?
# We check if P can be at each position. The one that's UNSAT is the answer.

found_options = []
for letter, pos in [("A", 2), ("B", 3), ("C", 4), ("D", 6), ("E", 7)]:
    solver.push()
    solver.add(P == pos)
    if solver.check() == sat:
        found_options.append(letter)
    solver.pop()

# We want the position P CANNOT be at
# So we look for options that are NOT in found_options (i.e., UNSAT)
cannot_be = [l for l in ["A", "B", "C", "D", "E"] if l not in found_options]

print(f"Positions P CAN be at: {found_options}")
print(f"Positions P CANNOT be at: {cannot_be}")

if len(cannot_be) == 1:
    print("STATUS: sat")
    print(f"answer:{cannot_be[0]}")
elif len(cannot_be) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple impossible positions found {cannot_be}")
else:
    print("STATUS: unsat")
    print("Refine: No impossible positions found")