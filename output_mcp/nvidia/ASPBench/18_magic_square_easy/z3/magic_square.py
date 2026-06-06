from z3 import *

solver = Solver()

# 3x3 grid of integer variables
square = [[Int(f"x_{i}_{j}") for j in range(3)] for i in range(3)]

# Each cell must be between 1 and 9
for i in range(3):
    for j in range(3):
        solver.add(square[i][j] >= 1, square[i][j] <= 9)

# All numbers 1-9 must appear exactly once
all_cells = [square[i][j] for i in range(3) for j in range(3)]
solver.add(Distinct(all_cells))

# Row sums must be 15
for i in range(3):
    solver.add(Sum([square[i][j] for j in range(3)]) == 15)

# Column sums must be 15
for j in range(3):
    solver.add(Sum([square[i][j] for i in range(3)]) == 15)

# Diagonal sums must be 15
solver.add(Sum([square[i][i] for i in range(3)]) == 15)
solver.add(Sum([square[i][2 - i] for i in range(3)]) == 15)

# Solve and output
BENCHMARK_MODE = True
result = solver.check()
if result == sat:
    model = solver.model()
    print("STATUS: sat")
    # Print the 3x3 grid as a list of lists
    grid = [[model[square[i][j]].as_long() for j in range(3)] for i in range(3)]
    print(grid)
else:
    print("STATUS: unsat")