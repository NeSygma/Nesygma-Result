from z3 import *

solver = Solver()

# Declare variables for each clue's chapter (1-7)
pos_R = Int('pos_R')
pos_S = Int('pos_S')
pos_T = Int('pos_T')
pos_U = Int('pos_U')
pos_W = Int('pos_W')
pos_X = Int('pos_X')
pos_Z = Int('pos_Z')

# Base constraints
# All chapters are between 1 and 7
solver.add(pos_R >= 1, pos_R <= 7)
solver.add(pos_S >= 1, pos_S <= 7)
solver.add(pos_T >= 1, pos_T <= 7)
solver.add(pos_U >= 1, pos_U <= 7)
solver.add(pos_W >= 1, pos_W <= 7)
solver.add(pos_X >= 1, pos_X <= 7)
solver.add(pos_Z >= 1, pos_Z <= 7)

# All clues are in distinct chapters
solver.add(Distinct(pos_R, pos_S, pos_T, pos_U, pos_W, pos_X, pos_Z))

# T cannot be in chapter 1
solver.add(pos_T != 1)

# T before W and exactly two chapters separating them: pos_W = pos_T + 3
solver.add(pos_W == pos_T + 3)

# S and Z not adjacent
solver.add(Abs(pos_S - pos_Z) != 1)

# W and X not adjacent
solver.add(Abs(pos_W - pos_X) != 1)

# U and X adjacent
solver.add(Abs(pos_U - pos_X) == 1)

# Z is in chapter 7
solver.add(pos_Z == 7)

# Define option constraints
opt_a_constr = (pos_R == 3)
opt_b_constr = (pos_S == 3)
opt_c_constr = (pos_T == 4)
opt_d_constr = (pos_U == 1)
opt_e_constr = (pos_X == 5)

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