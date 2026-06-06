from z3 import *

solver = Solver()

# Variables: chapter assignment for each clue (1-7)
R, S, T, U, W, X, Z = Ints('R S T U W X Z')
clues = [R, S, T, U, W, X, Z]

# Each clue assigned to a chapter 1-7, all different
for c in clues:
    solver.add(c >= 1, c <= 7)
solver.add(Distinct(clues))

# Given: Z is mentioned in chapter 7
solver.add(Z == 7)

# Constraint 1: T cannot be mentioned in chapter 1
solver.add(T != 1)

# Constraint 2: T must be mentioned before W, exactly two chapters separating
# "exactly two chapters separating" means W = T + 3
solver.add(W == T + 3)

# Constraint 3: S and Z cannot be mentioned in adjacent chapters
solver.add(Abs(S - Z) != 1)

# Constraint 4: W and X cannot be mentioned in adjacent chapters
solver.add(Abs(W - X) != 1)

# Constraint 5: U and X must be mentioned in adjacent chapters
solver.add(Abs(U - X) == 1)

# Now test each option
found_options = []

# (A) R is mentioned in chapter 3
solver.push()
solver.add(R == 3)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# (B) S is mentioned in chapter 3
solver.push()
solver.add(S == 3)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# (C) T is mentioned in chapter 4
solver.push()
solver.add(T == 4)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# (D) U is mentioned in chapter 1
solver.push()
solver.add(U == 1)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# (E) X is mentioned in chapter 5
solver.push()
solver.add(X == 5)
if solver.check() == sat:
    found_options.append("E")
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