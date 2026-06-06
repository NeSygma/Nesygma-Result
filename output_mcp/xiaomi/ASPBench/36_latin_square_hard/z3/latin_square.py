from z3 import *

solver = Solver()

# Create 8x8 grid of integer variables
grid = [[Int(f"grid_{i}_{j}") for j in range(8)] for i in range(8)]

# Domain constraints: each cell must be between 1 and 8
for i in range(8):
    for j in range(8):
        solver.add(grid[i][j] >= 1, grid[i][j] <= 8)

# Latin Square Constraint: each row has all numbers 1-8
for i in range(8):
    solver.add(Distinct([grid[i][j] for j in range(8)]))

# Latin Square Constraint: each column has all numbers 1-8
for j in range(8):
    solver.add(Distinct([grid[i][j] for i in range(8)]))

# Pre-filled cells (converting 1-indexed to 0-indexed)
solver.add(grid[0][0] == 1)   # (1,1) = 1
solver.add(grid[0][7] == 8)   # (1,8) = 8
solver.add(grid[1][1] == 6)   # (2,2) = 6
solver.add(grid[2][2] == 4)   # (3,3) = 4
solver.add(grid[3][3] == 5)   # (4,4) = 5
solver.add(grid[4][4] == 7)   # (5,5) = 7
solver.add(grid[5][5] == 4)   # (6,6) = 4
solver.add(grid[6][6] == 6)   # (7,7) = 6
solver.add(grid[7][7] == 3)   # (8,8) = 3
solver.add(grid[7][0] == 8)   # (8,1) = 8

# Adjacent Pair Sum Constraint: grid[r][c] + grid[r][c+1] > 5
for i in range(8):
    for j in range(7):
        solver.add(grid[i][j] + grid[i][j+1] > 5)

# Quadrant Parity Constraint
# Top-left quadrant (rows 0-3, cols 0-3): exactly 8 even numbers
even_count_tl = Sum([If(grid[i][j] % 2 == 0, 1, 0) for i in range(4) for j in range(4)])
solver.add(even_count_tl == 8)

# Bottom-right quadrant (rows 4-7, cols 4-7): exactly 8 odd numbers
odd_count_br = Sum([If(grid[i][j] % 2 != 0, 1, 0) for i in range(4, 8) for j in range(4, 8)])
solver.add(odd_count_br == 8)

# Partial Sum Constraints
# Sum of first four cells in row 1 (0-indexed row 0) = 14
solver.add(grid[0][0] + grid[0][1] + grid[0][2] + grid[0][3] == 14)

# Sum of first four cells in column 1 (0-indexed col 0) = 10
solver.add(grid[0][0] + grid[1][0] + grid[2][0] + grid[3][0] == 10)

# Solve
BENCHMARK_MODE = True
result = solver.check()

if result == sat:
    model = solver.model()
    print("STATUS: sat")
    print("Solution found:")
    for i in range(8):
        row = [model[grid[i][j]] for j in range(8)]
        print(f"Row {i+1}: {row}")
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")