from z3 import *

solver = Solver()

# Declare position variables
pos_F = Int('pos_F')
pos_H = Int('pos_H')
pos_L = Int('pos_L')
pos_O = Int('pos_O')
pos_P = Int('pos_P')
pos_R = Int('pos_R')
pos_S = Int('pos_S')
pos_T = Int('pos_T')

# Add domain constraints
for var in [pos_F, pos_H, pos_L, pos_O, pos_P, pos_R, pos_S, pos_T]:
    solver.add(var >= 1, var <= 8)

# All distinct
solver.add(Distinct([pos_F, pos_H, pos_L, pos_O, pos_P, pos_R, pos_S, pos_T]))

# Global constraints
solver.add(pos_S == 4)  # S is fourth
solver.add(Or(pos_O == 1, pos_O == 5))  # O is first or fifth
solver.add(Or(pos_L == 8, pos_H == 8))  # eighth is L or H
solver.add(pos_P < pos_S)  # P before S
solver.add(Or(pos_O + 2 <= pos_S, pos_S + 2 <= pos_O))  # at least one between O and S
solver.add(Or(pos_F + 3 <= pos_R, pos_R + 3 <= pos_F))  # at least two between F and R
solver.add(Or(pos_T + 1 == pos_F, pos_T == pos_R + 1))  # T adjacency

# Option-specific constraints as conjunctions
opt_a_constr = And(pos_F == 1, pos_H == 2, pos_P == 3)
opt_b_constr = And(pos_H == 1, pos_P == 2, pos_L == 3)
opt_c_constr = And(pos_O == 1, pos_P == 2, pos_R == 3)
opt_d_constr = And(pos_O == 1, pos_P == 2, pos_T == 3)
opt_e_constr = And(pos_P == 1, pos_R == 2, pos_T == 3)

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