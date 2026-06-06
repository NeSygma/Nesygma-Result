from z3 import *

# Sudoku solver
solver = Solver()

# Create 9x9 grid of Int variables
cells = [[Int(f"c_{i}_{j}") for j in range(9)] for i in range(9)]

# Domain constraints: 1-9
for i in range(9):
    for j in range(9):
        solver.add(cells[i][j] >= 1, cells[i][j] <= 9)

# Row constraints
for i in range(9):
    solver.add(Distinct(cells[i]))

# Column constraints
for j in range(9):
    col = [cells[i][j] for i in range(9)]
    solver.add(Distinct(col))

# 3x3 sub-box constraints
for bi in range(0,9,3):
    for bj in range(0,9,3):
        box = [cells[i][j] for i in range(bi, bi+3) for j in range(bj, bj+3)]
        solver.add(Distinct(box))

# Given clues
clues = [
    [5,3,0,0,7,0,0,0,0],
    [6,0,0,1,9,5,0,0,0],
    [0,9,8,0,0,0,0,6,0],
    [8,0,0,0,6,0,0,0,3],
    [4,0,0,8,0,3,0,0,1],
    [7,0,0,0,2,0,0,0,6],
    [0,6,0,0,0,0,2,8,0],
    [0,0,0,4,1,9,0,0,5],
    [0,0,0,0,8,0,0,7,9]
]

for i in range(9):
    for j in range(9):
        val = clues[i][j]
        if val != 0:
            solver.add(cells[i][j] == val)

# Check satisfiability
result = solver.check()

if result == sat:
    model = solver.model()
    print("STATUS: sat")
    # Print each cell variable
    for i in range(9):
        for j in range(9):
            print(f"c_{i}_{j} = {model[cells[i][j]]}")
    # Optionally, print grid
    print("\nSolution grid:")
    for i in range(9):
        row_vals = [str(model[cells[i][j]]) for j in range(9)]
        print(" ".join(row_vals))
elif result == unsat:
    print("STATUS: unsat")
    # In benchmark mode, unsat is non-terminal; but we are not in benchmark mode
else:
    print("STATUS: unknown")