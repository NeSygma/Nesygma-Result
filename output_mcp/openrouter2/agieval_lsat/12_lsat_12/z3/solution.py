from z3 import *

solver = Solver()
# Declare position variables for each composition
pos_F = Int('pos_F')
pos_H = Int('pos_H')
pos_L = Int('pos_L')
pos_O = Int('pos_O')
pos_P = Int('pos_P')
pos_R = Int('pos_R')
pos_S = Int('pos_S')
pos_T = Int('pos_T')

# Domain constraints: positions 1..8
for v in [pos_F, pos_H, pos_L, pos_O, pos_P, pos_R, pos_S, pos_T]:
    solver.add(v >= 1, v <= 8)

# All positions distinct
solver.add(Distinct([pos_F, pos_H, pos_L, pos_O, pos_P, pos_R, pos_S, pos_T]))

# Base constraints
# T is performed either immediately before F or immediately after R
solver.add(Or(pos_T + 1 == pos_F, pos_T - 1 == pos_R))
# At least two compositions between F and R
solver.add(Or(pos_F + 3 <= pos_R, pos_R + 3 <= pos_F))
# O is performed either first or fifth
solver.add(Or(pos_O == 1, pos_O == 5))
# The eighth composition performed is either L or H
solver.add(Or(pos_L == 8, pos_H == 8))
# P is performed before S
solver.add(pos_P < pos_S)
# At least one composition between O and S
solver.add(Or(pos_O + 2 <= pos_S, pos_S + 2 <= pos_O))

# Option constraints
opt_a_constr = And(
    pos_L == 1,
    pos_P == 2,
    pos_S == 3,
    pos_R == 4,
    pos_O == 5,
    pos_T == 6,
    pos_F == 7,
    pos_H == 8
)
opt_b_constr = And(
    pos_O == 1,
    pos_T == 2,
    pos_P == 3,
    pos_F == 4,
    pos_S == 5,
    pos_H == 6,
    pos_R == 7,
    pos_L == 8
)
opt_c_constr = And(
    pos_P == 1,
    pos_T == 2,
    pos_F == 3,
    pos_S == 4,
    pos_L == 5,
    pos_R == 6,
    pos_O == 7,
    pos_H == 8
)
opt_d_constr = And(
    pos_P == 1,
    pos_T == 2,
    pos_F == 3,
    pos_S == 4,
    pos_O == 5,
    pos_R == 6,
    pos_L == 7,
    pos_H == 8
)
opt_e_constr = And(
    pos_T == 1,
    pos_F == 2,
    pos_P == 3,
    pos_R == 4,
    pos_O == 5,
    pos_L == 6,
    pos_S == 7,
    pos_H == 8
)

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