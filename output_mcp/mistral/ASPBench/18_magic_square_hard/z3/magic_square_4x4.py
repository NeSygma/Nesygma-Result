from z3 import *

# BENCHMARK_MODE: ON (model-finding mode)
BENCHMARK_MODE = True

# Create a 4x4 grid of integer variables
grid = [[Int(f"grid_{i}_{j}") for j in range(4)] for i in range(4)]

# Magic constant
magic_sum = 34

# Small primes
small_primes = {2, 3, 5, 7}

# Corner cells (1-based indexing)
corner_cells = [(0, 0), (0, 3), (3, 0), (3, 3)]

# Create solver
solver = Solver()

# 1. Uniqueness: Each integer from 1 to 16 appears exactly once
all_cells = [grid[i][j] for i in range(4) for j in range(4)]
solver.add(Distinct(all_cells))
for i in range(4):
    for j in range(4):
        solver.add(grid[i][j] >= 1, grid[i][j] <= 16)

# 2. Magic sum: All rows, columns, and both main diagonals sum to 34
# Rows
for i in range(4):
    solver.add(Sum([grid[i][j] for j in range(4)]) == magic_sum)

# Columns
for j in range(4):
    solver.add(Sum([grid[i][j] for i in range(4)]) == magic_sum)

# Main diagonals
solver.add(Sum([grid[i][i] for i in range(4)]) == magic_sum)
solver.add(Sum([grid[i][3-i] for i in range(4)]) == magic_sum)

# 3. Symmetrical pairs: Opposite cells sum to 17 (1-based indexing)
# In 0-based indexing, opposite of (i,j) is (3-i, 3-j)
for i in range(4):
    for j in range(4):
        solver.add(grid[i][j] + grid[3-i][3-j] == 17)

# 4. Quadrant sums: Each 2x2 quadrant sums to 34
# Top-Left: (0,0), (0,1), (1,0), (1,1)
solver.add(Sum([grid[0][0], grid[0][1], grid[1][0], grid[1][1]]) == magic_sum)

# Top-Right: (0,2), (0,3), (1,2), (1,3)
solver.add(Sum([grid[0][2], grid[0][3], grid[1][2], grid[1][3]]) == magic_sum)

# Bottom-Left: (2,0), (2,1), (3,0), (3,1)
solver.add(Sum([grid[2][0], grid[2][1], grid[3][0], grid[3][1]]) == magic_sum)

# Bottom-Right: (2,2), (2,3), (3,2), (3,3)
solver.add(Sum([grid[2][2], grid[2][3], grid[3][2], grid[3][3]]) == magic_sum)

# 5. Prime placement: Small primes {2,3,5,7} cannot be in corner cells
for (i, j) in corner_cells:
    solver.add(Not(Or([grid[i][j] == p for p in small_primes])))

# Check for a solution
result = solver.check()

if result == sat:
    model = solver.model()
    print("STATUS: sat")
    print("Solution found!")
    for i in range(4):
        row = [str(model[grid[i][j]]) for j in range(4)]
        print(f"row {i+1}: [{', '.join(row)}]")
    
    # Validate symmetrical pairs
    is_symmetrical_pairs = True
    for i in range(4):
        for j in range(4):
            if model[grid[i][j]].as_long() + model[grid[3-i][3-j]].as_long() != 17:
                is_symmetrical_pairs = False
                break
        if not is_symmetrical_pairs:
            break
    print(f"is_symmetrical_pairs: {is_symmetrical_pairs}")
    
    # Validate quadrant sums
    is_quadrant_sum_valid = True
    # Top-Left
    tl_sum = sum(model[grid[i][j]].as_long() for i in range(2) for j in range(2))
    if tl_sum != magic_sum:
        is_quadrant_sum_valid = False
    # Top-Right
    tr_sum = sum(model[grid[i][j]].as_long() for i in range(2) for j in range(2, 4))
    if tr_sum != magic_sum:
        is_quadrant_sum_valid = False
    # Bottom-Left
    bl_sum = sum(model[grid[i][j]].as_long() for i in range(2, 4) for j in range(2))
    if bl_sum != magic_sum:
        is_quadrant_sum_valid = False
    # Bottom-Right
    br_sum = sum(model[grid[i][j]].as_long() for i in range(2, 4) for j in range(2, 4))
    if br_sum != magic_sum:
        is_quadrant_sum_valid = False
    print(f"is_quadrant_sum_valid: {is_quadrant_sum_valid}")
    
    # Validate prime placement in corners
    is_prime_placement_valid = True
    for (i, j) in corner_cells:
        val = model[grid[i][j]].as_long()
        if val in small_primes:
            is_prime_placement_valid = False
            break
    print(f"is_prime_placement_valid: {is_prime_placement_valid}")
    
    print(f"valid: {is_symmetrical_pairs and is_quadrant_sum_valid and is_prime_placement_valid}")
    
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")