from z3 import *

# Create a 5x5 grid of integer variables
grid = [[Int(f"grid_{i}_{j}") for j in range(5)] for i in range(5)]

solver = Solver()

# Domain: each cell must be between 1 and 5
for i in range(5):
    for j in range(5):
        solver.add(grid[i][j] >= 1, grid[i][j] <= 5)

# Given fixed values
solver.add(grid[0][0] == 1)  # Cell (1,1)
solver.add(grid[1][2] == 3)  # Cell (2,3)
solver.add(grid[2][3] == 4)  # Cell (3,4)
solver.add(grid[3][4] == 5)  # Cell (4,5)
solver.add(grid[4][1] == 2)  # Cell (5,2)

# Each row must contain numbers 1..5 exactly once
for i in range(5):
    solver.add(Distinct([grid[i][j] for j in range(5)]))

# Each column must contain numbers 1..5 exactly once
for j in range(5):
    solver.add(Distinct([grid[i][j] for i in range(5)]))

BENCHMARK_MODE = True
result = solver.check()

if result == sat:
    m = solver.model()
    print("STATUS: sat")
    print("solved: True")
    print("grid:")
    for i in range(5):
        row = [m.eval(grid[i][j]).as_long() for j in range(5)]
        print(row)
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")