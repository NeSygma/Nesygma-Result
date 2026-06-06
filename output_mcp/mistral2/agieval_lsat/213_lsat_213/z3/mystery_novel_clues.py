from z3 import *

solver = Solver()

# Declare the chapters as integers 1 through 7
chapters = [Int(f'chapter_{i}') for i in range(1, 8)]

# Declare the clues as symbolic constants
R, S, T, U, W, X, Z = Ints('R S T U W X Z')

# Each chapter must be assigned exactly one clue
solver.add(Distinct(chapters))

# Each clue must be mentioned exactly once
solver.add(Distinct([R, S, T, U, W, X, Z]))

# Assign clues to chapters (chapters are positions, clues are values)
# We need to ensure that each chapter's value is one of the clues
# and each clue is assigned to exactly one chapter.
# To do this, we will use the fact that chapters are distinct and clues are distinct.
# We will also add constraints to ensure that the clues are assigned to the chapters.

# Helper: Ensure that the values of chapters are exactly the clues
solver.add(Or([And(chapters[0] == R, chapters[1] != R, chapters[2] != R, chapters[3] != R, chapters[4] != R, chapters[5] != R, chapters[6] != R),
               And(chapters[0] == S, chapters[1] != S, chapters[2] != S, chapters[3] != S, chapters[4] != S, chapters[5] != S, chapters[6] != S),
               And(chapters[0] == T, chapters[1] != T, chapters[2] != T, chapters[3] != T, chapters[4] != T, chapters[5] != T, chapters[6] != T),
               And(chapters[0] == U, chapters[1] != U, chapters[2] != U, chapters[3] != U, chapters[4] != U, chapters[5] != U, chapters[6] != U),
               And(chapters[0] == W, chapters[1] != W, chapters[2] != W, chapters[3] != W, chapters[4] != W, chapters[5] != W, chapters[6] != W),
               And(chapters[0] == X, chapters[1] != X, chapters[2] != X, chapters[3] != X, chapters[4] != X, chapters[5] != X, chapters[6] != X),
               And(chapters[0] == Z, chapters[1] != Z, chapters[2] != Z, chapters[3] != Z, chapters[4] != Z, chapters[5] != Z, chapters[6] != Z)]))

solver.add(Or([And(chapters[1] == R, chapters[0] != R, chapters[2] != R, chapters[3] != R, chapters[4] != R, chapters[5] != R, chapters[6] != R),
               And(chapters[1] == S, chapters[0] != S, chapters[2] != S, chapters[3] != S, chapters[4] != S, chapters[5] != S, chapters[6] != S),
               And(chapters[1] == T, chapters[0] != T, chapters[2] != T, chapters[3] != T, chapters[4] != T, chapters[5] != T, chapters[6] != T),
               And(chapters[1] == U, chapters[0] != U, chapters[2] != U, chapters[3] != U, chapters[4] != U, chapters[5] != U, chapters[6] != U),
               And(chapters[1] == W, chapters[0] != W, chapters[2] != W, chapters[3] != W, chapters[4] != W, chapters[5] != W, chapters[6] != W),
               And(chapters[1] == X, chapters[0] != X, chapters[2] != X, chapters[3] != X, chapters[4] != X, chapters[5] != X, chapters[6] != X),
               And(chapters[1] == Z, chapters[0] != Z, chapters[2] != Z, chapters[3] != Z, chapters[4] != Z, chapters[5] != Z, chapters[6] != Z)]))

solver.add(Or([And(chapters[2] == R, chapters[0] != R, chapters[1] != R, chapters[3] != R, chapters[4] != R, chapters[5] != R, chapters[6] != R),
               And(chapters[2] == S, chapters[0] != S, chapters[1] != S, chapters[3] != S, chapters[4] != S, chapters[5] != S, chapters[6] != S),
               And(chapters[2] == T, chapters[0] != T, chapters[1] != T, chapters[3] != T, chapters[4] != T, chapters[5] != T, chapters[6] != T),
               And(chapters[2] == U, chapters[0] != U, chapters[1] != U, chapters[3] != U, chapters[4] != U, chapters[5] != U, chapters[6] != U),
               And(chapters[2] == W, chapters[0] != W, chapters[1] != W, chapters[3] != W, chapters[4] != W, chapters[5] != W, chapters[6] != W),
               And(chapters[2] == X, chapters[0] != X, chapters[1] != X, chapters[3] != X, chapters[4] != X, chapters[5] != X, chapters[6] != X),
               And(chapters[2] == Z, chapters[0] != Z, chapters[1] != Z, chapters[3] != Z, chapters[4] != Z, chapters[5] != Z, chapters[6] != Z)]))

solver.add(Or([And(chapters[3] == R, chapters[0] != R, chapters[1] != R, chapters[2] != R, chapters[4] != R, chapters[5] != R, chapters[6] != R),
               And(chapters[3] == S, chapters[0] != S, chapters[1] != S, chapters[2] != S, chapters[4] != S, chapters[5] != S, chapters[6] != S),
               And(chapters[3] == T, chapters[0] != T, chapters[1] != T, chapters[2] != T, chapters[4] != T, chapters[5] != T, chapters[6] != T),
               And(chapters[3] == U, chapters[0] != U, chapters[1] != U, chapters[2] != U, chapters[4] != U, chapters[5] != U, chapters[6] != U),
               And(chapters[3] == W, chapters[0] != W, chapters[1] != W, chapters[2] != W, chapters[4] != W, chapters[5] != W, chapters[6] != W),
               And(chapters[3] == X, chapters[0] != X, chapters[1] != X, chapters[2] != X, chapters[4] != X, chapters[5] != X, chapters[6] != X),
               And(chapters[3] == Z, chapters[0] != Z, chapters[1] != Z, chapters[2] != Z, chapters[4] != Z, chapters[5] != Z, chapters[6] != Z)]))

solver.add(Or([And(chapters[4] == R, chapters[0] != R, chapters[1] != R, chapters[2] != R, chapters[3] != R, chapters[5] != R, chapters[6] != R),
               And(chapters[4] == S, chapters[0] != S, chapters[1] != S, chapters[2] != S, chapters[3] != S, chapters[5] != S, chapters[6] != S),
               And(chapters[4] == T, chapters[0] != T, chapters[1] != T, chapters[2] != T, chapters[3] != T, chapters[5] != T, chapters[6] != T),
               And(chapters[4] == U, chapters[0] != U, chapters[1] != U, chapters[2] != U, chapters[3] != U, chapters[5] != U, chapters[6] != U),
               And(chapters[4] == W, chapters[0] != W, chapters[1] != W, chapters[2] != W, chapters[3] != W, chapters[5] != W, chapters[6] != W),
               And(chapters[4] == X, chapters[0] != X, chapters[1] != X, chapters[2] != X, chapters[3] != X, chapters[5] != X, chapters[6] != X),
               And(chapters[4] == Z, chapters[0] != Z, chapters[1] != Z, chapters[2] != Z, chapters[3] != Z, chapters[5] != Z, chapters[6] != Z)]))

solver.add(Or([And(chapters[5] == R, chapters[0] != R, chapters[1] != R, chapters[2] != R, chapters[3] != R, chapters[4] != R, chapters[6] != R),
               And(chapters[5] == S, chapters[0] != S, chapters[1] != S, chapters[2] != S, chapters[3] != S, chapters[4] != S, chapters[6] != S),
               And(chapters[5] == T, chapters[0] != T, chapters[1] != T, chapters[2] != T, chapters[3] != T, chapters[4] != T, chapters[6] != T),
               And(chapters[5] == U, chapters[0] != U, chapters[1] != U, chapters[2] != U, chapters[3] != U, chapters[4] != U, chapters[6] != U),
               And(chapters[5] == W, chapters[0] != W, chapters[1] != W, chapters[2] != W, chapters[3] != W, chapters[4] != W, chapters[6] != W),
               And(chapters[5] == X, chapters[0] != X, chapters[1] != X, chapters[2] != X, chapters[3] != X, chapters[4] != X, chapters[6] != X),
               And(chapters[5] == Z, chapters[0] != Z, chapters[1] != Z, chapters[2] != Z, chapters[3] != Z, chapters[4] != Z, chapters[6] != Z)]))

solver.add(Or([And(chapters[6] == R, chapters[0] != R, chapters[1] != R, chapters[2] != R, chapters[3] != R, chapters[4] != R, chapters[5] != R),
               And(chapters[6] == S, chapters[0] != S, chapters[1] != S, chapters[2] != S, chapters[3] != S, chapters[4] != S, chapters[5] != S),
               And(chapters[6] == T, chapters[0] != T, chapters[1] != T, chapters[2] != T, chapters[3] != T, chapters[4] != T, chapters[5] != T),
               And(chapters[6] == U, chapters[0] != U, chapters[1] != U, chapters[2] != U, chapters[3] != U, chapters[4] != U, chapters[5] != U),
               And(chapters[6] == W, chapters[0] != W, chapters[1] != W, chapters[2] != W, chapters[3] != W, chapters[4] != W, chapters[5] != W),
               And(chapters[6] == X, chapters[0] != X, chapters[1] != X, chapters[2] != X, chapters[3] != X, chapters[4] != X, chapters[5] != X),
               And(chapters[6] == Z, chapters[0] != Z, chapters[1] != Z, chapters[2] != Z, chapters[3] != Z, chapters[4] != Z, chapters[5] != Z)]))

# Constraints from the problem statement

# T cannot be mentioned in chapter 1
solver.add(chapters[0] != T)

# T must be mentioned before W, with exactly two chapters separating T and W
# This means if T is in chapter i, W must be in chapter i+3
for i in range(4):  # T can be in chapters 2, 3, 4, or 5 (0-indexed: 1, 2, 3, 4)
    solver.add(Implies(chapters[i] == T, chapters[i+3] == W))

# S and Z cannot be mentioned in adjacent chapters
for i in range(6):
    solver.add(Not(And(Or(chapters[i] == S, chapters[i] == Z), Or(chapters[i+1] == S, chapters[i+1] == Z))))

# W and X cannot be mentioned in adjacent chapters
for i in range(6):
    solver.add(Not(And(Or(chapters[i] == W, chapters[i] == X), Or(chapters[i+1] == W, chapters[i+1] == X))))

# U and X must be mentioned in adjacent chapters
adjacent_ux = []
for i in range(6):
    adjacent_ux.append(And(chapters[i] == U, Or(chapters[i+1] == X, chapters[i-1] == X)))
    adjacent_ux.append(And(chapters[i] == X, Or(chapters[i+1] == U, chapters[i-1] == U)))
solver.add(Or(adjacent_ux))

# Evaluate the multiple choice options
found_options = []

# Option A: S, T, Z, X, U, W, R
solver.push()
solver.add(chapters[0] == S)
solver.add(chapters[1] == T)
solver.add(chapters[2] == Z)
solver.add(chapters[3] == X)
solver.add(chapters[4] == U)
solver.add(chapters[5] == W)
solver.add(chapters[6] == R)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: T, X, U, W, S, R, Z
solver.push()
solver.add(chapters[0] == T)
solver.add(chapters[1] == X)
solver.add(chapters[2] == U)
solver.add(chapters[3] == W)
solver.add(chapters[4] == S)
solver.add(chapters[5] == R)
solver.add(chapters[6] == Z)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: U, S, X, T, Z, R, W
solver.push()
solver.add(chapters[0] == U)
solver.add(chapters[1] == S)
solver.add(chapters[2] == X)
solver.add(chapters[3] == T)
solver.add(chapters[4] == Z)
solver.add(chapters[5] == R)
solver.add(chapters[6] == W)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: X, U, T, Z, R, W, S
solver.push()
solver.add(chapters[0] == X)
solver.add(chapters[1] == U)
solver.add(chapters[2] == T)
solver.add(chapters[3] == Z)
solver.add(chapters[4] == R)
solver.add(chapters[5] == W)
solver.add(chapters[6] == S)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: Z, R, T, U, X, W, S
solver.push()
solver.add(chapters[0] == Z)
solver.add(chapters[1] == R)
solver.add(chapters[2] == T)
solver.add(chapters[3] == U)
solver.add(chapters[4] == X)
solver.add(chapters[5] == W)
solver.add(chapters[6] == S)
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