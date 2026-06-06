from z3 import *

solver = Solver()

# Create 9x9 grid of integer variables (1-9)
cells = [[Int(f'cell_{r}_{c}') for c in range(9)] for r in range(9)]

# Domain constraints: each cell is between 1 and 9
for r in range(9):
    for c in range(9):
        solver.add(cells[r][c] >= 1, cells[r][c] <= 9)

# Row constraints: all different in each row
for r in range(9):
    solver.add(Distinct(cells[r]))

# Column constraints: all different in each column
for c in range(9):
    solver.add(Distinct([cells[r][c] for r in range(9)]))

# 3x3 box constraints: all different in each sub-box
for box_r in range(3):
    for box_c in range(3):
        box = [cells[box_r*3 + dr][box_c*3 + dc] for dr in range(3) for dc in range(3)]
        solver.add(Distinct(box))

# Given clues
clues = [
    (0,0,5), (0,1,3), (0,4,7),
    (1,0,6), (1,3,1), (1,4,9), (1,5,5),
    (2,1,9), (2,2,8), (2,7,6),
    (3,0,8), (3,4,6), (3,8,3),
    (4,0,4), (4,3,8), (4,5,3), (4,8,1),
    (5,0,7), (5,4,2), (5,8,6),
    (6,1,6), (6,6,2), (6,7,8),
    (7,3,4), (7,4,1), (7,5,9), (7,8,5),
    (8,4,8), (8,7,7), (8,8,9)
]

for r, c, val in clues:
    solver.add(cells[r][c] == val)

BENCHMARK_MODE = True
result = solver.check()

if result == sat:
    model = solver.model()
    print("STATUS: sat")
    print("Sudoku Solution:")
    for r in range(9):
        row_vals = []
        for c in range(9):
            row_vals.append(str(model[cells[r][c]].as_long()))
        # Format with box separators
        line = " ".join(row_vals[:3]) + " | " + " ".join(row_vals[3:6]) + " | " + " ".join(row_vals[6:])
        print(line)
        if r in (2, 5):
            print("------+-------+------")
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")