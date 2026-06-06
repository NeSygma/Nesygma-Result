from z3 import *

solver = Solver()

# Declare the compositions as integers representing their positions (1 to 8)
# We will use a list where the index represents the position (0-based) and the value represents the composition
compositions = [Int(f'pos_{i}') for i in range(8)]

# Each composition is one of F, H, L, O, P, R, S, T
# We will use integers 0-7 to represent these compositions for simplicity
# F=0, H=1, L=2, O=3, P=4, R=5, S=6, T=7
composers = [0, 1, 2, 3, 4, 5, 6, 7]

# Add constraints to ensure all compositions are used exactly once
solver.add(Distinct(compositions))
for c in compositions:
    solver.add(Or([c == comp for comp in composers]))

# Condition 1: T is performed either immediately before F or immediately after R
# T is 7, F is 0, R is 5
# Find the position of T, F, and R
pos_T = compositions.index(7)
pos_F = compositions.index(0)
pos_R = compositions.index(5)

# T is immediately before F: pos_T + 1 == pos_F
# T is immediately after R: pos_R + 1 == pos_T
solver.add(Or(pos_T + 1 == pos_F, pos_R + 1 == pos_T))

# Condition 2: At least two compositions are performed either after F and before R, or after R and before F
# This means the absolute difference between pos_F and pos_R must be at least 3
solver.add(Abs(pos_F - pos_R) >= 3)

# Condition 3: O is performed either first or fifth
# O is 3
pos_O = compositions.index(3)
solver.add(Or(pos_O == 0, pos_O == 4))

# Condition 4: The eighth composition performed is either L or H
# L is 2, H is 1
pos_eighth = compositions[7]
solver.add(Or(pos_eighth == 2, pos_eighth == 1))

# Condition 5: P is performed at some time before S
# P is 4, S is 6
pos_P = compositions.index(4)
pos_S = compositions.index(6)
solver.add(pos_P < pos_S)

# Condition 6: At least one composition is performed either after O and before S, or after S and before O
# This means the absolute difference between pos_O and pos_S must be at least 2
solver.add(Abs(pos_O - pos_S) >= 2)

# Additional constraints for the specific scenario:
# P is performed third and S is performed sixth
solver.add(pos_P == 2)  # Third position (0-based index 2)
solver.add(pos_S == 5)  # Sixth position (0-based index 5)

# Now, we need to determine the composition performed fifth (0-based index 4)
# We will check which of the options (A) F or H, (B) F or O, (C) F or T, (D) H or L, (E) O or R is valid

# Define the options as constraints on the composition at position 4 (fifth performance)
# Option A: F (0) or H (1)
opt_A = Or(compositions[4] == 0, compositions[4] == 1)

# Option B: F (0) or O (3)
opt_B = Or(compositions[4] == 0, compositions[4] == 3)

# Option C: F (0) or T (7)
opt_C = Or(compositions[4] == 0, compositions[4] == 7)

# Option D: H (1) or L (2)
opt_D = Or(compositions[4] == 1, compositions[4] == 2)

# Option E: O (3) or R (5)
opt_E = Or(compositions[4] == 3, compositions[4] == 5)

# Evaluate each option
found_options = []
for letter, constr in [("A", opt_A), ("B", opt_B), ("C", opt_C), ("D", opt_D), ("E", opt_E)]:
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