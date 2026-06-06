from z3 import *

# Create solver
solver = Solver()

# 4x4 grid of integer variables, values 1..16
grid = [[Int(f"cell_{r}_{c}") for c in range(4)] for r in range(4)]

# Domain: each cell is between 1 and 16
for r in range(4):
    for c in range(4):
        solver.add(grid[r][c] >= 1, grid[r][c] <= 16)

# Constraint 1: All values 1..16 appear exactly once (Distinct)
all_cells = [grid[r][c] for r in range(4) for c in range(4)]
solver.add(Distinct(all_cells))

# Magic constant
M = 34

# Constraint 2: All rows sum to 34
for r in range(4):
    solver.add(Sum([grid[r][c] for c in range(4)]) == M)

# All columns sum to 34
for c in range(4):
    solver.add(Sum([grid[r][c] for r in range(4)]) == M)

# Both main diagonals sum to 34
solver.add(Sum([grid[i][i] for i in range(4)]) == M)
solver.add(Sum([grid[i][3 - i] for i in range(4)]) == M)

# Constraint 3: Symmetrical pairs sum to 17
# Using 0-based indexing: cell (r,c) opposite to (3-r, 3-c)
for r in range(4):
    for c in range(4):
        # Only add each pair once to avoid redundant constraints
        if r < 3 - r or (r == 3 - r and c < 3 - c):
            solver.add(grid[r][c] + grid[3 - r][3 - c] == 17)

# Constraint 4: Quadrant sums = 34
# Top-Left: (0,0),(0,1),(1,0),(1,1)
solver.add(Sum([grid[0][0], grid[0][1], grid[1][0], grid[1][1]]) == M)
# Top-Right: (0,2),(0,3),(1,2),(1,3)
solver.add(Sum([grid[0][2], grid[0][3], grid[1][2], grid[1][3]]) == M)
# Bottom-Left: (2,0),(2,1),(3,0),(3,1)
solver.add(Sum([grid[2][0], grid[2][1], grid[3][0], grid[3][1]]) == M)
# Bottom-Right: (2,2),(2,3),(3,2),(3,3)
solver.add(Sum([grid[2][2], grid[2][3], grid[3][2], grid[3][3]]) == M)

# Constraint 5: Small primes {2,3,5,7} forbidden from corners
# Corners: (0,0), (0,3), (3,0), (3,3)
corners = [(0,0), (0,3), (3,0), (3,3)]
small_primes = [2, 3, 5, 7]
for (r, c) in corners:
    for p in small_primes:
        solver.add(grid[r][c] != p)

# Solve
BENCHMARK_MODE = True
result = solver.check()

if result == sat:
    m = solver.model()
    print("STATUS: sat")
    print("Solution found:")
    for r in range(4):
        row_vals = [m.eval(grid[r][c]).as_long() for c in range(4)]
        print(" ".join(f"{v:2d}" for v in row_vals))
    
    # Validate all constraints for output
    print()
    # Check magic sums
    print("Row sums:", [sum(m.eval(grid[r][c]).as_long() for c in range(4)) for r in range(4)])
    print("Col sums:", [sum(m.eval(grid[r][c]).as_long() for r in range(4)) for c in range(4)])
    print("Diag1 sum:", sum(m.eval(grid[i][i]).as_long() for i in range(4)))
    print("Diag2 sum:", sum(m.eval(grid[i][3-i]).as_long() for i in range(4)))
    
    # Check symmetrical pairs
    sym_ok = True
    for r in range(4):
        for c in range(4):
            if r < 3 - r or (r == 3 - r and c < 3 - c):
                v1 = m.eval(grid[r][c]).as_long()
                v2 = m.eval(grid[3-r][3-c]).as_long()
                if v1 + v2 != 17:
                    sym_ok = False
    print("Symmetrical pairs sum to 17:", sym_ok)
    
    # Check quadrant sums
    q1 = sum(m.eval(grid[r][c]).as_long() for r in range(2) for c in range(2))
    q2 = sum(m.eval(grid[r][c]).as_long() for r in range(2) for c in range(2,4))
    q3 = sum(m.eval(grid[r][c]).as_long() for r in range(2,4) for c in range(2))
    q4 = sum(m.eval(grid[r][c]).as_long() for r in range(2,4) for c in range(2,4))
    print(f"Quadrant sums: TL={q1}, TR={q2}, BL={q3}, BR={q4}")
    
    # Check prime placement
    corner_vals = [m.eval(grid[r][c]).as_long() for (r,c) in corners]
    primes_in_corners = [v for v in corner_vals if v in small_primes]
    print(f"Corner values: {corner_vals}")
    print(f"Small primes in corners: {primes_in_corners}")
    
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")