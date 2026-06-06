from z3 import *

# Create solver
solver = Solver()

# Grid variables
grid = [[Int(f"c_{i}_{j}") for j in range(9)] for i in range(9)]

# Domain constraints 1..9
for i in range(9):
    for j in range(9):
        solver.add(And(grid[i][j] >= 1, grid[i][j] <= 9))

# Sudoku constraints: rows, columns, boxes distinct
for i in range(9):
    solver.add(Distinct(grid[i]))  # rows
for j in range(9):
    solver.add(Distinct([grid[i][j] for i in range(9)]))  # columns
for br in range(3):
    for bc in range(3):
        cells = []
        for i in range(3):
            for j in range(3):
                cells.append(grid[br*3 + i][bc*3 + j])
        solver.add(Distinct(cells))

# Mine definition: a Bool per cell indicating even digit
is_mine = [[Bool(f"m_{i}_{j}") for j in range(9)] for i in range(9)]
for i in range(9):
    for j in range(9):
        solver.add(is_mine[i][j] == Or(grid[i][j] == 2, grid[i][j] == 4, grid[i][j] == 6, grid[i][j] == 8))

# Mine-count clue locations
mine_clue_coords = [(0,1), (3,1), (5,7)]
for (r,c) in mine_clue_coords:
    # compute neighbor sum
    neighbor_sum = Sum([If(is_mine[ni][nj], 1, 0)
                        for di in (-1,0,1) for dj in (-1,0,1)
                        if not (di==0 and dj==0)
                        for ni in [r+di] for nj in [c+dj]
                        if 0 <= ni < 9 and 0 <= nj < 9])
    solver.add(grid[r][c] == neighbor_sum)

# Optional: compute booleans for clue preservation
# Original Sudoku clues
original_clues = {
    (0,0):5, (0,4):7, (0,8):2,
    (4,0):4, (4,4):5, (4,8):1,
    (8,0):3, (8,4):8, (8,8):9
}
clue_preserve_exprs = []
for (r,c), val in original_clues.items():
    clue_preserve_exprs.append(grid[r][c] == val)
# sudoku_clues_preserved is true iff all preserved
sudoku_clues_preserved = Bool('sudoku_clues_preserved')
solver.add(sudoku_clues_preserved == And(clue_preserve_exprs))

# is_valid_sudoku is true because we enforced constraints
is_valid_sudoku = Bool('is_valid_sudoku')
solver.add(is_valid_sudoku == True)

# Solve
result = solver.check()
if result == sat:
    m = solver.model()
    print("STATUS: sat")
    # Print grid
    for i in range(9):
        row_vals = [m.eval(grid[i][j]).as_long() for j in range(9)]
        print('Row', i, ':', row_vals)
    # Mines list
    mines = []
    for i in range(9):
        for j in range(9):
            val = m.eval(grid[i][j]).as_long()
            if val % 2 == 0:
                mines.append((i,j))
    print('Mines =', mines)
    # Booleans
    print('is_valid_sudoku =', m.eval(is_valid_sudoku))
    print('sudoku_clues_preserved =', m.eval(sudoku_clues_preserved))
    # Verify mine-count clues satisfied (should be true)
    mine_clues_satisfied = Bool('mine_clues_satisfied')
    # compute satisfaction directly from model
    satisfied = True
    for (r,c) in mine_clue_coords:
        # count neighbor mines from model
        cnt = 0
        for di in (-1,0,1):
            for dj in (-1,0,1):
                if di==0 and dj==0: continue
                ni, nj = r+di, c+dj
                if 0 <= ni < 9 and 0 <= nj < 9:
                    if m.eval(grid[ni][nj]).as_long() % 2 == 0:
                        cnt += 1
        if m.eval(grid[r][c]).as_long() != cnt:
            satisfied = False
            break
    print('mine_clues_satisfied =', satisfied)
else:
    print('STATUS: unsat')