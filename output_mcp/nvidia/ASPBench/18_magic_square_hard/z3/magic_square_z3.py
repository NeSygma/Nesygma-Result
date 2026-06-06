from z3 import *

solver = Solver()

# 4x4 grid of integer variables
grid = [[Int(f'x_{i}_{j}') for j in range(4)] for i in range(4)]

# each cell must be between 1 and 16
for i in range(4):
    for j in range(4):
        solver.add(grid[i][j] >= 1, grid[i][j] <= 16)

# all numbers 1..16 must appear exactly once
solver.add(Distinct([grid[i][j] for i in range(4) for j in range(4)]))

# magic sum constraints: rows, columns, and both diagonals
for i in range(4):
    solver.add(Sum([grid[i][j] for j in range(4)]) == 34)          # row i
    solver.add(Sum([grid[j][i] for j in range(4)]) == 34)          # column i

# diagonals
solver.add(Sum([grid[i][i] for i in range(4)]) == 34)              # main diagonal
solver.add(Sum([grid[i][3-i] for i in range(4)]) == 34)            # anti-diagonal

# symmetrical pairs: opposite cells sum to 17 (1-based indexing => 0-based opposite is (3-i,3-j))
for i in range(4):
    for j in range(4):
        solver.add(grid[i][j] + grid[3-i][3-j] == 17)

# quadrant sums (each 2x2 quadrant must sum to 34)
solver.add(Sum([grid[0][0], grid[0][1], grid[1][0], grid[1][1]]) == 34)          # top-left
solver.add(Sum([grid[0][2], grid[0][3], grid[1][2], grid[1][3]]) == 34)          # top-right
solver.add(Sum([grid[2][0], grid[2][1], grid[3][0], grid[3][1]]) == 34)          # bottom-left
solver.add(Sum([grid[2][2], grid[2][3], grid[3][2], grid[3][3]]) == 34)          # bottom-right

# prime placement: corners (0,0), (0,3), (3,0), (3,3) cannot be 2,3,5,7
corners = [(0,0), (0,3), (3,0), (3,3)]
for (i, j) in corners:
    solver.add(And(grid[i][j] != 2, grid[i][j] != 3, grid[i][j] != 5, grid[i][j] != 7))

# solve and output
result = solver.check()
if result == sat:
    print("STATUS: sat")
    m = solver.model()
    for i in range(4):
        row_vals = [m[grid[i][j]].as_long() for j in range(4)]
        print(row_vals)
elif result == unsat:
    print("STATUS: unsat")
else:
    print("STATUS: unknown")