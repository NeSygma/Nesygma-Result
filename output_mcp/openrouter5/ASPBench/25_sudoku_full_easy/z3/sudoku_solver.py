from z3 import *

# Create a 9x9 grid of integer variables
grid = [[Int(f"cell_{r}_{c}") for c in range(9)] for r in range(9)]

solver = Solver()

# Domain constraint: each cell is between 1 and 9
for r in range(9):
    for c in range(9):
        solver.add(grid[r][c] >= 1, grid[r][c] <= 9)

# Row constraint: each row has distinct digits 1-9
for r in range(9):
    solver.add(Distinct(grid[r]))

# Column constraint: each column has distinct digits 1-9
for c in range(9):
    solver.add(Distinct([grid[r][c] for r in range(9)]))

# Box constraint: each 3x3 box has distinct digits 1-9
for box_r in range(3):
    for box_c in range(3):
        cells = []
        for r in range(3):
            for c in range(3):
                cells.append(grid[box_r * 3 + r][box_c * 3 + c])
        solver.add(Distinct(cells))

# Given clues (0 represents empty/unknown)
clues = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]

# Add clue constraints
for r in range(9):
    for c in range(9):
        if clues[r][c] != 0:
            solver.add(grid[r][c] == clues[r][c])

# Solve
result = solver.check()

if result == sat:
    model = solver.model()
    print("STATUS: sat")
    print("Solution:")
    for r in range(9):
        row_vals = []
        for c in range(9):
            row_vals.append(str(model[grid[r][c]]))
        print(" ".join(row_vals))
else:
    print("STATUS: unsat")
    print("No solution found")