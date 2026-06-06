from z3 import *

# BENCHMARK_MODE: ON (model-finding mode)
BENCHMARK_MODE = True

# Declare the solver
solver = Solver()

# Declare the chapters as an array of 7 Int variables (0-indexed: chapters[0] = chapter 1, ..., chapters[6] = chapter 7)
chapters = [Int(f'chapter_{i+1}') for i in range(7)]

# Declare the clues as symbolic constants
R, S, T, U, W, X, Z = Ints('R S T U W X Z')

# Add the constraint that all chapters have distinct clues
solver.add(Distinct(chapters))

# Add the constraint that all chapters are assigned one of the clues
solver.add(And([Or([chapters[i] == c for c in [R, S, T, U, W, X, Z]]) for i in range(7)]))

# Constraint 1: T cannot be mentioned in chapter 1 (chapter 0 in 0-index)
solver.add(chapters[0] != T)

# Constraint 2: T must be mentioned before W, with exactly two chapters separating T and W
# This means if T is in chapter i, W must be in chapter i+3
# We need to encode this for all possible positions of T
for i in range(4):  # T can be in chapters 0-3 (1-4) to have W in i+3 <= 6
    for j in range(7):
        solver.add(Implies(And(chapters[i] == T, chapters[j] == W), j == i + 3))

# Also, ensure that if W is in chapter j, then T must be in chapter j-3 (if j >= 3)
for j in range(3, 7):
    for i in range(7):
        solver.add(Implies(And(chapters[j] == W, chapters[i] == T), i == j - 3))

# Constraint 3: S and Z cannot be mentioned in adjacent chapters
for i in range(6):
    solver.add(Not(And(chapters[i] == S, chapters[i+1] == Z)))
    solver.add(Not(And(chapters[i] == Z, chapters[i+1] == S)))

# Constraint 4: W and X cannot be mentioned in adjacent chapters
for i in range(6):
    solver.add(Not(And(chapters[i] == W, chapters[i+1] == X)))
    solver.add(Not(And(chapters[i] == X, chapters[i+1] == W)))

# Constraint 5: U and X must be mentioned in adjacent chapters
adjacent_ux = []
for i in range(6):
    adjacent_ux.append(And(chapters[i] == U, chapters[i+1] == X))
    adjacent_ux.append(And(chapters[i] == X, chapters[i+1] == U))
solver.add(Or(adjacent_ux))

# Base constraints are set. Now test each multiple-choice option.

# Define the options as constraints
opt_A = (chapters[6] == R)  # R is mentioned in chapter 7
opt_B = (chapters[4] == T)  # T is mentioned in chapter 5
opt_C = (chapters[6] == U)  # U is mentioned in chapter 7
opt_D = (chapters[2] == W)  # W is mentioned in chapter 3
opt_E = (chapters[5] == X)  # X is mentioned in chapter 6

# Test each option
found_options = []
for letter, constr in [("A", opt_A), ("B", opt_B), ("C", opt_C), ("D", opt_D), ("E", opt_E)]:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
    solver.pop()

# Output the result
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")