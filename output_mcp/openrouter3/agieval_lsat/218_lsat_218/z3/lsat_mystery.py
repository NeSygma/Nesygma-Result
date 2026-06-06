from z3 import *

# Create solver
solver = Solver()

# Variables: position of each clue (1-7)
R, S, T, U, W, X, Z = Ints('R S T U W X Z')
clues = [R, S, T, U, W, X, Z]

# Domain constraints: each position between 1 and 7
for clue in clues:
    solver.add(clue >= 1, clue <= 7)

# All clues must have distinct positions
solver.add(Distinct(clues))

# Original constraint: T cannot be in chapter 1
solver.add(T != 1)

# T must be mentioned before W
solver.add(T < W)

# Exactly two chapters separating T and W (so W = T + 3)
solver.add(W == T + 3)

# S and Z cannot be adjacent (|S - Z| != 1)
solver.add(Or(S - Z != 1, Z - S != 1))  # Actually need to ensure absolute difference != 1
# Better: Not(Or(S == Z+1, Z == S+1))
solver.add(Not(Or(S == Z + 1, Z == S + 1)))

# W and X cannot be adjacent
solver.add(Not(Or(W == X + 1, X == W + 1)))

# U and X must be adjacent
solver.add(Or(U == X + 1, X == U + 1))

# Check if original problem is satisfiable
print("Checking original problem with T != 1...")
result = solver.check()
if result == sat:
    print("Original problem is satisfiable")
    m = solver.model()
    print("Example solution:")
    for clue in clues:
        print(f"{clue} = {m[clue]}")
else:
    print("Original problem is unsatisfiable")
    print("This would be a modeling error - need to refine")