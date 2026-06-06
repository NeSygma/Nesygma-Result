from z3 import *

# Create a 3x3 grid of integer variables
square = [[Int(f"cell_{i}_{j}") for j in range(3)] for i in range(3)]

solver = Solver()
MAGIC_SUM = 15

# 1. Each cell must contain a number from 1 to 9
for i in range(3):
    for j in range(3):
        solver.add(square[i][j] >= 1)
        solver.add(square[i][j] <= 9)

# 2. Each number 1-9 appears exactly once (all cells distinct)
all_cells = [square[i][j] for i in range(3) for j in range(3)]
solver.add(Distinct(all_cells))

# 3. All three rows must sum to 15
for i in range(3):
    solver.add(Sum([square[i][j] for j in range(3)]) == MAGIC_SUM)

# 4. All three columns must sum to 15
for j in range(3):
    solver.add(Sum([square[i][j] for i in range(3)]) == MAGIC_SUM)

# 5. Both diagonals must sum to 15
solver.add(Sum([square[i][i] for i in range(3)]) == MAGIC_SUM)
solver.add(Sum([square[i][2 - i] for i in range(3)]) == MAGIC_SUM)

BENCHMARK_MODE = True
result = solver.check()

if result == sat:
    m = solver.model()
    print("STATUS: sat")
    print("Solution found (3x3 magic square):")
    for i in range(3):
        row = [str(m.eval(square[i][j])) for j in range(3)]
        print(" ".join(row))
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")