from z3 import *

solver = Solver()

# Seven chapters (1-7), seven clues: R, S, T, U, W, X, Z
# Each clue is mentioned exactly once, one per chapter.
# We'll use integer variables for the chapter number of each clue.
R, S, T, U, W, X, Z = Ints('R S T U W X Z')

# Domain: each clue is in chapter 1..7
clues = [R, S, T, U, W, X, Z]
for c in clues:
    solver.add(c >= 1, c <= 7)

# All different (each chapter has exactly one clue)
solver.add(Distinct(clues))

# Constraints:
# 1. T cannot be mentioned in chapter 1.
solver.add(T != 1)

# 2. T must be mentioned before W, and exactly two chapters separate them.
#    So W = T + 3 (since exactly two chapters between means difference of 3)
solver.add(W == T + 3)

# 3. S and Z cannot be mentioned in adjacent chapters.
solver.add(Abs(S - Z) != 1)

# 4. W and X cannot be mentioned in adjacent chapters.
solver.add(Abs(W - X) != 1)

# 5. U and X must be mentioned in adjacent chapters.
solver.add(Abs(U - X) == 1)

# Additional condition: U is mentioned in chapter 3.
solver.add(U == 3)

# Now evaluate each option
# (A) R is mentioned in chapter 1.
opt_a = (R == 1)
# (B) R is mentioned in chapter 5.
opt_b = (R == 5)
# (C) S is mentioned in chapter 7.
opt_c = (S == 7)
# (D) W is mentioned in chapter 6.
opt_d = (W == 6)
# (E) X is mentioned in chapter 4.
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