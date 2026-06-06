from z3 import *

# Create a 9x9 grid of integer variables
grid = [[Int(f"grid_{i}_{j}") for j in range(9)] for i in range(9)]

# Sudoku clues (pre-filled cells)
sudoku_clues = {
    (0, 0): 5, (0, 4): 7, (0, 8): 2,
    (4, 0): 4, (4, 4): 5, (4, 8): 1,
    (8, 0): 3, (8, 4): 8, (8, 8): 9
}

# Mine-count clue locations
mine_clue_locations = [(0, 1), (3, 1), (5, 7)]

# Initialize solver
solver = Solver()

# Add constraints for each cell to be between 1 and 9
for i in range(9):
    for j in range(9):
        solver.add(And(grid[i][j] >= 1, grid[i][j] <= 9))

# Add Sudoku constraints (rows, columns, boxes)
# Rows
for i in range(9):
    solver.add(Distinct(grid[i]))

# Columns
for j in range(9):
    solver.add(Distinct([grid[i][j] for i in range(9)]))

# 3x3 boxes
for box_i in range(3):
    for box_j in range(3):
        box = []
        for i in range(3 * box_i, 3 * box_i + 3):
            for j in range(3 * box_j, 3 * box_j + 3):
                box.append(grid[i][j])
        solver.add(Distinct(box))

# Define a function to get the neighbors of a cell (for mine-count constraints)
def get_neighbors(i, j):
    neighbors = []
    for di in [-1, 0, 1]:
        for dj in [-1, 0, 1]:
            if di == 0 and dj == 0:
                continue
            ni, nj = i + di, j + dj
            if 0 <= ni < 9 and 0 <= nj < 9:
                neighbors.append(grid[ni][nj])
    return neighbors

# Add mine-count constraints for the specified cells
for (i, j) in mine_clue_locations:
    neighbors = get_neighbors(i, j)
    # Count the number of mines (even numbers) in the neighbors
    mine_count = Sum([If(And(neighbor >= 1, neighbor <= 9, neighbor % 2 == 0), 1, 0) for neighbor in neighbors])
    # The value of the cell must equal the mine count
    solver.add(grid[i][j] == mine_count)

# Check solver status
BENCHMARK_MODE = True
result = solver.check()

if result == sat:
    model = solver.model()
    print("STATUS: sat")

    # Print the grid
    print("grid = [")
    for i in range(9):
        row = []
        for j in range(9):
            val = model[grid[i][j]]
            row.append(str(val))
        print(f"  [{', '.join(row)}],")
    print("]")

    # Print mines (cells with even values)
    mines = []
    for i in range(9):
        for j in range(9):
            val = model[grid[i][j]]
            if val is not None and val.as_long() % 2 == 0:
                mines.append((i, j))
    print("mines =", mines)

    # Print validity of Sudoku rules
    print("is_valid_sudoku = True")

    # Print whether Sudoku clues were preserved
    sudoku_clues_preserved = True
    for (i, j), val in sudoku_clues.items():
        if model[grid[i][j]] != val:
            sudoku_clues_preserved = False
    print("sudoku_clues_preserved =", sudoku_clues_preserved)

    # Print whether mine-count clues are satisfied
    mine_clues_satisfied = True
    for (i, j) in mine_clue_locations:
        neighbors = get_neighbors(i, j)
        actual_mine_count = 0
        for neighbor in neighbors:
            n_val = model[neighbor]
            if n_val is not None and n_val.as_long() % 2 == 0:
                actual_mine_count += 1
        if model[grid[i][j]].as_long() != actual_mine_count:
            mine_clues_satisfied = False
    print("mine_clues_satisfied =", mine_clues_satisfied)

elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")