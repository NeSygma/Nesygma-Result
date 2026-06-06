from z3 import *

solver = Solver()
# Variables for positions 1..8
pos_F = Int('pos_F')
pos_H = Int('pos_H')
pos_L = Int('pos_L')
pos_O = Int('pos_O')
pos_P = Int('pos_P')
pos_R = Int('pos_R')
pos_S = Int('pos_S')
pos_T = Int('pos_T')

# Domain constraints
for v in [pos_F, pos_H, pos_L, pos_O, pos_P, pos_R, pos_S, pos_T]:
    solver.add(v >= 1, v <= 8)

# Distinct constraint
solver.add(Distinct([pos_F, pos_H, pos_L, pos_O, pos_P, pos_R, pos_S, pos_T]))

# Base constraints
# T is performed either immediately before F or immediately after R.
solver.add(Or(pos_T == pos_F - 1, pos_T == pos_R + 1))
# At least two compositions are performed either after F and before R, or after R and before F.
solver.add(Or(pos_F - pos_R >= 3, pos_R - pos_F >= 3))
# O is performed either first or fifth.
solver.add(Or(pos_O == 1, pos_O == 5))
# The eighth composition performed is either L or H.
solver.add(Or(pos_L == 8, pos_H == 8))
# P is performed at some time before S.
solver.add(pos_P < pos_S)
# At least one composition is performed either after O and before S, or after S and before O.
solver.add(Or(pos_O - pos_S >= 2, pos_S - pos_O >= 2))

# Assumption: O is performed immediately after T
solver.add(pos_O == pos_T + 1)

# Options constraints
opt_a_constr = Or(pos_F == 1, pos_F == 2)
opt_b_constr = Or(pos_F == 2, pos_F == 3)
opt_c_constr = Or(pos_F == 4, pos_F == 6)
opt_d_constr = Or(pos_F == 4, pos_F == 7)
opt_e_constr = Or(pos_F == 6, pos_F == 7)

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