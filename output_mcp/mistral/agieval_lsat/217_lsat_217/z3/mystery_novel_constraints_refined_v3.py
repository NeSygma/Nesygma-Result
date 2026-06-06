from z3 import *

# BENCHMARK_MODE: ON (model-finding mode)
BENCHMARK_MODE = True

# Declare the solver
solver = Solver()

# Declare the clues as symbolic constants
R, S, T, U, W, X, Z = Ints('R S T U W X Z')

# Declare the positions (chapters) for each clue as Int variables (1-7)
pos_R = Int('pos_R')
pos_S = Int('pos_S')
pos_T = Int('pos_T')
pos_U = Int('pos_U')
pos_W = Int('pos_W')
pos_X = Int('pos_X')
pos_Z = Int('pos_Z')

# All positions must be between 1 and 7
solver.add(And(pos_R >= 1, pos_R <= 7))
solver.add(And(pos_S >= 1, pos_S <= 7))
solver.add(And(pos_T >= 1, pos_T <= 7))
solver.add(And(pos_U >= 1, pos_U <= 7))
solver.add(And(pos_W >= 1, pos_W <= 7))
solver.add(And(pos_X >= 1, pos_X <= 7))
solver.add(And(pos_Z >= 1, pos_Z <= 7))

# All positions must be distinct
solver.add(Distinct([pos_R, pos_S, pos_T, pos_U, pos_W, pos_X, pos_Z]))

# Constraint 1: T cannot be mentioned in chapter 1
solver.add(pos_T != 1)

# Constraint 2: T must be mentioned before W, with exactly two chapters separating T and W
# This means pos_W = pos_T + 3
solver.add(pos_W == pos_T + 3)

# Constraint 3: S and Z cannot be mentioned in adjacent chapters
solver.add(Not(Or(
    And(pos_S + 1 == pos_Z, pos_S >= 1, pos_Z <= 7),
    And(pos_Z + 1 == pos_S, pos_Z >= 1, pos_S <= 7)
)))

# Constraint 4: W and X cannot be mentioned in adjacent chapters
solver.add(Not(Or(
    And(pos_W + 1 == pos_X, pos_W >= 1, pos_X <= 7),
    And(pos_X + 1 == pos_W, pos_X >= 1, pos_W <= 7)
)))

# Constraint 5: U and X must be mentioned in adjacent chapters
solver.add(Or(
    And(pos_U + 1 == pos_X, pos_U >= 1, pos_X <= 7),
    And(pos_X + 1 == pos_U, pos_X >= 1, pos_U <= 7)
))

# All clues must be assigned to some position
solver.add(Or([pos_R == i for i in range(1, 8)]))
solver.add(Or([pos_S == i for i in range(1, 8)]))
solver.add(Or([pos_T == i for i in range(1, 8)]))
solver.add(Or([pos_U == i for i in range(1, 8)]))
solver.add(Or([pos_W == i for i in range(1, 8)]))
solver.add(Or([pos_X == i for i in range(1, 8)]))
solver.add(Or([pos_Z == i for i in range(1, 8)]))

# Base constraints are set. Now test each multiple-choice option.

# Define the options as constraints
# Option A: R is mentioned in chapter 7
opt_A = (pos_R == 7)

# Option B: T is mentioned in chapter 5
opt_B = (pos_T == 5)

# Option C: U is mentioned in chapter 7
opt_C = (pos_U == 7)

# Option D: W is mentioned in chapter 3
opt_D = (pos_W == 3)

# Option E: X is mentioned in chapter 6
opt_E = (pos_X == 6)

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