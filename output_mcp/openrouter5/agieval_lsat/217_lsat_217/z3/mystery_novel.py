from z3 import *

solver = Solver()

# Seven chapters (1-7), seven clues (R, S, T, U, W, X, Z)
# Each clue is assigned a chapter number (1-7), all distinct
clues = ['R', 'S', 'T', 'U', 'W', 'X', 'Z']
chapter = {c: Int(f'chapter_{c}') for c in clues}

# Domain: each chapter between 1 and 7
for c in clues:
    solver.add(chapter[c] >= 1, chapter[c] <= 7)

# All different chapters
solver.add(Distinct([chapter[c] for c in clues]))

# Constraints:
# 1. T cannot be mentioned in chapter 1.
solver.add(chapter['T'] != 1)

# 2. T must be mentioned before W, and there must be exactly two chapters separating
#    the mention of T from the mention of W.
#    i.e., chapter[W] - chapter[T] = 3 (since exactly two chapters between them)
solver.add(chapter['W'] - chapter['T'] == 3)

# 3. S and Z cannot be mentioned in adjacent chapters.
solver.add(Abs(chapter['S'] - chapter['Z']) != 1)

# 4. W and X cannot be mentioned in adjacent chapters.
solver.add(Abs(chapter['W'] - chapter['X']) != 1)

# 5. U and X must be mentioned in adjacent chapters.
solver.add(Abs(chapter['U'] - chapter['X']) == 1)

# Evaluate each option
found_options = []

# (A) R is mentioned in chapter 7.
opt_a = (chapter['R'] == 7)

# (B) T is mentioned in chapter 5.
opt_b = (chapter['T'] == 5)

# (C) U is mentioned in chapter 7.
opt_c = (chapter['U'] == 7)

# (D) W is mentioned in chapter 3.
opt_d = (chapter['W'] == 3)

# (E) X is mentioned in chapter 6.
opt_e = (chapter['X'] == 6)

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