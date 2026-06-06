from z3 import *

solver = Solver()

# 8x8 grid of integer variables
grid = [[Int(f'grid_{r}_{c}') for c in range(8)] for r in range(8)]

# domain constraints: 1..8
for r in range(8):
    for c in range(8):
        solver.add(grid[r][c] >= 1, grid[r][c] <= 8)

# prefilled cells (1-indexed to 0-indexed)
solver.add(grid[0][0] == 1)      # (1,1) = 1
solver.add(grid[0][7] == 8)      # (1,8) = 8
solver.add(grid[1][1] == 6)      # (2,2) = 6
solver.add(grid[2][2] == 4)      # (3,3) = 4
solver.add(grid[3][3] == 5)      # (4,4) = 5
solver.add(grid[4][4] == 7)      # (5,5) = 7
solver.add(grid[5][5] == 4)      # (6,6) = 4
solver.add(grid[6][6] == 6)      # (7,7) = 6
solver.add(grid[7][7] == 3)      # (8,8) = 3
solver.add(grid[7][0] == 8)      # (8,1) = 8

# Latin square constraints: each row and column contains 1..8 exactly once
for r in range(8):
    solver.add(Distinct([grid[r][c] for c in range(8)]))
for c in range(8):
    solver.add(Distinct([grid[r][c] for r in range(8)]))

# Adjacent pair sum > 5 (horizontally adjacent)
for r in range(8):
    for c in range(7):
        solver.add(grid[r][c] + grid[r][c+1] > 5)

# Quadrant parity constraints
# top-left quadrant (rows 0-3, cols 0-3): exactly 8 even numbers
evens_tl = Sum([If(Equals(Mod(grid[r][c], 2), 0), 1, 0) for r in range(4) for c in range(4)])
solver.add(evens_tl == 8)
# bottom-right quadrant (rows 4-7, cols 4-7): exactly 8 odd numbers
odds_br = Sum([If(Equals(Mod(grid[r][c], 2), 1), 1, 0) for r in range(4,8) for c in range(4,8)])
solver.add(odds_br == 8)

# Partial sum constraints
# row 1 first four cells sum = 14
solver.add(Sum([grid[0][c] for c in range(4)]) == 14)
# column 1 first four cells sum = 10
solver.add(Sum([grid[r][0] for r in range(4)]) == 10)

# Solve and print result
BENCHMARK_MODE = True
result = solver.check()
if result == sat:
    print("STATUS: sat")
    model = solver.model()
    for r in range(8):
        row_vals = [model[grid[r][c]].as_long() for c in range(8)]
        print("Row", r+1, ":", row_vals)
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")