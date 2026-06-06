from z3 import *

solver = Solver()

# declare grid variables
grid = [[Int(f'cell_{i}_{j}') for j in range(5)] for i in range(5)]

# domain constraints
for i in range(5):
    for j in range(5):
        solver.add(grid[i][j] >= 1, grid[i][j] <= 5)

# row distinct
for i in range(5):
    solver.add(Distinct(grid[i]))

# column distinct
for j in range(5):
    solver.add(Distinct([grid[i][j] for i in range(5)]))

# fixed cells
solver.add(grid[0][0] == 1)
solver.add(grid[1][2] == 3)
solver.add(grid[2][3] == 4)
solver.add(grid[3][4] == 5)
solver.add(grid[4][1] == 2)

# check
result = solver.check()
if result == sat:
    m = solver.model()
    solved = True
    # extract grid
    solved_grid = [[m.evaluate(grid[i][j], model_completion=True).as_long() for j in range(5)] for i in range(5)]
    print("STATUS: sat")
    print("grid:")
    for row in solved_grid:
        print(row)
    print("solved:", solved)
else:
    print("STATUS: unsat")