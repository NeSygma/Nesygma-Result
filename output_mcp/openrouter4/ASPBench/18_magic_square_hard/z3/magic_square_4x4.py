from z3 import *

# Create solver
solver = Solver()

# Grid: 4x4, indexed 0..3 for rows and columns (0-based internally, 1-based problem)
# We create a Python list of lists of Ints
grid = [[Int(f"cell_{r}_{c}") for c in range(4)] for r in range(4)]

# Constants
N = 4
MAGIC = 34
MIN_VAL = 1
MAX_VAL = 16

# Constraint 1: Each cell gets a value from 1 to 16
for r in range(N):
    for c in range(N):
        solver.add(grid[r][c] >= MIN_VAL, grid[r][c] <= MAX_VAL)

# Constraint 1: All values are distinct (each integer 1-16 used exactly once)
all_cells = [grid[r][c] for r in range(N) for c in range(N)]
solver.add(Distinct(all_cells))

# Constraint 2: All rows sum to 34
for r in range(N):
    solver.add(Sum([grid[r][c] for c in range(N)]) == MAGIC)

# Constraint 2: All columns sum to 34
for c in range(N):
    solver.add(Sum([grid[r][c] for r in range(N)]) == MAGIC)

# Constraint 2: Both main diagonals sum to 34
solver.add(Sum([grid[i][i] for i in range(N)]) == MAGIC)          # main diagonal
solver.add(Sum([grid[i][N-1-i] for i in range(N)]) == MAGIC)     # anti-diagonal

# Constraint 3: Symmetrical pairs sum to 17
# Cell (r, c) opposite to cell (N-1-r, N-1-c) in 0-based indexing
# Problem says: cell (r,c) opposite to (5-r, 5-c) with 1-based indexing
# In 0-based: (r,c) opposite to (3-r, 3-c)
for r in range(N):
    for c in range(N):
        # To avoid double-adding the constraint, only do it for r < (N-1-r) or 
        # r == (N-1-r) and c < (N-1-c) — but actually symmetrical pairs are distinct
        # unless the cell is its own opposite, which only happens at center of odd grid
        # For a 4x4 grid, no cell is its own opposite, so we can just do all
        # But to be clean, let's add once per pair
        opp_r = N - 1 - r
        opp_c = N - 1 - c
        if (r < opp_r) or (r == opp_r and c < opp_c):
            solver.add(grid[r][c] + grid[opp_r][opp_c] == 17)

# Constraint 4: Quadrant sums = 34
# Top-Left: (0,0),(0,1),(1,0),(1,1)
solver.add(Sum([grid[0][0], grid[0][1], grid[1][0], grid[1][1]]) == MAGIC)
# Top-Right: (0,2),(0,3),(1,2),(1,3)
solver.add(Sum([grid[0][2], grid[0][3], grid[1][2], grid[1][3]]) == MAGIC)
# Bottom-Left: (2,0),(2,1),(3,0),(3,1)
solver.add(Sum([grid[2][0], grid[2][1], grid[3][0], grid[3][1]]) == MAGIC)
# Bottom-Right: (2,2),(2,3),(3,2),(3,3)
solver.add(Sum([grid[2][2], grid[2][3], grid[3][2], grid[3][3]]) == MAGIC)

# Constraint 5: Small primes {2,3,5,7} forbidden from corners
# Corners (0-based): (0,0), (0,3), (3,0), (3,3)
corners = [(0,0), (0,3), (3,0), (3,3)]
small_primes = [2, 3, 5, 7]
for (r, c) in corners:
    for p in small_primes:
        solver.add(grid[r][c] != p)

# Solve and output
BENCHMARK_MODE = True
result = solver.check()

if result == sat:
    m = solver.model()
    print("STATUS: sat")
    print("Solution found!")
    print()
    # Print the grid
    print("Grid:")
    for r in range(N):
        row_vals = [m.eval(grid[r][c]).as_long() for c in range(N)]
        print("  " + " ".join(f"{v:2d}" for v in row_vals))
    
    # Print validation info
    print()
    print("Validation:")
    
    # Rows
    print("  Row sums:", [sum(m.eval(grid[r][c]).as_long() for c in range(N)) for r in range(N)])
    
    # Columns
    col_sums = []
    for c in range(N):
        col_sum = sum(m.eval(grid[r][c]).as_long() for r in range(N))
        col_sums.append(col_sum)
    print("  Column sums:", col_sums)
    
    # Diagonals
    main_diag = sum(m.eval(grid[i][i]).as_long() for i in range(N))
    anti_diag = sum(m.eval(grid[i][N-1-i]).as_long() for i in range(N))
    print("  Main diagonal sum:", main_diag)
    print("  Anti-diagonal sum:", anti_diag)
    
    # Symmetrical pairs
    print("  Opposite pairs (should sum to 17):")
    sym_ok = True
    for r in range(N):
        for c in range(N):
            opp_r = N - 1 - r
            opp_c = N - 1 - c
            if (r < opp_r) or (r == opp_r and c < opp_c):
                v1 = m.eval(grid[r][c]).as_long()
                v2 = m.eval(grid[opp_r][opp_c]).as_long()
                if v1 + v2 != 17:
                    sym_ok = False
                print(f"    ({r+1},{c+1})={v1} + ({opp_r+1},{opp_c+1})={v2} = {v1+v2}")
    print("  Symmetrical pairs valid:", sym_ok)
    
    # Quadrant sums
    print("  Quadrant sums (should all be 34):")
    quadrants = [
        ("Top-Left", [(0,0),(0,1),(1,0),(1,1)]),
        ("Top-Right", [(0,2),(0,3),(1,2),(1,3)]),
        ("Bottom-Left", [(2,0),(2,1),(3,0),(3,1)]),
        ("Bottom-Right", [(2,2),(2,3),(3,2),(3,3)])
    ]
    quad_ok = True
    for name, cells in quadrants:
        s = sum(m.eval(grid[r][c]).as_long() for (r,c) in cells)
        if s != 34:
            quad_ok = False
        print(f"    {name}: {s}")
    print("  Quadrant sums valid:", quad_ok)
    
    # Prime placement
    print("  Corner values:", end=" ")
    prime_ok = True
    for (r,c) in corners:
        v = m.eval(grid[r][c]).as_long()
        if v in small_primes:
            prime_ok = False
        print(f"({r+1},{c+1})={v}", end=" ")
    print()
    print("  Prime placement valid:", prime_ok)
    
    print()
    print("Overall valid:", sym_ok and quad_ok and prime_ok)
    
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")