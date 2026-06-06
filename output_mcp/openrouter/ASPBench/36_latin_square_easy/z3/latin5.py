from z3 import *

# Define size
N = 5
# Create grid of Int variables
grid = [[Int(f'cell_{i}_{j}') for j in range(N)] for i in range(N)]
solver = Solver()

# Domain constraints: each cell between 1 and 5
for i in range(N):
    for j in range(N):
        solver.add(And(grid[i][j] >= 1, grid[i][j] <= N))

# Row distinctness
for i in range(N):
    solver.add(Distinct(grid[i]))

# Column distinctness
for j in range(N):
    col = [grid[i][j] for i in range(N)]
    solver.add(Distinct(col))

# Given values
givens = [((0,0),1), ((1,2),3), ((2,3),4), ((3,4),5), ((4,1),2)]
for (i,j), val in givens:
    solver.add(grid[i][j] == val)

# Solve
result = solver.check()
if result == sat:
    m = solver.model()
    print("STATUS: sat")
    # Print grid rows
    for i in range(N):
        row_vals = [m.eval(grid[i][j]).as_long() for j in range(N)]
        print('Row', i+1, ':', row_vals)
else:
    print('STATUS: unsat' if result == unsat else 'STATUS: unknown')