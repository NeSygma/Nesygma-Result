from z3 import *

# Create 9x9 grid of Int variables
grid = [[Int(f"x_{i}_{j}") for j in range(9)] for i in range(9)]

solver = Solver()

# Domain constraints: each cell must be 1-9
for i in range(9):
    for j in range(9):
        solver.add(grid[i][j] >= 1, grid[i][j] <= 9)

# Row constraints: all digits distinct
for i in range(9):
    solver.add(Distinct(*grid[i]))

# Column constraints: all digits distinct
for j in range(9):
    col = [grid[i][j] for i in range(9)]
    solver.add(Distinct(*col))

# 3x3 box constraints: all digits distinct
for bi in range(3):
    for bj in range(3):
        box = []
        for i in range(3):
            for j in range(3):
                box.append(grid[bi*3 + i][bj*3 + j])
        solver.add(Distinct(*box))

# Given clues (row, col, digit)
clues = [
    (0,0,5),(0,1,3),(0,4,7),
    (1,0,6),(1,3,1),(1,4,9),(1,5,5),
    (2,1,9),(2,2,8),(2,6,6),
    (3,0,8),(3,4,6),(3,8,3),
    (4,0,4),(4,3,8),(4,4,3),(4,8,1),
    (5,0,7),(5,4,2),(5,8,6),
    (6,1,6),(6,6,2),(6,7,8),
    (7,3,4),(7,4,1),(7,5,9),(7,8,5),
    (8,4,8),(8,6,7),(8,8,9)
]
for (i,j,val) in clues:
    solver.add(grid[i][j] == val)

# Solve
BENCHMARK_MODE = True
result = solver.check()
if result == sat:
    print("STATUS: sat")
    m = solver.model()
    for i in range(9):
        row = [str(m[grid[i][j]].as_long()) for j in range(9)]
        print(" ".join(row))
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")