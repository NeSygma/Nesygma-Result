from z3 import *

solver = Solver()

# 4x4 grid of integers 1..16
grid = [[Int(f"c_{r}_{c}") for c in range(4)] for r in range(4)]

# Domain constraints
for r in range(4):
    for c in range(4):
        solver.add(grid[r][c] >= 1, grid[r][c] <= 16)

# All numbers must be distinct
cells = [grid[r][c] for r in range(4) for c in range(4)]
solver.add(Distinct(cells))

# Row sums
for r in range(4):
    solver.add(Sum(grid[r]) == 34)

# Column sums
for c in range(4):
    solver.add(Sum([grid[r][c] for r in range(4)]) == 34)

# Diagonal sums
solver.add(Sum([grid[i][i] for i in range(4)]) == 34)
solver.add(Sum([grid[i][3-i] for i in range(4)]) == 34)

# Symmetrical pairs (opposite cells sum to 17)
for r in range(4):
    for c in range(4):
        solver.add(grid[r][c] + grid[3-r][3-c] == 17)

# Quadrant sums
solver.add(Sum([grid[0][0], grid[0][1], grid[1][0], grid[1][1]]) == 34)  # TL
solver.add(Sum([grid[0][2], grid[0][3], grid[1][2], grid[1][3]]) == 34)  # TR
solver.add(Sum([grid[2][0], grid[2][1], grid[3][0], grid[3][1]]) == 34)  # BL
solver.add(Sum([grid[2][2], grid[2][3], grid[3][2], grid[3][3]]) == 34)  # BR

# Prime placement: corners cannot be 2,3,5,7
primes = [2, 3, 5, 7]
corners = [(0,0), (0,3), (3,0), (3,3)]
for (r,c) in corners:
    for p in primes:
        solver.add(grid[r][c] != p)

# Solve
result = solver.check()
if result == sat:
    m = solver.model()
    print("STATUS: sat")
    print("square:")
    for r in range(4):
        row_vals = [m[grid[r][c]] for c in range(4)]
        print(row_vals)
    print("magic_sum: 34")

    # Compute properties
    is_sym = True
    for r in range(4):
        for c in range(4):
            if m[grid[r][c]].as_long() + m[grid[3-r][3-c]].as_long() != 17:
                is_sym = False

    tl = m[grid[0][0]].as_long() + m[grid[0][1]].as_long() + m[grid[1][0]].as_long() + m[grid[1][1]].as_long()
    tr = m[grid[0][2]].as_long() + m[grid[0][3]].as_long() + m[grid[1][2]].as_long() + m[grid[1][3]].as_long()
    bl = m[grid[2][0]].as_long() + m[grid[2][1]].as_long() + m[grid[3][0]].as_long() + m[grid[3][1]].as_long()
    br = m[grid[2][2]].as_long() + m[grid[2][3]].as_long() + m[grid[3][2]].as_long() + m[grid[3][3]].as_long()
    is_quad = (tl == 34 and tr == 34 and bl == 34 and br == 34)

    is_prime = True
    for (r,c) in corners:
        if m[grid[r][c]].as_long() in primes:
            is_prime = False

    print("properties:")
    print(f"  is_symmetrical_pairs: {is_sym}")
    print(f"  is_quadrant_sum_valid: {is_quad}")
    print(f"  is_prime_placement_valid: {is_prime}")
    print("valid: True")
elif result == unsat:
    print("STATUS: unsat")
else:
    print("STATUS: unknown")