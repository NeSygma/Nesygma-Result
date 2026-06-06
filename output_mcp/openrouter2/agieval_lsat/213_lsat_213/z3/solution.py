from z3 import *

solver = Solver()
# Declare positions for each clue
pos_R = Int('pos_R')
pos_S = Int('pos_S')
pos_T = Int('pos_T')
pos_U = Int('pos_U')
pos_W = Int('pos_W')
pos_X = Int('pos_X')
pos_Z = Int('pos_Z')

# Domain constraints: positions 1..7
for p in [pos_R, pos_S, pos_T, pos_U, pos_W, pos_X, pos_Z]:
    solver.add(p >= 1, p <= 7)

# All distinct
solver.add(Distinct([pos_R, pos_S, pos_T, pos_U, pos_W, pos_X, pos_Z]))

# Constraints
solver.add(pos_T != 1)  # T cannot be in chapter 1
solver.add(pos_T + 3 == pos_W)  # T before W with exactly two chapters between
solver.add(Abs(pos_S - pos_Z) != 1)  # S and Z not adjacent
solver.add(Abs(pos_W - pos_X) != 1)  # W and X not adjacent
solver.add(Abs(pos_U - pos_X) == 1)  # U and X adjacent

# Option constraints
opt_a_constr = And(pos_S == 1, pos_T == 2, pos_Z == 3, pos_X == 4, pos_U == 5, pos_W == 6, pos_R == 7)
opt_b_constr = And(pos_T == 1, pos_X == 2, pos_U == 3, pos_W == 4, pos_S == 5, pos_R == 6, pos_Z == 7)
opt_c_constr = And(pos_U == 1, pos_S == 2, pos_X == 3, pos_T == 4, pos_Z == 5, pos_R == 6, pos_W == 7)
opt_d_constr = And(pos_X == 1, pos_U == 2, pos_T == 3, pos_Z == 4, pos_R == 5, pos_W == 6, pos_S == 7)
opt_e_constr = And(pos_Z == 1, pos_R == 2, pos_T == 3, pos_U == 4, pos_X == 5, pos_W == 6, pos_S == 7)

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