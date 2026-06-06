from z3 import *

solver = Solver()

# Seven chapters: 1 through 7
# Seven clues: R, S, T, U, W, X, Z
# Each clue mentioned exactly once, one per chapter.
# We'll use Int variables for the chapter number of each clue.
R, S, T, U, W, X, Z = Ints('R S T U W X Z')
clues = [R, S, T, U, W, X, Z]

# Domain: each clue is in chapter 1..7
for c in clues:
    solver.add(c >= 1, c <= 7)

# All different (each chapter has exactly one clue)
solver.add(Distinct(clues))

# Constraints:
# 1. T cannot be mentioned in chapter 1.
solver.add(T != 1)

# 2. T must be mentioned before W, and there must be exactly two chapters separating the mention of T from the mention of W.
#    "exactly two chapters separating" means |T - W| = 3, and T before W means T < W.
solver.add(T < W)
solver.add(W - T == 3)

# 3. S and Z cannot be mentioned in adjacent chapters.
solver.add(Abs(S - Z) != 1)

# 4. W and X cannot be mentioned in adjacent chapters.
solver.add(Abs(W - X) != 1)

# 5. U and X must be mentioned in adjacent chapters.
solver.add(Abs(U - X) == 1)

# Additional condition from the question: X is mentioned in chapter 1.
solver.add(X == 1)

# Now evaluate each option
found_options = []

# Option A: R is mentioned in chapter 3.
opt_a = (R == 3)

# Option B: R is mentioned in chapter 7.
opt_b = (R == 7)

# Option C: S is mentioned in chapter 2.
opt_c = (S == 2)

# Option D: W is mentioned in chapter 5.
opt_d = (W == 5)

# Option E: Z is mentioned in chapter 3.
opt_e = (Z == 3)

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