from z3 import *

n = 5
grid = [[Int(f'g_{i}_{j}') for j in range(n)] for i in range(n)]

solver = Solver()

# domain constraints (1 to 5)
for i in range(n):
    for j in range(n):
        solver.add(grid[i][j] >= 1, grid[i][j] <= n)

# row distinctness
for i in range(n):
    solver.add(Distinct(grid[i]))

# column distinctness
for j in range(n):
    solver.add(Distinct([grid[i][j] for i in range(n)]))

# given clues (1-indexed positions)
solver.add(grid[0][0] == 1)   # Row 1, Col 1 = 1
solver.add(grid[1][2] == 3)   # Row 2, Col 3 = 3
solver.add(grid[2][3] == 4)   # Row 3, Col 4 = 4
solver.add(grid[3][4] == 5)   # Row 4, Col 5 = 5
solver.add(grid[4][1] == 2)   # Row 5, Col 2 = 2

# solve
result = solver.check()
if result == sat:
    m = solver.model()
    print("STATUS: sat")
    print("solved = True")
    for i in range(n):
        for j in range(n):
            print(f"grid[{i}][{j}] = {m[grid[i][j]]}")
else:
    print("STATUS: unsat")