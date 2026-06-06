from z3 import *

solver = Solver()

# Define position variables for each composition
pos_F = Int('pos_F')
pos_H = Int('pos_H')
pos_L = Int('pos_L')
pos_O = Int('pos_O')
pos_P = Int('pos_P')
pos_R = Int('pos_R')
pos_S = Int('pos_S')
pos_T = Int('pos_T')

# All positions between 1 and 8 inclusive
compositions = [pos_F, pos_H, pos_L, pos_O, pos_P, pos_R, pos_S, pos_T]
for p in compositions:
    solver.add(p >= 1, p <= 8)

# All distinct
solver.add(Distinct(compositions))

# Base constraints from problem statement

# 1. T is performed either immediately before F or immediately after R.
solver.add(Or(pos_T == pos_F - 1, pos_T == pos_R + 1))

# 2. At least two compositions between F and R (in either order)
solver.add(Or(And(pos_F < pos_R, pos_R - pos_F >= 3),
              And(pos_R < pos_F, pos_F - pos_R >= 3)))

# 3. O is performed either first or fifth
solver.add(Or(pos_O == 1, pos_O == 5))

# 4. The eighth composition is either L or H
solver.add(Or(pos_L == 8, pos_H == 8))

# 5. P is performed before S
solver.add(pos_P < pos_S)

# 6. At least one composition between O and S
solver.add(Or(And(pos_O < pos_S, pos_S - pos_O >= 2),
              And(pos_S < pos_O, pos_O - pos_S >= 2)))

# Additional condition: S is performed fourth
solver.add(pos_S == 4)

# Now test each answer option for the first three positions
found_options = []

# Option A: F, H, P as first, second, third respectively
opt_a_constr = And(pos_F == 1, pos_H == 2, pos_P == 3)

# Option B: H, P, L
opt_b_constr = And(pos_H == 1, pos_P == 2, pos_L == 3)

# Option C: O, P, R
opt_c_constr = And(pos_O == 1, pos_P == 2, pos_R == 3)

# Option D: O, P, T
opt_d_constr = And(pos_O == 1, pos_P == 2, pos_T == 3)

# Option E: P, R, T
opt_e_constr = And(pos_P == 1, pos_R == 2, pos_T == 3)

for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr),
                       ("C", opt_c_constr), ("D", opt_d_constr),
                       ("E", opt_e_constr)]:
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