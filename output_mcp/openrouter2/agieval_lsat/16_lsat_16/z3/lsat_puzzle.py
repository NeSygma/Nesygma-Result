from z3 import *

solver = Solver()
# Variables for positions of each composition
pos_F = Int('pos_F')
pos_H = Int('pos_H')
pos_L = Int('pos_L')
pos_O = Int('pos_O')
pos_P = Int('pos_P')
pos_R = Int('pos_R')
pos_S = Int('pos_S')
pos_T = Int('pos_T')

# Domain constraints: positions 1 through 8
solver.add(pos_F >= 1, pos_F <= 8)
solver.add(pos_H >= 1, pos_H <= 8)
solver.add(pos_L >= 1, pos_L <= 8)
solver.add(pos_O >= 1, pos_O <= 8)
solver.add(pos_P >= 1, pos_P <= 8)
solver.add(pos_R >= 1, pos_R <= 8)
solver.add(pos_S >= 1, pos_S <= 8)
solver.add(pos_T >= 1, pos_T <= 8)

# All compositions performed exactly once
solver.add(Distinct(pos_F, pos_H, pos_L, pos_O, pos_P, pos_R, pos_S, pos_T))

# Fixed S at position 4
solver.add(pos_S == 4)

# O is performed either first or fifth
solver.add(Or(pos_O == 1, pos_O == 5))

# The eighth composition performed is either L or H
solver.add(Or(pos_L == 8, pos_H == 8))

# T is performed either immediately before F or immediately after R
solver.add(Or(pos_T == pos_F - 1, pos_T == pos_R + 1))

# At least two compositions are performed either after F and before R, or after R and before F
solver.add(Or(pos_F - pos_R >= 3, pos_R - pos_F >= 3))

# P is performed at some time before S
solver.add(pos_P < pos_S)

# At least one composition is performed either after O and before S, or after S and before O
solver.add(Or(pos_O - pos_S >= 2, pos_S - pos_O >= 2))

# Define option constraints
opt_a_constr = And(pos_F == 1, pos_H == 2, pos_P == 3)
opt_b_constr = And(pos_H == 1, pos_P == 2, pos_L == 3)
opt_c_constr = And(pos_O == 1, pos_P == 2, pos_R == 3)
opt_d_constr = And(pos_O == 1, pos_P == 2, pos_T == 3)
opt_e_constr = And(pos_P == 1, pos_R == 2, pos_T == 3)

# Evaluate options
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