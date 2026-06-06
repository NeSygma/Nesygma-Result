from z3 import *

# BENCHMARK_MODE: ON (model-finding mode)
BENCHMARK_MODE = True

# Create a 9x9 grid of integer variables (1-9)
grid = [[Int(f"grid_{i}_{j}") for j in range(9)] for i in range(9)]

# Sudoku clues (pre-filled cells)
sudoku_clues = {
    (0, 0): 5, (0, 4): 7, (0, 8): 2,
    (4, 0): 4, (4, 4): 5, (4, 8): 1,
    (8, 0): 3, (8, 4): 8, (8, 8): 9
}

# Mine-count clue locations (highest priority)
mine_count_clues = [(0, 1), (3, 1), (5, 7)]

# Initialize solver
solver = Solver()

# 1. Add domain constraints: each cell must be between 1 and 9
for i in range(9):
    for j in range(9):
        solver.add(And(grid[i][j] >= 1, grid[i][j] <= 9))

# 2. Add Sudoku constraints: all rows, columns, and 3x3 boxes must contain distinct values
# Rows
for i in range(9):
    solver.add(Distinct(grid[i]))

# Columns
for j in range(9):
    solver.add(Distinct([grid[i][j] for i in range(9)]))

# 3x3 boxes
for box_i in range(0, 9, 3):
    for box_j in range(0, 9, 3):
        box = [grid[box_i + di][box_j + dj] for di in range(3) for dj in range(3)]
        solver.add(Distinct(box))

# 3. Add mine-count constraints for specific cells
# A cell is a mine if its value is even (2,4,6,8)
# For each mine-count clue cell, its value must equal the number of neighboring mines

def is_mine(i, j):
    """Return a Z3 expression that is True if grid[i][j] is a mine (even)."""
    return And(grid[i][j] >= 2, grid[i][j] <= 8, grid[i][j] % 2 == 0)

def count_neighboring_mines(i, j):
    """Return a Z3 expression for the number of neighboring mines of cell (i,j)."""
    count = 0
    for di in [-1, 0, 1]:
        for dj in [-1, 0, 1]:
            if di == 0 and dj == 0:
                continue  # Skip the cell itself
            ni, nj = i + di, j + dj
            if 0 <= ni < 9 and 0 <= nj < 9:
                count += If(is_mine(ni, nj), 1, 0)
    return count

# Add constraints for mine-count clue cells
for (i, j) in mine_count_clues:
    solver.add(grid[i][j] == count_neighboring_mines(i, j))

# 4. Add Sudoku clues, except for mine-count clue cells (mine-count constraints take priority)
for (i, j), val in sudoku_clues.items():
    if (i, j) not in mine_count_clues:
        solver.add(grid[i][j] == val)

# Check satisfiability
result = solver.check()

if result == sat:
    model = solver.model()
    print("STATUS: sat")
    # Extract and print the grid
    print("Grid:")
    for i in range(9):
        row = []
        for j in range(9):
            val = model[grid[i][j]]
            row.append(str(val))
        print(" ".join(row))
    
    # Extract mines: all cells with even values
    mines = []
    for i in range(9):
        for j in range(9):
            val = model[grid[i][j]]
            if val.as_long() % 2 == 0:
                mines.append((i, j))
    print("Mines (even-valued cells):")
    print(mines)
    
    # Check if Sudoku clues are preserved (only for non-mine-count clue cells)
    sudoku_clues_preserved = True
    for (i, j), val in sudoku_clues.items():
        if (i, j) not in mine_count_clues:
            cell_val = model[grid[i][j]]
            if cell_val.as_long() != val:
                sudoku_clues_preserved = False
                break
    print("sudoku_clues_preserved:", sudoku_clues_preserved)
    
    # Check if mine-count clues are satisfied
    mine_clues_satisfied = True
    for (i, j) in mine_count_clues:
        cell_val = model[grid[i][j]]
        expected = count_neighboring_mines(i, j)
        # Evaluate expected in the model
        actual_mines = 0
        for di in [-1, 0, 1]:
            for dj in [-1, 0, 1]:
                if di == 0 and dj == 0:
                    continue
                ni, nj = i + di, j + dj
                if 0 <= ni < 9 and 0 <= nj < 9:
                    neighbor_val = model[grid[ni][nj]]
                    if neighbor_val.as_long() % 2 == 0:
                        actual_mines += 1
        if cell_val.as_long() != actual_mines:
            mine_clues_satisfied = False
            break
    print("mine_clues_satisfied:", mine_clues_satisfied)
    
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")