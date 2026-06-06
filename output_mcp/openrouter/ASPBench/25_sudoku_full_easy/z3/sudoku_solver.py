from z3 import *

# Sudoku solver for given puzzle
solver = Solver()

# Create 9x9 matrix of Int variables
grid = [[Int(f'cell_{r}_{c}') for c in range(9)] for r in range(9)]

# Add domain constraints (1..9)
for r in range(9):
    for c in range(9):
        solver.add(And(grid[r][c] >= 1, grid[r][c] <= 9))

# Add row distinct constraints
for r in range(9):
    solver.add(Distinct(grid[r]))

# Add column distinct constraints
for c in range(9):
    col = [grid[r][c] for r in range(9)]
    solver.add(Distinct(col))

# Add 3x3 subgrid distinct constraints
for br in range(3):
    for bc in range(3):
        block = [grid[r][c]
                 for r in range(br*3, br*3+3)
                 for c in range(bc*3, bc*3+3)]
        solver.add(Distinct(block))

# Given clues (0 or '_' denotes empty)
clues = [
    [5,3,0, 0,7,0, 0,0,0],
    [6,0,0, 1,9,5, 0,0,0],
    [0,9,8, 0,0,0, 0,6,0],
    [8,0,0, 0,6,0, 0,0,3],
    [4,0,0, 8,0,3, 0,0,1],
    [7,0,0, 0,2,0, 0,0,6],
    [0,6,0, 0,0,0, 2,8,0],
    [0,0,0, 4,1,9, 0,0,5],
    [0,0,0, 0,8,0, 0,7,9]
]
for r in range(9):
    for c in range(9):
        val = clues[r][c]
        if val != 0:
            solver.add(grid[r][c] == val)

# Solve
result = solver.check()
if result == sat:
    m = solver.model()
    print("STATUS: sat")
    # Print solution grid
    for r in range(9):
        row_vals = [m.eval(grid[r][c]).as_long() for c in range(9)]
        print(' '.join(str(v) for v in row_vals))
else:
    print("STATUS: unsat")