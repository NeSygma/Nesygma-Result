from z3 import *

solver = Solver()

# 4x4 grid of integers
grid = [[Int(f"cell_{r}_{c}") for c in range(4)] for r in range(4)]

# Constraint 1: Each cell is between 1 and 16
for r in range(4):
    for c in range(4):
        solver.add(grid[r][c] >= 1, grid[r][c] <= 16)

# Constraint 2: All values distinct (each 1-16 used exactly once)
all_cells = [grid[r][c] for r in range(4) for c in range(4)]
solver.add(Distinct(all_cells))

# Constraint 3: All rows sum to 34
for r in range(4):
    solver.add(Sum([grid[r][c] for c in range(4)]) == 34)

# Constraint 4: All columns sum to 34
for c in range(4):
    solver.add(Sum([grid[r][c] for r in range(4)]) == 34)

# Constraint 5: Both main diagonals sum to 34
solver.add(Sum([grid[i][i] for i in range(4)]) == 34)
solver.add(Sum([grid[i][3 - i] for i in range(4)]) == 34)

# Constraint 6: Symmetrical pairs - diametrically opposite cells sum to 17
# Cell (r,c) is opposite to cell (3-r, 3-c) in 0-based indexing
for r in range(4):
    for c in range(4):
        solver.add(grid[r][c] + grid[3 - r][3 - c] == 17)

# Constraint 7: Each 2x2 quadrant sums to 34
# Top-Left: (0,0), (0,1), (1,0), (1,1)
solver.add(grid[0][0] + grid[0][1] + grid[1][0] + grid[1][1] == 34)
# Top-Right: (0,2), (0,3), (1,2), (1,3)
solver.add(grid[0][2] + grid[0][3] + grid[1][2] + grid[1][3] == 34)
# Bottom-Left: (2,0), (2,1), (3,0), (3,1)
solver.add(grid[2][0] + grid[2][1] + grid[3][0] + grid[3][1] == 34)
# Bottom-Right: (2,2), (2,3), (3,2), (3,3)
solver.add(grid[2][2] + grid[2][3] + grid[3][2] + grid[3][3] == 34)

# Constraint 8: Small primes {2, 3, 5, 7} forbidden in corners
# Corners (0-based): (0,0), (0,3), (3,0), (3,3)
small_primes = [2, 3, 5, 7]
corners = [(0, 0), (0, 3), (3, 0), (3, 3)]
for (r, c) in corners:
    for p in small_primes:
        solver.add(grid[r][c] != p)

BENCHMARK_MODE = True
result = solver.check()

if result == sat:
    m = solver.model()
    print("STATUS: sat")
    print("Magic square found:")
    for r in range(4):
        row_vals = [m[grid[r][c]].as_long() for c in range(4)]
        print(f"  Row {r+1}: {row_vals}")
    
    # Validate properties
    square = [[m[grid[r][c]].as_long() for c in range(4)] for r in range(4)]
    
    # Check symmetrical pairs
    sym_ok = True
    for r in range(4):
        for c in range(4):
            if square[r][c] + square[3-r][3-c] != 17:
                sym_ok = False
    print(f"is_symmetrical_pairs: {sym_ok}")
    
    # Check quadrant sums
    quad_ok = True
    for qr, qc in [(0,0),(0,2),(2,0),(2,2)]:
        s = sum(square[qr+i][qc+j] for i in range(2) for j in range(2))
        if s != 34:
            quad_ok = False
    print(f"is_quadrant_sum_valid: {quad_ok}")
    
    # Check prime placement
    prime_ok = True
    for (r, c) in corners:
        if square[r][c] in small_primes:
            prime_ok = False
    print(f"is_prime_placement_valid: {prime_ok}")
    
    # Check magic sums
    magic_ok = True
    for r in range(4):
        if sum(square[r]) != 34:
            magic_ok = False
    for c in range(4):
        if sum(square[r][c] for r in range(4)) != 34:
            magic_ok = False
    if sum(square[i][i] for i in range(4)) != 34:
        magic_ok = False
    if sum(square[i][3-i] for i in range(4)) != 34:
        magic_ok = False
    print(f"is_magic_sum_valid: {magic_ok}")
    print(f"valid: {sym_ok and quad_ok and prime_ok and magic_ok}")
    
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")