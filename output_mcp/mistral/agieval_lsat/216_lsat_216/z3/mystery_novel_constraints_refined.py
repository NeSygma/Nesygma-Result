from z3 import *

# BENCHMARK_MODE: ON (model-finding mode)
BENCHMARK_MODE = True

# Base constraints solver
solver = Solver()

# Variables: chapter[i] is the clue in chapter i (1-indexed)
chapters = [Int(f'chapter_{i}') for i in range(1, 8)]

# Domain: Each chapter must be assigned a distinct clue from {R, S, T, U, W, X, Z}
clues = ["R", "S", "T", "U", "W", "X", "Z"]

# Each chapter must be one of the clues
for i in range(7):
    solver.add(Or([chapters[i] == ord(c) for c in clues]))

# All chapters must have distinct clues
solver.add(Distinct(chapters))

# Constraint 1: T cannot be in chapter 1
solver.add(chapters[0] != ord("T"))

# Constraint 2: T must be before W, with exactly two chapters separating them
# So if T is in chapter i, W must be in chapter i+3
# We need to enforce this relationship
# Also, ensure that T and W are placed uniquely
solver.add(Or([
    And(chapters[0] == ord("T"), chapters[3] == ord("W")),
    And(chapters[1] == ord("T"), chapters[4] == ord("W")),
    And(chapters[2] == ord("T"), chapters[5] == ord("W")),
    And(chapters[3] == ord("T"), chapters[6] == ord("W")),
]))

# Constraint 3: S and Z cannot be adjacent
for i in range(6):
    solver.add(Not(And(Or(chapters[i] == ord("S"), chapters[i] == ord("Z")),
                       Or(chapters[i+1] == ord("S"), chapters[i+1] == ord("Z")))))

# Constraint 4: W and X cannot be adjacent
for i in range(6):
    solver.add(Not(And(chapters[i] == ord("W"), chapters[i+1] == ord("X"))))
    solver.add(Not(And(chapters[i] == ord("X"), chapters[i+1] == ord("W"))))

# Constraint 5: U and X must be adjacent
adjacent_ux = []
for i in range(6):
    adjacent_ux.append(And(chapters[i] == ord("U"), chapters[i+1] == ord("X")))
    adjacent_ux.append(And(chapters[i] == ord("X"), chapters[i+1] == ord("U")))
solver.add(Or(adjacent_ux))

# Additional constraint: Z is mentioned in chapter 7
solver.add(chapters[6] == ord("Z"))

# Now, evaluate each option under these constraints
found_options = []

# Option A: R is mentioned in chapter 3
solver.push()
solver.add(chapters[2] == ord("R"))
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: S is mentioned in chapter 3
solver.push()
solver.add(chapters[2] == ord("S"))
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: T is mentioned in chapter 4
solver.push()
solver.add(chapters[3] == ord("T"))
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: U is mentioned in chapter 1
solver.push()
solver.add(chapters[0] == ord("U"))
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: X is mentioned in chapter 5
solver.push()
solver.add(chapters[4] == ord("X"))
if solver.check() == sat:
    found_options.append("E")
solver.pop()

# Output result
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")