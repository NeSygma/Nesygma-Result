from z3 import *

# Create solver
solver = Solver()

# 4x4 grid of Int variables
n = 4
grid = [[Int(f"c_{r}_{c}") for c in range(n)] for r in range(n)]

# Domain constraints: each cell 1..16
cells = [grid[r][c] for r in range(n) for c in range(n)]
for cell in cells:
    solver.add(cell >= 1, cell <= 16)

# All distinct
solver.add(Distinct(cells))

# Magic sum constant
MAGIC = 34

# Row sums
for r in range(n):
    solver.add(Sum(grid[r]) == MAGIC)

# Column sums
for c in range(n):
    solver.add(Sum([grid[r][c] for r in range(n)]) == MAGIC)

# Diagonals
solver.add(Sum([grid[i][i] for i in range(n)]) == MAGIC)
solver.add(Sum([grid[i][n-1-i] for i in range(n)]) == MAGIC)

# Symmetrical pairs: opposite cells sum to 17
for r in range(n):
    for c in range(n):
        opp_r = n-1 - r
        opp_c = n-1 - c
        # add constraint only once per pair (e.g., when (r,c) <= (opp_r,opp_c) in lex order)
        if (r < opp_r) or (r == opp_r and c <= opp_c):
            solver.add(grid[r][c] + grid[opp_r][opp_c] == 17)

# Quadrant sums (2x2 blocks) each 34
# Top-left block rows 0-1, cols 0-1
solver.add(Sum([grid[r][c] for r in range(0,2) for c in range(0,2)]) == MAGIC)
# Top-right rows 0-1, cols 2-3
solver.add(Sum([grid[r][c] for r in range(0,2) for c in range(2,4)]) == MAGIC)
# Bottom-left rows 2-3, cols 0-1
solver.add(Sum([grid[r][c] for r in range(2,4) for c in range(0,2)]) == MAGIC)
# Bottom-right rows 2-3, cols 2-3
solver.add(Sum([grid[r][c] for r in range(2,4) for c in range(2,4)]) == MAGIC)

# Prime placement: corners not in {2,3,5,7}
prime_set = {2,3,5,7}
corner_coords = [(0,0),(0,3),(3,0),(3,3)]
for (r,c) in corner_coords:
    for p in prime_set:
        solver.add(grid[r][c] != p)

# Check
result = solver.check()
if result == sat:
    m = solver.model()
    print("STATUS: sat")
    # Print grid rows
    for r in range(n):
        row_vals = [m.eval(grid[r][c]).as_long() for c in range(n)]
        print(' '.join(map(str, row_vals)))
else:
    print("STATUS: unsat" if result == unsat else "STATUS: unknown")