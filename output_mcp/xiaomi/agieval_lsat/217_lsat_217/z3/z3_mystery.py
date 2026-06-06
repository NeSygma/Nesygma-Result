from z3 import *

solver = Solver()

# Variables: chapter assignment for each clue (1-7)
R, S, T, U, W, X, Z = Ints('R S T U W X Z')
clues = [R, S, T, U, W, X, Z]

# Each clue assigned to a chapter 1-7
for c in clues:
    solver.add(c >= 1, c <= 7)

# All clues in distinct chapters
solver.add(Distinct(clues))

# T cannot be in chapter 1
solver.add(T != 1)

# T must be mentioned before W, with exactly two chapters separating them
# "exactly two chapters separating" means W - T == 3 (e.g., T in ch1, W in ch4)
solver.add(W - T == 3)

# S and Z cannot be in adjacent chapters
solver.add(Abs(S - Z) != 1)

# W and X cannot be in adjacent chapters
solver.add(Abs(W - X) != 1)

# U and X must be in adjacent chapters
solver.add(Abs(U - X) == 1)

# Define option constraints
opt_a = (R == 7)
opt_b = (T == 5)
opt_c = (U == 7)
opt_d = (W == 3)
opt_e = (X == 6)

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