from z3 import *

solver = Solver()

# Variables: chapter assignment for each clue (1-7)
R, S, T, U, W, X, Z = Ints('R S T U W X Z')
clues = [R, S, T, U, W, X, Z]

# Each clue assigned to a chapter 1-7
for c in clues:
    solver.add(c >= 1, c <= 7)

# All different chapters
solver.add(Distinct(clues))

# U is mentioned in chapter 3
solver.add(U == 3)

# T cannot be mentioned in chapter 1
solver.add(T != 1)

# T must be mentioned before W, and exactly two chapters separating T and W
# This means W = T + 3 (e.g., T=1,W=4 or T=2,W=5 or T=3,W=6 or T=4,W=7)
solver.add(W == T + 3)

# S and Z cannot be mentioned in adjacent chapters
solver.add(Abs(S - Z) != 1)

# W and X cannot be mentioned in adjacent chapters
solver.add(Abs(W - X) != 1)

# U and X must be mentioned in adjacent chapters
solver.add(Abs(U - X) == 1)

# Since U=3, X must be 2 or 4
# But W and X cannot be adjacent, so we need to check both

# Define option constraints
opt_a = (R == 1)
opt_b = (R == 5)
opt_c = (S == 7)
opt_d = (W == 6)
opt_e = (X == 4)

found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
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