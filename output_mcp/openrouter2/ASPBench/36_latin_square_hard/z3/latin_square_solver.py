from z3 import *

# Define grid variables
N = 8
grid = [[Int(f"g_{i}_{j}") for j in range(N)] for i in range(N)]

solver = Solver()

# Domain constraints
for i in range(N):
    for j in range(N):
        solver.add(grid[i][j] >= 1, grid[i][j] <= 8)

# Latin square constraints: each row and column distinct
for i in range(N):
    solver.add(Distinct(grid[i]))
for j in range(N):
    col = [grid[i][j] for i in range(N)]
    solver.add(Distinct(col))

# Pre-filled cells (1-indexed to 0-indexed)
pre_filled = {
    (0,0):1,
    (0,7):8,
    (1,1):6,
    (2,2):4,
    (3,3):5,
    (4,4):7,
    (5,5):4,
    (6,6):6,
    (7,7):3,
    (7,0):8,
}
for (i,j), val in pre_filled.items():
    solver.add(grid[i][j] == val)

# Adjacent pair sum constraint (horizontal only)
for i in range(N):
    for j in range(N-1):
        solver.add(grid[i][j] + grid[i][j+1] > 5)

# Quadrant parity constraints
# Top-left quadrant rows 0-3, cols 0-3: exactly 8 even numbers
even_count_tl = Sum([If(grid[i][j] % 2 == 0, 1, 0) for i in range(4) for j in range(4)])
solver.add(even_count_tl == 8)
# Bottom-right quadrant rows 4-7, cols 4-7: exactly 8 odd numbers
odd_count_br = Sum([If(grid[i][j] % 2 == 1, 1, 0) for i in range(4,8) for j in range(4,8)])
solver.add(odd_count_br == 8)

# Partial sum constraints
# Row 0 first four cells sum 14
solver.add(Sum([grid[0][j] for j in range(4)]) == 14)
# Column 0 first four cells sum 10
solver.add(Sum([grid[i][0] for i in range(4)]) == 10)

# Solve
result = solver.check()
if result == sat:
    m = solver.model()
    print("STATUS: sat")
    # Print grid rows
    for i in range(N):
        row_vals = [str(m[grid[i][j]]) for j in range(N)]
        print(" ".join(row_vals))
else:
    print("STATUS: unsat")
    if result == unknown:
        print("RAW_RESULT: unknown")
    else:
        print("RAW_RESULT: unsat")