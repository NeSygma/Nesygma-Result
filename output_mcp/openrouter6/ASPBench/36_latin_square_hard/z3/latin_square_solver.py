from z3 import *

# Create solver
solver = Solver()

# 8x8 grid with numbers 1-8
grid = [[Int(f'grid_{i}_{j}') for j in range(8)] for i in range(8)]

# Domain constraints: each cell between 1 and 8
for i in range(8):
    for j in range(8):
        solver.add(grid[i][j] >= 1, grid[i][j] <= 8)

# Pre-filled cells (1-indexed to 0-indexed)
prefilled = [
    (0, 0, 1),   # (1,1) = 1
    (0, 7, 8),   # (1,8) = 8
    (1, 1, 6),   # (2,2) = 6
    (2, 2, 4),   # (3,3) = 4
    (3, 3, 5),   # (4,4) = 5
    (4, 4, 7),   # (5,5) = 7
    (5, 5, 4),   # (6,6) = 4
    (6, 6, 6),   # (7,7) = 6
    (7, 7, 3),   # (8,8) = 3
    (7, 0, 8),   # (8,1) = 8
]

for i, j, val in prefilled:
    solver.add(grid[i][j] == val)

# 1. Latin square constraint: each row and column must contain 1..8 exactly once
for i in range(8):
    solver.add(Distinct([grid[i][j] for j in range(8)]))
for j in range(8):
    solver.add(Distinct([grid[i][j] for i in range(8)]))

# 2. Adjacent pair sum constraint: grid[r][c] + grid[r][c+1] > 5
for r in range(8):
    for c in range(7):  # columns 0-6
        solver.add(grid[r][c] + grid[r][c+1] > 5)

# 3. Quadrant parity constraints
# Top-left quadrant (rows 0-3, cols 0-3): exactly 8 even numbers
top_left_cells = [grid[i][j] for i in range(4) for j in range(4)]
# Count even numbers using If
even_count_tl = Sum([If(cell % 2 == 0, 1, 0) for cell in top_left_cells])
solver.add(even_count_tl == 8)

# Bottom-right quadrant (rows 4-7, cols 4-7): exactly 8 odd numbers
bottom_right_cells = [grid[i][j] for i in range(4, 8) for j in range(4, 8)]
odd_count_br = Sum([If(cell % 2 == 1, 1, 0) for cell in bottom_right_cells])
solver.add(odd_count_br == 8)

# 4. Partial sum constraints
# Row 1 (index 0): sum of first 4 cells = 14
solver.add(Sum([grid[0][j] for j in range(4)]) == 14)
# Column 1 (index 0): sum of first 4 cells = 10
solver.add(Sum([grid[i][0] for i in range(4)]) == 10)

# Check satisfiability
result = solver.check()
print(f"Solver result: {result}")

if result == sat:
    model = solver.model()
    print("STATUS: sat")
    print("Solution found:")
    for i in range(8):
        row_vals = [model.eval(grid[i][j]) for j in range(8)]
        print(f"Row {i+1}: {row_vals}")
elif result == unsat:
    print("STATUS: unsat")
    print("No solution exists")
else:
    print("STATUS: unknown")
    print("Solver returned unknown")