from z3 import *

# Create 9x9 grid of integer variables
grid = [[Int(f"cell_{r}_{c}") for c in range(9)] for r in range(9)]

solver = Solver()

# Domain: each cell is 1-9
for r in range(9):
    for c in range(9):
        solver.add(grid[r][c] >= 1, grid[r][c] <= 9)

# Standard Sudoku rules
# Each row contains 1-9 exactly once
for r in range(9):
    solver.add(Distinct([grid[r][c] for c in range(9)]))

# Each column contains 1-9 exactly once
for c in range(9):
    solver.add(Distinct([grid[r][c] for r in range(9)]))

# Each 3x3 box contains 1-9 exactly once
for box_r in range(3):
    for box_c in range(3):
        cells = []
        for r in range(3):
            for c in range(3):
                cells.append(grid[box_r*3 + r][box_c*3 + c])
        solver.add(Distinct(cells))

# Sudoku clues (pre-filled cells) - add initially
sudoku_clues = {
    (0,0): 5, (0,4): 7, (0,8): 2,
    (4,0): 4, (4,4): 5, (4,8): 1,
    (8,0): 3, (8,4): 8, (8,8): 9
}
for (r,c), val in sudoku_clues.items():
    solver.add(grid[r][c] == val)

# Mine-count clue locations
mine_clue_cells = [(0,1), (3,1), (5,7)]

# Helper: check if a cell is a mine (even digit)
def is_mine(cell):
    return Or([cell == 2, cell == 4, cell == 6, cell == 8])

# For each mine-count clue cell, the cell's value equals the number of neighboring mines
for (mr, mc) in mine_clue_cells:
    neighbor_mines = []
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            nr, nc = mr + dr, mc + dc
            if 0 <= nr < 9 and 0 <= nc < 9:
                neighbor_mines.append(If(is_mine(grid[nr][nc]), 1, 0))
    solver.add(grid[mr][mc] == Sum(neighbor_mines))

BENCHMARK_MODE = True
result = solver.check()

if result == sat:
    m = solver.model()
    print("STATUS: sat")
    print("SOLUTION:")
    for r in range(9):
        row_vals = [str(m[grid[r][c]]) for c in range(9)]
        print(" ".join(row_vals))
    
    # Check if sudoku clues were preserved
    clues_preserved = True
    for (r,c), val in sudoku_clues.items():
        if m[grid[r][c]].as_long() != val:
            clues_preserved = False
            break
    print(f"sudoku_clues_preserved: {clues_preserved}")
    
    # Check mine clues
    mine_clues_satisfied = True
    for (mr, mc) in mine_clue_cells:
        val = m[grid[mr][mc]].as_long()
        neighbor_count = 0
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                nr, nc = mr + dr, mc + dc
                if 0 <= nr < 9 and 0 <= nc < 9:
                    nv = m[grid[nr][nc]].as_long()
                    if nv in [2, 4, 6, 8]:
                        neighbor_count += 1
        if val != neighbor_count:
            mine_clues_satisfied = False
            break
    print(f"mine_clues_satisfied: {mine_clues_satisfied}")
    
    # List mines
    mines = []
    for r in range(9):
        for c in range(9):
            val = m[grid[r][c]].as_long()
            if val in [2, 4, 6, 8]:
                mines.append((r, c))
    print(f"Mines ({len(mines)} cells with even numbers):")
    for (r,c) in mines:
        print(f"  ({r},{c}): {m[grid[r][c]]}")
    
elif result == unsat:
    print("STATUS: unsat")
    print("RAW_RESULT: unsat (may need to relax sudoku clues)")
else:
    print("STATUS: unknown")