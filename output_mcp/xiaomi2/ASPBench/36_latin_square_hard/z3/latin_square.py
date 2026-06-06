from z3 import *

solver = Solver()

# 8x8 grid, each cell is an Int between 1 and 8
grid = [[Int(f"grid_{r}_{c}") for c in range(8)] for r in range(8)]

# Domain constraints: each cell is between 1 and 8
for r in range(8):
    for c in range(8):
        solver.add(grid[r][c] >= 1, grid[r][c] <= 8)

# Latin Square: each row has all distinct values
for r in range(8):
    solver.add(Distinct([grid[r][c] for c in range(8)]))

# Latin Square: each column has all distinct values
for c in range(8):
    solver.add(Distinct([grid[r][c] for r in range(8)]))

# Pre-filled cells (converting 1-indexed to 0-indexed)
prefilled = [
    (0, 0, 1), (0, 7, 8),
    (1, 1, 6),
    (2, 2, 4),
    (3, 3, 5),
    (4, 4, 7),
    (5, 5, 4),
    (6, 6, 6),
    (7, 7, 3),
    (7, 0, 8),
]
for r, c, v in prefilled:
    solver.add(grid[r][c] == v)

# Constraint 2: Adjacent pair sum > 5 (horizontally)
for r in range(8):
    for c in range(7):
        solver.add(grid[r][c] + grid[r][c + 1] > 5)

# Constraint 3: Quadrant parity
# Top-left quadrant (rows 0-3, cols 0-3): exactly 8 even numbers
even_count_tl = Sum([If(grid[r][c] % 2 == 0, 1, 0) for r in range(4) for c in range(4)])
solver.add(even_count_tl == 8)

# Bottom-right quadrant (rows 4-7, cols 4-7): exactly 8 odd numbers
odd_count_br = Sum([If(grid[r][c] % 2 == 1, 1, 0) for r in range(4, 8) for c in range(4, 8)])
solver.add(odd_count_br == 8)

# Constraint 4: Partial sums
# Sum of first four cells in row 1 (0-indexed row 0) = 14
solver.add(grid[0][0] + grid[0][1] + grid[0][2] + grid[0][3] == 14)

# Sum of first four cells in column 1 (0-indexed col 0) = 10
solver.add(grid[0][0] + grid[1][0] + grid[2][0] + grid[3][0] == 10)

# Solve
result = solver.check()

if result == sat:
    model = solver.model()
    print("STATUS: sat")
    print("Solution found:")
    for r in range(8):
        row_vals = []
        for c in range(8):
            row_vals.append(str(model[grid[r][c]].as_long()))
        print(" ".join(row_vals))
    
    # Verify constraints for debugging
    print("\nVerification:")
    # Check pre-filled
    for r, c, v in prefilled:
        val = model[grid[r][c]].as_long()
        assert val == v, f"Pre-filled ({r},{c}) expected {v}, got {val}"
    print("Pre-filled cells: OK")
    
    # Check row 0 first 4 sum
    s = sum(model[grid[0][c]].as_long() for c in range(4))
    print(f"Row 0 first 4 sum: {s} (expected 14)")
    
    # Check col 0 first 4 sum
    s = sum(model[grid[r][0]].as_long() for r in range(4))
    print(f"Col 0 first 4 sum: {s} (expected 10)")
    
    # Check top-left even count
    evens = sum(1 for r in range(4) for c in range(4) if model[grid[r][c]].as_long() % 2 == 0)
    print(f"Top-left even count: {evens} (expected 8)")
    
    # Check bottom-right odd count
    odds = sum(1 for r in range(4, 8) for c in range(4, 8) if model[grid[r][c]].as_long() % 2 == 1)
    print(f"Bottom-right odd count: {odds} (expected 8)")
    
    # Check adjacent sums
    min_adj = min(model[grid[r][c]].as_long() + model[grid[r][c+1]].as_long() for r in range(8) for c in range(7))
    print(f"Min adjacent pair sum: {min_adj} (must be > 5)")

elif result == unsat:
    print("STATUS: unsat")
    print("No solution exists.")
else:
    print("STATUS: unknown")