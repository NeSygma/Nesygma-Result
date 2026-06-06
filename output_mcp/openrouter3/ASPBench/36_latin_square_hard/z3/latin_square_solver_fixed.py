from z3 import *

# Create solver
solver = Solver()

# 8x8 grid of integers from 1 to 8
grid = [[Int(f'grid_{i}_{j}') for j in range(8)] for i in range(8)]

# Domain constraints: 1 ≤ grid[i][j] ≤ 8
for i in range(8):
    for j in range(8):
        solver.add(grid[i][j] >= 1)
        solver.add(grid[i][j] <= 8)

# Pre-filled cells (1-indexed to 0-indexed)
pre_filled = [
    (0, 0, 1),   # (1,1) = 1
    (0, 7, 8),   # (1,8) = 8
    (1, 1, 6),   # (2,2) = 6
    (2, 2, 4),   # (3,3) = 4
    (3, 3, 5),   # (4,4) = 5
    (4, 4, 7),   # (5,5) = 7
    (5, 5, 4),   # (6,6) = 4
    (6, 6, 6),   # (7,7) = 6
    (7, 7, 3),   # (8,8) = 3
    (7, 0, 8)    # (8,1) = 8
]

for i, j, val in pre_filled:
    solver.add(grid[i][j] == val)

# Latin Square Constraint: each row and column must contain every number 1-8 exactly once
for i in range(8):
    # Row constraint: all numbers 1-8 appear exactly once
    solver.add(Distinct([grid[i][j] for j in range(8)]))
    
    # Column constraint: all numbers 1-8 appear exactly once
    solver.add(Distinct([grid[j][i] for j in range(8)]))

# Adjacent Pair Sum Constraint: grid[r][c] + grid[r][c+1] > 5 for all valid r, c
for r in range(8):
    for c in range(7):  # columns 0-6 (since c+1 must be valid)
        solver.add(grid[r][c] + grid[r][c+1] > 5)

# Quadrant Parity Constraint
# Top-left quadrant (rows 0-3, cols 0-3): exactly 8 even numbers
top_left_even = []
for i in range(4):
    for j in range(4):
        # Check if number is even: grid[i][j] % 2 == 0
        # In Z3: (grid[i][j] % 2) == 0
        top_left_even.append(If(grid[i][j] % 2 == 0, 1, 0))
solver.add(Sum(top_left_even) == 8)

# Bottom-right quadrant (rows 4-7, cols 4-7): exactly 8 odd numbers
bottom_right_odd = []
for i in range(4, 8):
    for j in range(4, 8):
        # Check if number is odd: grid[i][j] % 2 == 1
        bottom_right_odd.append(If(grid[i][j] % 2 == 1, 1, 0))
solver.add(Sum(bottom_right_odd) == 8)

# Partial Sum Constraint: row 1 sum = 14 (row index 0)
row1_sum = Sum([grid[0][j] for j in range(4)])
solver.add(row1_sum == 14)

# Partial Sum Constraint: column 1 sum = 10 (column index 0)
col1_sum = Sum([grid[i][0] for i in range(4)])
solver.add(col1_sum == 10)

# Check and print results
BENCHMARK_MODE = True
result = solver.check()

if result == sat:
    model = solver.model()
    print("STATUS: sat")
    print("Solution found!")
    print("\nGrid (8x8):")
    for i in range(8):
        row_vals = []
        for j in range(8):
            val = model.evaluate(grid[i][j])
            row_vals.append(str(val))
        print(" ".join(row_vals))
    
    # Verify constraints
    print("\nConstraint Verification:")
    
    # Check Latin square
    print("Latin square: Each row and column has distinct numbers 1-8")
    
    # Check adjacent pair sums
    all_adjacent_ok = True
    for r in range(8):
        for c in range(7):
            val1 = int(str(model.evaluate(grid[r][c])))
            val2 = int(str(model.evaluate(grid[r][c+1])))
            if val1 + val2 <= 5:
                all_adjacent_ok = False
                print(f"  Violation at ({r+1},{c+1}) and ({r+1},{c+2}): {val1}+{val2}={val1+val2}")
    if all_adjacent_ok:
        print("Adjacent pair sums > 5: OK")
    
    # Check quadrant parity
    top_left_evens = 0
    for i in range(4):
        for j in range(4):
            val = int(str(model.evaluate(grid[i][j])))
            if val % 2 == 0:
                top_left_evens += 1
    print(f"Top-left quadrant evens: {top_left_evens} (expected 8)")
    
    bottom_right_odds = 0
    for i in range(4, 8):
        for j in range(4, 8):
            val = int(str(model.evaluate(grid[i][j])))
            if val % 2 == 1:
                bottom_right_odds += 1
    print(f"Bottom-right quadrant odds: {bottom_right_odds} (expected 8)")
    
    # Check partial sums
    row1_sum_val = sum(int(str(model.evaluate(grid[0][j]))) for j in range(4))
    col1_sum_val = sum(int(str(model.evaluate(grid[i][0]))) for i in range(4))
    print(f"Row 1 sum (first 4 cells): {row1_sum_val} (expected 14)")
    print(f"Column 1 sum (first 4 cells): {col1_sum_val} (expected 10)")
    
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")