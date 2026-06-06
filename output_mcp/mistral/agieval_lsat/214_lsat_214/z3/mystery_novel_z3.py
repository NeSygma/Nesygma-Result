from z3 import *

# Declare the clues as constants
R, S, T, U, W, X, Z = Ints('R S T U W X Z')
clues = [R, S, T, U, W, X, Z]

# Create a solver
solver = Solver()

# Chapters are 1-indexed in the problem, but we'll use 0-indexed list for Z3
# chapters[i] is the clue in chapter i+1
chapters = [Int(f'chapter_{i+1}') for i in range(7)]

# Each chapter must be assigned a unique clue
solver.add(Distinct(chapters))

# Ensure each chapter's value is one of the clues
for i in range(7):
    solver.add(Or([chapters[i] == c for c in clues]))

# Constraint: X is mentioned in chapter 1
solver.add(chapters[0] == X)

# Constraint: T cannot be mentioned in chapter 1
solver.add(chapters[0] != T)

# Constraint: T must be mentioned before W, with exactly two chapters separating T and W
# This means if T is in chapter i, W is in chapter i+3
# We need to find an index i such that chapters[i] == T and chapters[i+3] == W
possible_T_positions = []
for i in range(4):  # i can be 0,1,2,3 (since i+3 must be <=6)
    possible_T_positions.append(And(chapters[i] == T, chapters[i+3] == W))
solver.add(Or(possible_T_positions))

# Constraint: S and Z cannot be mentioned in adjacent chapters
for i in range(6):
    solver.add(Not(And(chapters[i] == S, chapters[i+1] == Z)))
    solver.add(Not(And(chapters[i] == Z, chapters[i+1] == S)))

# Constraint: W and X cannot be mentioned in adjacent chapters
for i in range(6):
    solver.add(Not(And(chapters[i] == W, chapters[i+1] == X)))
    solver.add(Not(And(chapters[i] == X, chapters[i+1] == W)))

# Constraint: U and X must be mentioned in adjacent chapters
# This means there exists an i such that chapters[i] == U and chapters[i+1] == X, or vice versa
possible_UX_adjacent = []
for i in range(6):
    possible_UX_adjacent.append(And(chapters[i] == U, chapters[i+1] == X))
    possible_UX_adjacent.append(And(chapters[i] == X, chapters[i+1] == U))
solver.add(Or(possible_UX_adjacent))

# Now, evaluate each multiple-choice option
found_options = []

# Option A: R is mentioned in chapter 3 (index 2)
opt_a_constr = (chapters[2] == R)
solver.push()
solver.add(opt_a_constr)
if solver.check() == sat:
    found_options.append("A")
    print("Option A is satisfiable")
solver.pop()

# Option B: R is mentioned in chapter 7 (index 6)
opt_b_constr = (chapters[6] == R)
solver.push()
solver.add(opt_b_constr)
if solver.check() == sat:
    found_options.append("B")
    print("Option B is satisfiable")
solver.pop()

# Option C: S is mentioned in chapter 2 (index 1)
opt_c_constr = (chapters[1] == S)
solver.push()
solver.add(opt_c_constr)
if solver.check() == sat:
    found_options.append("C")
    print("Option C is satisfiable")
solver.pop()

# Option D: W is mentioned in chapter 5 (index 4)
opt_d_constr = (chapters[4] == W)
solver.push()
solver.add(opt_d_constr)
if solver.check() == sat:
    found_options.append("D")
    print("Option D is satisfiable")
solver.pop()

# Option E: Z is mentioned in chapter 3 (index 2)
opt_e_constr = (chapters[2] == Z)
solver.push()
solver.add(opt_e_constr)
if solver.check() == sat:
    found_options.append("E")
    print("Option E is satisfiable")
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