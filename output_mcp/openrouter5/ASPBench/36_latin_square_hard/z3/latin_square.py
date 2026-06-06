from z3 import *

# Create solver
solver = Solver()

# 8x8 grid of integer variables, values 1..8
grid = [[Int(f"grid_{i}_{j}") for j in range(8)] for i in range(8)]

# Domain: each cell is 1..8
for i in range(8):
    for j in range(8):
        solver.add(grid[i][j] >= 1, grid[i][j] <= 8)

# 1. Latin Square: each row and each column has all numbers 1..8 exactly once
for i in range(8):
    solver.add(Distinct([grid[i][j] for j in range(8)]))

for j in range(8):
    solver.add(Distinct([grid[i][j] for i in range(8)]))

# 2. Adjacent Pair Sum Constraint: grid[r][c] + grid[r][c+1] > 5
for r in range(8):
    for c in range(7):
        solver.add(grid[r][c] + grid[r][c+1] > 5)

# 3. Quadrant Parity Constraints
# Top-left quadrant (rows 0-3, cols 0-3): exactly 8 even numbers
top_left_even_count = Sum([If(grid[i][j] % 2 == 0, 1, 0) for i in range(4) for j in range(4)])
solver.add(top_left_even_count == 8)

# Bottom-right quadrant (rows 4-7, cols 4-7): exactly 8 odd numbers
bottom_right_odd_count = Sum([If(grid[i][j] % 2 == 1, 1, 0) for i in range(4, 8) for j in range(4, 8)])
solver.add(bottom_right_odd_count == 8)

# 4. Partial Sum Constraints
# Row 1 (index 0): sum of first 4 cells = 14
solver.add(grid[0][0] + grid[0][1] + grid[0][2] + grid[0][3] == 14)

# Column 1 (index 0): sum of first 4 cells = 10
solver.add(grid[0][0] + grid[1][0] + grid[2][0] + grid[3][0] == 10)

# Pre-filled cells (1-indexed -> 0-indexed)
# (1,1) = 1
solver.add(grid[0][0] == 1)
# (1,8) = 8
solver.add(grid[0][7] == 8)
# (2,2) = 6
solver.add(grid[1][1] == 6)
# (3,3) = 4
solver.add(grid[2][2] == 4)
# (4,4) = 5
solver.add(grid[3][3] == 5)
# (5,5) = 7
solver.add(grid[4][4] == 7)
# (6,6) = 4
solver.add(grid[5][5] == 4)
# (7,7) = 6
solver.add(grid[6][6] == 6)
# (8,8) = 3
solver.add(grid[7][7] == 3)
# (8,1) = 8
solver.add(grid[7][0] == 8)

# Solve
BENCHMARK_MODE = True
result = solver.check()

if result == sat:
    m = solver.model()
    print("STATUS: sat")
    print("Solution found:")
    for i in range(8):
        row_vals = [str(m.eval(grid[i][j])) for j in range(8)]
        print(" ".join(row_vals))
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")