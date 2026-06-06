from z3 import *

# Grid size
N = 4
# Values 1-16
vals = range(1, 17)

# Create 4x4 grid
grid = [[Int(f'cell_{r}_{c}') for c in range(N)] for r in range(N)]

solver = Solver()

# 1. Uniqueness: Each integer from 1 to 16 must appear exactly once
flat_grid = [grid[r][c] for r in range(N) for c in range(N)]
solver.add(Distinct(flat_grid))
for cell in flat_grid:
    solver.add(cell >= 1, cell <= 16)

# 2. Magic sum: All rows, columns, and diagonals sum to 34
magic_constant = 34
for i in range(N):
    solver.add(Sum(grid[i]) == magic_constant) # Rows
    solver.add(Sum([grid[r][i] for r in range(N)]) == magic_constant) # Columns

solver.add(Sum([grid[i][i] for i in range(N)]) == magic_constant) # Main diagonal
solver.add(Sum([grid[i][N-1-i] for i in range(N)]) == magic_constant) # Anti-diagonal

# 3. Symmetrical pairs: Diametrically opposite cells sum to 17
# (r, c) is opposite to (3-r, 3-c) in 0-based indexing
for r in range(N):
    for c in range(N):
        solver.add(grid[r][c] + grid[N-1-r][N-1-c] == 17)

# 4. Quadrant sums: Each 2x2 quadrant sums to 34
# Top-Left: (0,0), (0,1), (1,0), (1,1)
# Top-Right: (0,2), (0,3), (1,2), (1,3)
# Bottom-Left: (2,0), (2,1), (3,0), (3,1)
# Bottom-Right: (2,2), (2,3), (3,2), (3,3)
quadrants = [
    [(0,0), (0,1), (1,0), (1,1)],
    [(0,2), (0,3), (1,2), (1,3)],
    [(2,0), (2,1), (3,0), (3,1)],
    [(2,2), (2,3), (3,2), (3,3)]
]
for quad in quadrants:
    solver.add(Sum([grid[r][c] for r, c in quad]) == magic_constant)

# 5. Prime placement: {2, 3, 5, 7} forbidden from corners (0,0), (0,3), (3,0), (3,3)
corners = [(0,0), (0,3), (3,0), (3,3)]
small_primes = [2, 3, 5, 7]
for r, c in corners:
    for p in small_primes:
        solver.add(grid[r][c] != p)

# Solve
result = solver.check()
if result == sat:
    print("STATUS: sat")
    m = solver.model()
    for r in range(N):
        row_vals = [m.evaluate(grid[r][c]).as_long() for c in range(N)]
        print(row_vals)
else:
    print("STATUS: unsat")