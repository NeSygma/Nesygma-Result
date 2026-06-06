from z3 import *

# BENCHMARK_MODE: ON (model-finding mode)
BENCHMARK_MODE = True

# Declare the clues as symbolic constants
R, S, T, U, W, X, Z = Ints('R S T U W X Z')
clues = [R, S, T, U, W, X, Z]

# Declare the chapters as a list of Int variables
chapters = [Int(f'chapter_{i+1}') for i in range(7)]

# Create a solver
solver = Solver()

# 1. All clues must be used exactly once (distinct)
solver.add(Distinct(clues))

# 2. Each chapter must be assigned exactly one clue
for i in range(7):
    solver.add(Or([chapters[i] == c for c in clues]))
    # Ensure no two chapters have the same clue (redundant with Distinct, but explicit)
    for j in range(i+1, 7):
        solver.add(chapters[i] != chapters[j])

# 3. Constraints from the problem statement

# T cannot be in chapter 1
solver.add(chapters[0] != T)

# T must be before W, with exactly two chapters separating them
# So if T is in chapter i (1-based), W is in chapter i+3
# We can enforce this by ensuring that the position of T and W satisfy this condition
for i in range(7):
    for j in range(7):
        solver.add(Implies(And(chapters[i] == T, chapters[j] == W), j == i + 3))

# S and Z cannot be adjacent
for i in range(6):
    solver.add(Not(And(Or(chapters[i] == S, chapters[i] == Z), 
                       Or(chapters[i+1] == S, chapters[i+1] == Z))))

# W and X cannot be adjacent
for i in range(6):
    solver.add(Not(And(Or(chapters[i] == W, chapters[i] == X), 
                       Or(chapters[i+1] == W, chapters[i+1] == X))))

# U and X must be adjacent
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
solver.pop()

# Option B: R is mentioned in chapter 5
solver.push()
solver.add(chapters[4] == R)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: S is mentioned in chapter 7
solver.push()
solver.add(chapters[6] == S)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: W is mentioned in chapter 6
solver.push()
solver.add(chapters[5] == W)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: X is mentioned in chapter 4
solver.push()
solver.add(chapters[3] == X)
if solver.check() == sat:
    found_options.append("E")
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