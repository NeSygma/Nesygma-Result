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
# We can model this by ensuring that the chapters are a permutation of the clues
from itertools import permutations
solver.add(Or([And([chapters[i] == p[i] for i in range(7)]) for p in permutations(clues)]))

# 3. Constraints from the problem statement

# T cannot be in chapter 1
solver.add(chapters[0] != T)

# T must be before W, with exactly two chapters separating them
# So if T is in chapter i (1-based), W is in chapter i+3
# We can enforce this by ensuring that the position of T and W satisfy this condition
# Let's define a helper function to get the position of a clue in the chapters
# But since chapters are symbolic, we can instead enforce the constraint directly
for i in range(4):  # T can be in chapters 1-4 (since W must be in i+3 and there are 7 chapters)
    solver.add(Implies(chapters[i] == T, chapters[i+3] == W))

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
    # Debug: print the model for option A
    model = solver.model()
    print("Option A model:")
    for i in range(7):
        print(f"Chapter {i+1}: {model[chapters[i]]}")
solver.pop()

# Option B: R is mentioned in chapter 5
solver.push()
solver.add(chapters[4] == R)
if solver.check() == sat:
    found_options.append("B")
    # Debug: print the model for option B
    model = solver.model()
    print("Option B model:")
    for i in range(7):
        print(f"Chapter {i+1}: {model[chapters[i]]}")
solver.pop()

# Option C: S is mentioned in chapter 7
solver.push()
solver.add(chapters[6] == S)
if solver.check() == sat:
    found_options.append("C")
    # Debug: print the model for option C
    model = solver.model()
    print("Option C model:")
    for i in range(7):
        print(f"Chapter {i+1}: {model[chapters[i]]}")
solver.pop()

# Option D: W is mentioned in chapter 6
solver.push()
solver.add(chapters[5] == W)
if solver.check() == sat:
    found_options.append("D")
    # Debug: print the model for option D
    model = solver.model()
    print("Option D model:")
    for i in range(7):
        print(f"Chapter {i+1}: {model[chapters[i]]}")
solver.pop()

# Option E: X is mentioned in chapter 4
solver.push()
solver.add(chapters[3] == X)
if solver.check() == sat:
    found_options.append("E")
    # Debug: print the model for option E
    model = solver.model()
    print("Option E model:")
    for i in range(7):
        print(f"Chapter {i+1}: {model[chapters[i]]}")
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