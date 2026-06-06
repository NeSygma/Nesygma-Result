from z3 import *

solver = Solver()

# Declare symbolic variables for the chapter assignments of each clue
# We have 7 chapters and 7 clues: R, S, T, U, W, X, Z
chapters = [Int(f'chapter_{i}') for i in range(1, 8)]
clues = ['R', 'S', 'T', 'U', 'W', 'X', 'Z']

# Each chapter must have exactly one clue
solver.add(Distinct(chapters))

# Each clue must be mentioned exactly once
for clue in clues:
    solver.add(Or([chapters[i] == clue for i in range(7)]))

# Constraints from the problem statement
# 1. T cannot be mentioned in chapter 1
solver.add(chapters[0] != 'T')

# 2. T must be mentioned before W, with exactly two chapters separating T and W
# This means if T is in chapter i, W must be in chapter i+3
for i in range(4):  # i+3 must be <= 6 (0-indexed, so 0..6)
    solver.add(Implies(chapters[i] == 'T', chapters[i+3] == 'W'))

# 3. S and Z cannot be mentioned in adjacent chapters
for i in range(6):
    solver.add(Not(And(Or(chapters[i] == 'S', chapters[i] == 'Z'),
                      Or(chapters[i+1] == 'S', chapters[i+1] == 'Z'))))

# 4. W and X cannot be mentioned in adjacent chapters
for i in range(6):
    solver.add(Not(And(Or(chapters[i] == 'W', chapters[i] == 'X'),
                      Or(chapters[i+1] == 'W', chapters[i+1] == 'X'))))

# 5. U and X must be mentioned in adjacent chapters
# This means for some i, chapters[i] == 'U' and chapters[i+1] == 'X' or vice versa
adjacent_ux = []
for i in range(6):
    adjacent_ux.append(And(chapters[i] == 'U', chapters[i+1] == 'X'))
    adjacent_ux.append(And(chapters[i] == 'X', chapters[i+1] == 'U'))
solver.add(Or(adjacent_ux))

# Additional constraint: U is mentioned in chapter 3 (1-indexed, so index 2 in 0-indexed list)
solver.add(chapters[2] == 'U')

# Now evaluate the multiple choice options
found_options = []

# Option A: R is mentioned in chapter 1
solver.push()
solver.add(chapters[0] == 'R')
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: R is mentioned in chapter 5
solver.push()
solver.add(chapters[4] == 'R')
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: S is mentioned in chapter 7
solver.push()
solver.add(chapters[6] == 'S')
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: W is mentioned in chapter 6
solver.push()
solver.add(chapters[5] == 'W')
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: X is mentioned in chapter 4
solver.push()
solver.add(chapters[3] == 'X')
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