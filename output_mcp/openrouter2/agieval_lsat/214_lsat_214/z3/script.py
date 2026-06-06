from z3 import *
solver = Solver()
# declare variables
pos_R = Int('pos_R')
pos_S = Int('pos_S')
pos_T = Int('pos_T')
pos_U = Int('pos_U')
pos_W = Int('pos_W')
pos_X = Int('pos_X')
pos_Z = Int('pos_Z')
# domain constraints
for v in [pos_R, pos_S, pos_T, pos_U, pos_W, pos_X, pos_Z]:
    solver.add(v >= 1, v <= 7)
# distinct
solver.add(Distinct([pos_R, pos_S, pos_T, pos_U, pos_W, pos_X, pos_Z]))
# X in chapter 1
solver.add(pos_X == 1)
# U adjacent to X
solver.add(Abs(pos_U - pos_X) == 1)
# W not adjacent to X
solver.add(Abs(pos_W - pos_X) != 1)
# S and Z not adjacent
solver.add(Abs(pos_S - pos_Z) != 1)
# T not in chapter 1
solver.add(pos_T != 1)
# T before W
solver.add(pos_T < pos_W)
# exactly two chapters between T and W
solver.add(pos_W - pos_T == 3)
# define option constraints
opt_a_constr = pos_R == 3
opt_b_constr = pos_R == 7
opt_c_constr = pos_S == 2
opt_d_constr = pos_W == 5
opt_e_constr = pos_Z == 3
# evaluate options
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