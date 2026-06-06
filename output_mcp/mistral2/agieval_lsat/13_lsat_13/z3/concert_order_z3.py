from z3 import *

solver = Solver()

# Declare the compositions as a list of Int variables representing their positions (1 to 8)
compositions = [Int(f'pos_{c}') for c in ['F', 'H', 'L', 'O', 'P', 'R', 'S', 'T']]

# Each composition is assigned a unique position from 1 to 8
solver.add(Distinct(compositions))
for c in compositions:
    solver.add(c >= 1, c <= 8)

# T is performed either immediately before F or immediately after R
# Case 1: T immediately before F
solver.add(Or(
    And(
        compositions[compositions.index(Int('pos_T'))] + 1 == compositions[compositions.index(Int('pos_F'))],
        compositions[compositions.index(Int('pos_T'))] == compositions[compositions.index(Int('pos_F'))] - 1
    ),
    And(
        compositions[compositions.index(Int('pos_R'))] + 1 == compositions[compositions.index(Int('pos_T'))],
        compositions[compositions.index(Int('pos_T'))] == compositions[compositions.index(Int('pos_R'))] + 1
    )
))

# At least two compositions are performed either after F and before R, or after R and before F
# This means the absolute difference between F and R positions is at least 3
F_pos = compositions[compositions.index(Int('pos_F'))]
R_pos = compositions[compositions.index(Int('pos_R'))]
solver.add(Or(
    And(F_pos < R_pos, R_pos - F_pos >= 3),
    And(R_pos < F_pos, F_pos - R_pos >= 3)
))

# O is performed either first or fifth
O_pos = compositions[compositions.index(Int('pos_O'))]
solver.add(Or(O_pos == 1, O_pos == 5))

# The eighth composition performed is either L or H
solver.add(Or(
    compositions[compositions.index(Int('pos_L'))] == 8,
    compositions[compositions.index(Int('pos_H'))] == 8
))

# P is performed at some time before S
P_pos = compositions[compositions.index(Int('pos_P'))]
S_pos = compositions[compositions.index(Int('pos_S'))]
solver.add(P_pos < S_pos)

# At least one composition is performed either after O and before S, or after S and before O
solver.add(Or(
    And(O_pos < S_pos, S_pos - O_pos >= 2),
    And(S_pos < O_pos, O_pos - S_pos >= 2)
))

# Base constraints are set. Now evaluate the multiple-choice options for P's position
found_options = []

# Option A: P is second
solver.push()
solver.add(P_pos == 2)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: P is third
solver.push()
solver.add(P_pos == 3)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: P is fourth
solver.push()
solver.add(P_pos == 4)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: P is sixth
solver.push()
solver.add(P_pos == 6)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: P is seventh
solver.push()
solver.add(P_pos == 7)
if solver.check() == sat:
    found_options.append("E")
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