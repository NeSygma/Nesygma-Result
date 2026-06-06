from z3 import *

# Define the compositions as symbolic constants
F, H, L, O, P, R, S, T = Ints('F H L O P R S T')

# Performance order: perf[0] is first, perf[7] is eighth
perf = [Int(f'perf_{i}') for i in range(8)]

solver = Solver()

# Each composition must appear exactly once in the performance order
solver.add(Distinct(perf))

# All compositions must be used
compositions = [F, H, L, O, P, R, S, T]
solver.add(Distinct(compositions))
for c in compositions:
    solver.add(Or([p == c for p in perf]))

# Constraint: T is immediately before F or immediately after R
# Case 1: T immediately before F (perf[i] = T and perf[i+1] = F)
# Case 2: T immediately after R (perf[i] = R and perf[i+1] = T)
solver.add(Or(
    Or([And(perf[i] == T, perf[i+1] == F) for i in range(7)]),
    Or([And(perf[i] == R, perf[i+1] == T) for i in range(7)])
))

# Constraint: At least two compositions are performed either after F and before R, or after R and before F
# This means the positions of F and R must have at least two compositions between them in either order
# We'll enforce this by ensuring |pos(F) - pos(R)| >= 3 (since positions are 0-indexed)
pos_F = Int('pos_F')
pos_R = Int('pos_R')
solver.add(Or([And(perf[i] == F, pos_F == i) for i in range(8)]))
solver.add(Or([And(perf[i] == R, pos_R == i) for i in range(8)]))
solver.add(Or(
    And(pos_F < pos_R, pos_R - pos_F >= 3),
    And(pos_R < pos_F, pos_F - pos_R >= 3)
))

# Constraint: O is performed either first or fifth
solver.add(Or(perf[0] == O, perf[4] == O))

# Constraint: The eighth composition performed is either L or H
solver.add(Or(perf[7] == L, perf[7] == H))

# Constraint: P is performed at some time before S
pos_P = Int('pos_P')
pos_S = Int('pos_S')
solver.add(Or([And(perf[i] == P, pos_P == i) for i in range(8)]))
solver.add(Or([And(perf[i] == S, pos_S == i) for i in range(8)]))
solver.add(pos_P < pos_S)

# Constraint: At least one composition is performed either after O and before S, or after S and before O
# This means there is at least one composition between O and S in either order
pos_O = Int('pos_O')
solver.add(Or([And(perf[i] == O, pos_O == i) for i in range(8)]))
# Ensure |pos_O - pos_S| >= 2
solver.add(Or(
    And(pos_O < pos_S, pos_S - pos_O >= 2),
    And(pos_S < pos_O, pos_O - pos_S >= 2)
))

# Given condition: T is performed fifth and F is performed sixth
solver.push()
solver.add(perf[4] == T)
solver.add(perf[5] == F)

# From the constraints, O must be first (since it cannot be fifth, as F is at 5)
solver.add(perf[0] == O)

# R must be at position <= 2 (to satisfy the "at least two compositions between R and F" constraint)
# Since F is at 5, R must be at position <= 2
solver.add(Or([perf[i] == R for i in range(3)]))

# Now, let's find possible positions for S under the given condition
# We'll check each option (A-E) to see if S can be in the specified positions

# Define the options as constraints on S's position
# Option A: S is fourth or seventh (positions 3 or 6)
opt_a_constr = Or(perf[3] == S, perf[6] == S)

# Option B: S is third or sixth (positions 2 or 5)
opt_b_constr = Or(perf[2] == S, perf[5] == S)

# Option C: S is third or fourth (positions 2 or 3)
opt_c_constr = Or(perf[2] == S, perf[3] == S)

# Option D: S is second or seventh (positions 1 or 6)
opt_d_constr = Or(perf[1] == S, perf[6] == S)

# Option E: S is first or fourth (positions 0 or 3)
opt_e_constr = Or(perf[0] == S, perf[3] == S)

# Now, test each option
found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
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