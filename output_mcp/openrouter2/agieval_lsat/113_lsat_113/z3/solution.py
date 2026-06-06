from z3 import *

solver = Solver()

# Variables for positions of each article
pos_G, pos_H, pos_J, pos_Q, pos_R, pos_S, pos_Y = Ints('pos_G pos_H pos_J pos_Q pos_R pos_S pos_Y')

# Domain constraints: positions 1 through 7
for pos in [pos_G, pos_H, pos_J, pos_Q, pos_R, pos_S, pos_Y]:
    solver.add(pos >= 1, pos <= 7)

# All articles are edited in distinct positions
solver.add(Distinct([pos_G, pos_H, pos_J, pos_Q, pos_R, pos_S, pos_Y]))

# Consecutive articles cannot cover the same topic
# Finance: G, H, J
solver.add(Abs(pos_G - pos_H) != 1)
solver.add(Abs(pos_G - pos_J) != 1)
solver.add(Abs(pos_H - pos_J) != 1)
# Nutrition: Q, R, S
solver.add(Abs(pos_Q - pos_R) != 1)
solver.add(Abs(pos_Q - pos_S) != 1)
solver.add(Abs(pos_R - pos_S) != 1)

# S earlier than Y
solver.add(pos_S < pos_Y)

# J earlier than G, G earlier than R
solver.add(pos_J < pos_G)
solver.add(pos_G < pos_R)

# S can be earlier than Q only if Q is third
solver.add(Implies(pos_S < pos_Q, pos_Q == 3))

# J is third (condition for the question)
solver.add(pos_J == 3)

# Option constraints
opt_a_constr = pos_G == 4
opt_b_constr = pos_J == 6
opt_c_constr = pos_Q == 1
opt_d_constr = pos_S == 2
opt_e_constr = pos_Y == 5

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