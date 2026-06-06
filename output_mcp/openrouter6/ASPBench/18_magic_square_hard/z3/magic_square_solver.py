from z3 import *

# Create solver
solver = Solver()

# Grid size
N = 4

# Create 4x4 grid of integer variables (1-16)
grid = [[Int(f"cell_{r}_{c}") for c in range(N)] for r in range(N)]

# 1. Uniqueness: Each integer 1-16 appears exactly once
all_cells = [grid[r][c] for r in range(N) for c in range(N)]
solver.add(Distinct(all_cells))
for cell in all_cells:
    solver.add(cell >= 1, cell <= 16)

# 2. Magic sum: All rows, columns, and diagonals sum to 34
MAGIC_SUM = 34

# Rows
for r in range(N):
    solver.add(Sum([grid[r][c] for c in range(N)]) == MAGIC_SUM)

# Columns
for c in range(N):
    solver.add(Sum([grid[r][c] for r in range(N)]) == MAGIC_SUM)

# Main diagonals
solver.add(Sum([grid[i][i] for i in range(N)]) == MAGIC_SUM)
solver.add(Sum([grid[i][N-1-i] for i in range(N)]) == MAGIC_SUM)

# 3. Symmetrical pairs: Opposite cells sum to 17
# Using 1-based indexing: (r,c) opposite to (5-r,5-c)
# In 0-based indexing: (r,c) opposite to (3-r,3-c)
for r in range(N):
    for c in range(N):
        opp_r = N - 1 - r
        opp_c = N - 1 - c
        # Only add constraint once per pair (avoid duplicates)
        if (r, c) < (opp_r, opp_c):
            solver.add(grid[r][c] + grid[opp_r][opp_c] == 17)

# 4. Quadrant sums: Each 2x2 quadrant sums to 34
# Top-Left: (0,0), (0,1), (1,0), (1,1)
solver.add(Sum([grid[0][0], grid[0][1], grid[1][0], grid[1][1]]) == MAGIC_SUM)
# Top-Right: (0,2), (0,3), (1,2), (1,3)
solver.add(Sum([grid[0][2], grid[0][3], grid[1][2], grid[1][3]]) == MAGIC_SUM)
# Bottom-Left: (2,0), (2,1), (3,0), (3,1)
solver.add(Sum([grid[2][0], grid[2][1], grid[3][0], grid[3][1]]) == MAGIC_SUM)
# Bottom-Right: (2,2), (2,3), (3,2), (3,3)
solver.add(Sum([grid[2][2], grid[2][3], grid[3][2], grid[3][3]]) == MAGIC_SUM)

# 5. Prime placement: Small primes {2,3,5,7} forbidden from corners
# Corners: (0,0), (0,3), (3,0), (3,3)
small_primes = [2, 3, 5, 7]
corners = [(0,0), (0,3), (3,0), (3,3)]
for r, c in corners:
    for prime in small_primes:
        solver.add(grid[r][c] != prime)

# Check for solution
BENCHMARK_MODE = True
result = solver.check()

if result == sat:
    model = solver.model()
    print("STATUS: sat")
    print("\nSolution found:")
    print("Grid:")
    for r in range(N):
        row_vals = []
        for c in range(N):
            val = model.eval(grid[r][c])
            row_vals.append(str(val))
        print(" ".join(row_vals))
    
    # Verify constraints and print properties
    print("\nProperties:")
    
    # Check symmetrical pairs
    symmetrical_ok = True
    for r in range(N):
        for c in range(N):
            opp_r = N - 1 - r
            opp_c = N - 1 - c
            if (r, c) < (opp_r, opp_c):
                val1 = int(str(model.eval(grid[r][c])))
                val2 = int(str(model.eval(grid[opp_r][opp_c])))
                if val1 + val2 != 17:
                    symmetrical_ok = False
                    break
        if not symmetrical_ok:
            break
    print(f"is_symmetrical_pairs: {symmetrical_ok}")
    
    # Check quadrant sums
    quadrant_ok = True
    quadrants = [
        [(0,0), (0,1), (1,0), (1,1)],
        [(0,2), (0,3), (1,2), (1,3)],
        [(2,0), (2,1), (3,0), (3,1)],
        [(2,2), (2,3), (3,2), (3,3)]
    ]
    for quad in quadrants:
        quad_sum = sum(int(str(model.eval(grid[r][c]))) for r, c in quad)
        if quad_sum != MAGIC_SUM:
            quadrant_ok = False
            break
    print(f"is_quadrant_sum_valid: {quadrant_ok}")
    
    # Check prime placement
    prime_ok = True
    for r, c in corners:
        val = int(str(model.eval(grid[r][c])))
        if val in small_primes:
            prime_ok = False
            break
    print(f"is_prime_placement_valid: {prime_ok}")
    
    # Overall validity
    valid = symmetrical_ok and quadrant_ok and prime_ok
    print(f"\nvalid: {valid}")
    
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")