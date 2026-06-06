from z3 import *

solver = Solver()

# Compositions: F=0, H=1, L=2, O=3, P=4, R=5, S=6, T=7
composers = [0, 1, 2, 3, 4, 5, 6, 7]

# positions[i] = composer at position i (0-based)
positions = [Int(f'pos_{i}') for i in range(8)]

# Each position must be assigned a unique composer
solver.add(Distinct(positions))
for p in positions:
    solver.add(Or([p == c for c in composers]))

# Condition 1: T (7) is immediately before F (0) or immediately after R (5)
# T immediately before F: exists i such that positions[i] = 7 and positions[i+1] = 0
# T immediately after R: exists i such that positions[i] = 5 and positions[i+1] = 7
solver.add(Or(
    Or([And(positions[i] == 7, positions[i+1] == 0) for i in range(7)]),
    Or([And(positions[i] == 5, positions[i+1] == 7) for i in range(7)])
))

# Condition 2: At least two compositions are performed either after F and before R, or after R and before F
# This means the absolute difference between the positions of F and R must be at least 3
pos_F = Int('pos_F')
pos_R = Int('pos_R')
solver.add(pos_F == positions.index(0))
solver.add(pos_R == positions.index(5))
solver.add(Abs(pos_F - pos_R) >= 3)

# Condition 3: O (3) is performed either first or fifth
solver.add(Or(positions[0] == 3, positions[4] == 3))

# Condition 4: The eighth composition (position 7) is either L (2) or H (1)
solver.add(Or(positions[7] == 2, positions[7] == 1))

# Condition 5: P (4) is performed before S (6)
pos_P = Int('pos_P')
pos_S = Int('pos_S')
solver.add(pos_P == positions.index(4))
solver.add(pos_S == positions.index(6))
solver.add(pos_P < pos_S)

# Condition 6: At least one composition is performed either after O and before S, or after S and before O
pos_O = Int('pos_O')
solver.add(pos_O == positions.index(3))
solver.add(Or(
    And(pos_O < pos_S, pos_S - pos_O >= 2),
    And(pos_S < pos_O, pos_O - pos_S >= 2)
))

# Additional constraints for the specific scenario:
# P is performed third (position 2) and S is performed sixth (position 5)
solver.add(positions[2] == 4)  # P is at position 2
solver.add(positions[5] == 6)  # S is at position 5

# Now, we need to determine the composition performed fifth (position 4)
# We will check which of the options (A) F or H, (B) F or O, (C) F or T, (D) H or L, (E) O or R is valid

# Define the options as constraints on the composition at position 4 (fifth performance)
# Option A: F (0) or H (1)
opt_A = Or(positions[4] == 0, positions[4] == 1)

# Option B: F (0) or O (3)
opt_B = Or(positions[4] == 0, positions[4] == 3)

# Option C: F (0) or T (7)
opt_C = Or(positions[4] == 0, positions[4] == 7)

# Option D: H (1) or L (2)
opt_D = Or(positions[4] == 1, positions[4] == 2)

# Option E: O (3) or R (5)
opt_E = Or(positions[4] == 3, positions[4] == 5)

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