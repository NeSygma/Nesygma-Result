from z3 import *

# Create the solver
solver = Solver()

# 8x8 grid
grid = [[Int(f"grid_{r}_{c}") for c in range(8)] for r in range(8)]

# Domain constraints: 1 to 8
for r in range(8):
    for c in range(8):
        solver.add(grid[r][c] >= 1, grid[r][c] <= 8)

# Latin Square Constraint
for r in range(8):
    solver.add(Distinct(grid[r]))
for c in range(8):
    solver.add(Distinct([grid[r][c] for r in range(8)]))

# Pre-filled cells (1-indexed in problem, 0-indexed here)
# (1,1) = 1 -> (0,0) = 1
# (1,8) = 8 -> (0,7) = 8
# (2,2) = 6 -> (1,1) = 6
# (3,3) = 4 -> (2,2) = 4
# (4,4) = 5 -> (3,3) = 5
# (5,5) = 7 -> (4,4) = 7
# (6,6) = 4 -> (5,5) = 4
# (7,7) = 6 -> (6,6) = 6
# (8,8) = 3 -> (7,7) = 3
# (8,1) = 8 -> (7,0) = 8
solver.add(grid[0][0] == 1)
solver.add(grid[0][7] == 8)
solver.add(grid[1][1] == 6)
solver.add(grid[2][2] == 4)
solver.add(grid[3][3] == 5)
solver.add(grid[4][4] == 7)
solver.add(grid[5][5] == 4)
solver.add(grid[6][6] == 6)
solver.add(grid[7][7] == 3)
solver.add(grid[7][0] == 8)

# Adjacent Pair Sum Constraint: grid[r][c] + grid[r][c+1] > 5
for r in range(8):
    for c in range(7):
        solver.add(grid[r][c] + grid[r][c+1] > 5)

# Quadrant Parity Constraint
# Top-left (rows 0-3, cols 0-3): exactly 8 even numbers
solver.add(Sum([If(grid[r][c] % 2 == 0, 1, 0) for r in range(4) for c in range(4)]) == 8)
# Bottom-right (rows 4-7, cols 4-7): exactly 8 odd numbers
solver.add(Sum([If(grid[r][c] % 2 != 0, 1, 0) for r in range(4, 8) for c in range(4, 8)]) == 8)

# Partial Sum Constraint
# Row 1 (0), cols 1-4 (0-3): sum = 14
solver.add(Sum([grid[0][c] for c in range(4)]) == 14)
# Col 1 (0), rows 1-4 (0-3): sum = 10
solver.add(Sum([grid[r][0] for r in range(4)]) == 10)

# Solve
result = solver.check()
if result == sat:
    print("STATUS: sat")
    model = solver.model()
    for r in range(8):
        row_vals = [model.evaluate(grid[r][c]).as_long() for c in range(8)]
        print(row_vals)
else:
    print("STATUS: unsat")