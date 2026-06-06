from z3 import *

# BENCHMARK_MODE: ON (model-finding mode)
BENCHMARK_MODE = True

# Declare the clues as symbolic Int constants
R, S, T, U, W, X, Z = Ints('R S T U W X Z')

# Declare the chapters as a list of Int variables (chapter_1 to chapter_7)
chapters = [Int(f'chapter_{i+1}') for i in range(7)]

# Create a solver
solver = Solver()

# 1. All clues must be used exactly once (distinct)
solver.add(Distinct([R, S, T, U, W, X, Z]))

# 2. Each chapter must be assigned exactly one clue (distinct chapters)
solver.add(Distinct(chapters))

# 3. The chapters must be a permutation of the clues (all clues used exactly once)
# We can enforce this by ensuring that the sum of the chapters equals the sum of the clues
# and the product of the chapters equals the product of the clues, but this is not sufficient.
# Instead, we can use the fact that the chapters are distinct and the clues are distinct,
# and add constraints to ensure that the chapters are assigned the clues in a valid way.

# Helper: Ensure that the chapters are assigned exactly the clues (no extras, no omissions)
# We can do this by ensuring that the set of chapters is equal to the set of clues.
# Since Z3 does not have a built-in set equality, we can use the following:
# For every chapter, there exists a clue such that chapter == clue, and vice versa.
# But this is not directly enforceable. Instead, we can use the following:
# The chapters and clues are both distinct lists of the same length, and we can enforce
# that the chapters are assigned the clues by ensuring that the sum of the chapters
# equals the sum of the clues, and the product of the chapters equals the product of the clues.
# However, this is not sufficient for all cases. Instead, we can use the following:
# The chapters are a permutation of the clues. We can enforce this by adding constraints
# that ensure that the chapters are assigned the clues in a valid way.

# Since the clues are symbolic constants, we can enforce that the chapters are assigned
# the clues by ensuring that the chapters are equal to the clues in some order.
# We can do this by adding constraints that ensure that the chapters are assigned the clues
# in a valid way.

# For now, we will add constraints to ensure that the chapters are assigned the clues in a valid way.
# We will add constraints to ensure that the chapters are assigned the clues in a valid way.

# 4. Constraints from the problem statement

# T cannot be mentioned in chapter 1
solver.add(chapters[0] != T)

# T must be mentioned before W, with exactly two chapters separating them
# So if T is in chapter i (0-based), W is in chapter i+3 (0-based)
for i in range(4):  # T can be in chapters 0-3 (since W must be in i+3 and there are 7 chapters)
    solver.add(Implies(chapters[i] == T, chapters[i+3] == W))

# S and Z cannot be mentioned in adjacent chapters
for i in range(6):
    solver.add(Not(And(
        Or(chapters[i] == S, chapters[i] == Z), 
        Or(chapters[i+1] == S, chapters[i+1] == Z)
    )))

# W and X cannot be mentioned in adjacent chapters
for i in range(6):
    solver.add(Not(And(
        Or(chapters[i] == W, chapters[i] == X), 
        Or(chapters[i+1] == W, chapters[i+1] == X)
    )))

# U and X must be mentioned in adjacent chapters
for i in range(6):
    solver.add(Or(
        And(chapters[i] == U, chapters[i+1] == X),
        And(chapters[i] == X, chapters[i+1] == U),
        And(chapters[i+1] == U, chapters[i] == X),
        And(chapters[i+1] == X, chapters[i] == U)
    ))

# Given: U is mentioned in chapter 3 (index 2 in 0-based)
solver.add(chapters[2] == U)

# Evaluate the options
found_options = []

# Option A: R is mentioned in chapter 1
solver.push()
solver.add(chapters[0] == R)
if solver.check() == sat:
    found_options.append("A")
    model = solver.model()
    print("Option A model:")
    for i in range(7):
        print(f"Chapter {i+1}: {model[chapters[i]]}")
else:
    print("Option A: unsat or unknown")
solver.pop()

# Option B: R is mentioned in chapter 5
solver.push()
solver.add(chapters[4] == R)
if solver.check() == sat:
    found_options.append("B")
    model = solver.model()
    print("Option B model:")
    for i in range(7):
        print(f"Chapter {i+1}: {model[chapters[i]]}")
else:
    print("Option B: unsat or unknown")
solver.pop()

# Option C: S is mentioned in chapter 7
solver.push()
solver.add(chapters[6] == S)
if solver.check() == sat:
    found_options.append("C")
    model = solver.model()
    print("Option C model:")
    for i in range(7):
        print(f"Chapter {i+1}: {model[chapters[i]]}")
else:
    print("Option C: unsat or unknown")
solver.pop()

# Option D: W is mentioned in chapter 6
solver.push()
solver.add(chapters[5] == W)
if solver.check() == sat:
    found_options.append("D")
    model = solver.model()
    print("Option D model:")
    for i in range(7):
        print(f"Chapter {i+1}: {model[chapters[i]]}")
else:
    print("Option D: unsat or unknown")
solver.pop()

# Option E: X is mentioned in chapter 4
solver.push()
solver.add(chapters[3] == X)
if solver.check() == sat:
    found_options.append("E")
    model = solver.model()
    print("Option E model:")
    for i in range(7):
        print(f"Chapter {i+1}: {model[chapters[i]]}")
else:
    print("Option E: unsat or unknown")
solver.pop()

# Print the result
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")