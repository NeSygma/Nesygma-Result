from z3 import *

# BENCHMARK_MODE: ON (model-finding mode)
BENCHMARK_MODE = True

# Create an 8x8 grid of integer variables (1-8)
grid = [[Int(f"grid_{i}_{j}") for j in range(8)] for i in range(8)]

solver = Solver()

# 1. Pre-filled cells (1-indexed in problem, 0-indexed in code)
prefilled = {
    (0, 0): 1,   # (1,1) = 1
    (0, 7): 8,   # (1,8) = 8
    (1, 1): 6,   # (2,2) = 6
    (2, 2): 4,   # (3,3) = 4
    (3, 3): 5,   # (4,4) = 5
    (4, 4): 7,   # (5,5) = 7
    (5, 5): 4,   # (6,6) = 4
    (6, 6): 6,   # (7,7) = 6
    (7, 7): 3,   # (8,8) = 3
    (7, 0): 8,   # (8,1) = 8
}

for (i, j), val in prefilled.items():
    solver.add(grid[i][j] == val)

# 2. Latin Square Constraint: Each row and column must contain 1-8 exactly once
for i in range(8):
    solver.add(Distinct(grid[i]))  # Row constraint

for j in range(8):
    solver.add(Distinct([grid[i][j] for i in range(8)]))  # Column constraint

# 3. Adjacent Pair Sum Constraint: grid[r][c] + grid[r][c+1] > 5 for all valid r, c
for i in range(8):
    for j in range(7):
        solver.add(grid[i][j] + grid[i][j+1] > 5)

# 4. Quadrant Parity Constraint
# Top-left quadrant (rows 0-3, columns 0-3): exactly 8 even numbers
# Bottom-right quadrant (rows 4-7, columns 4-7): exactly 8 odd numbers

top_left_quadrant = [grid[i][j] for i in range(4) for j in range(4)]
bottom_right_quadrant = [grid[i][j] for i in range(4, 8) for j in range(4, 8)]

# Count even numbers in top-left quadrant
solver.add(Sum([If(And(grid[i][j] % 2 == 0, 0 <= i, i < 4, 0 <= j, j < 4), 1, 0) for i in range(8) for j in range(8)]) == 8)

# Count odd numbers in bottom-right quadrant
solver.add(Sum([If(And(grid[i][j] % 2 == 1, 4 <= i, i < 8, 4 <= j, j < 8), 1, 0) for i in range(8) for j in range(8)]) == 8)

# 5. Partial Sum Constraint
# Sum of first four cells in row 1 (0-indexed row 0) must be 14
solver.add(Sum([grid[0][j] for j in range(4)]) == 14)

# Sum of first four cells in column 1 (0-indexed column 0) must be 10
solver.add(Sum([grid[i][0] for i in range(4)]) == 10)

# Ensure all cells are between 1 and 8
for i in range(8):
    for j in range(8):
        solver.add(grid[i][j] >= 1, grid[i][j] <= 8)

# Check for a solution
result = solver.check()

if result == sat:
    model = solver.model()
    print("STATUS: sat")
    # Print the grid in a readable format
    for i in range(8):
        row = []
        for j in range(8):
            row.append(str(model[grid[i][j]]))
        print("row_{}: {}".format(i+1, " ".join(row)))
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")