from z3 import *

solver = Solver()

# Variables for each clue
R, S, T, U, W, X, Z = Ints('R S T U W X Z')

# Domain constraints: each clue appears in a chapter 1..7
for v in [R, S, T, U, W, X, Z]:
    solver.add(v >= 1, v <= 7)

# Each clue appears exactly once
solver.add(Distinct(R, S, T, U, W, X, Z))

# T cannot be in chapter 1
solver.add(T != 1)

# T must be before W and exactly two chapters separate them
solver.add(W == T + 3)

# S and Z cannot be in adjacent chapters
solver.add(Abs(S - Z) != 1)

# W and X cannot be in adjacent chapters
solver.add(Abs(W - X) != 1)

# U and X must be in adjacent chapters
solver.add(Abs(U - X) == 1)

# Option constraints
opt_a_constr = (R == 7)
opt_b_constr = (T == 5)
opt_c_constr = (U == 7)
opt_d_constr = (W == 3)
opt_e_constr = (X == 6)

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