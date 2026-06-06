from z3 import *

solver = Solver()

# Variables: chapter position for each clue (1-7)
R, S, T, U, W, X, Z = Ints('R S T U W X Z')
clues = [R, S, T, U, W, X, Z]

# Each clue is assigned to a chapter 1-7
for c in clues:
    solver.add(c >= 1, c <= 7)

# All clues in distinct chapters
solver.add(Distinct(clues))

# Base constraints:
# T cannot be mentioned in chapter 1
solver.add(T != 1)

# T must be mentioned before W, and exactly two chapters separating T and W
# This means W = T + 3 (T before W with exactly 2 chapters between them)
solver.add(W == T + 3)

# S and Z cannot be mentioned in adjacent chapters
solver.add(Abs(S - Z) != 1)

# W and X cannot be mentioned in adjacent chapters
solver.add(Abs(W - X) != 1)

# U and X must be mentioned in adjacent chapters
solver.add(Abs(U - X) == 1)

# Additional constraint: X is mentioned in chapter 1
solver.add(X == 1)

# Define option constraints
opt_a_constr = (R == 3)
opt_b_constr = (R == 7)
opt_c_constr = (S == 2)
opt_d_constr = (W == 5)
opt_e_constr = (Z == 3)

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