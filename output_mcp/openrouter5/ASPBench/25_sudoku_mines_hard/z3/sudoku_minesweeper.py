from z3 import *

# Create 9x9 grid of integer variables (1-9)
grid = [[Int(f"cell_{r}_{c}") for c in range(9)] for r in range(9)]

solver = Solver()

# Domain: each cell is 1-9
for r in range(9):
    for c in range(9):
        solver.add(grid[r][c] >= 1, grid[r][c] <= 9)

# Standard Sudoku constraints
# Each row has distinct values 1-9
for r in range(9):
    solver.add(Distinct([grid[r][c] for c in range(9)]))

# Each column has distinct values 1-9
for c in range(9):
    solver.add(Distinct([grid[r][c] for r in range(9)]))

# Each 3x3 box has distinct values 1-9
for br in range(3):
    for bc in range(3):
        cells = [grid[br*3 + r][bc*3 + c] for r in range(3) for c in range(3)]
        solver.add(Distinct(cells))

# Sudoku clues (pre-filled cells) - these may be overridden by mine-count constraints
# We add them as soft constraints by tracking whether they are preserved
# Actually, per the problem: mine-count constraints take priority.
# So we add the clues but allow them to be changed if needed.
# We'll add them as constraints but also track them.

# Pre-filled cells
clue_cells = [(0,0,5), (0,4,7), (0,8,2),
              (4,0,4), (4,4,5), (4,8,1),
              (8,0,3), (8,4,8), (8,8,9)]

# We'll add these as constraints but also track if they're preserved.
# Since mine-count constraints have highest priority, we add the clues
# but we'll check later if they conflict.

# Actually, let's add them as constraints. If they conflict with mine-count,
# the solver will find a solution that satisfies mine-count and may violate clues.
# But we need to allow violation. So we should NOT add them as hard constraints.
# Instead, we'll track them separately.

# Mine definition: a cell is a mine if its value is even (2,4,6,8)
def is_mine(cell_var):
    return Or([cell_var == 2, cell_var == 4, cell_var == 6, cell_var == 8])

# Mine-count clue locations
mine_clue_cells = [(0,1), (3,1), (5,7)]

# For each mine-count clue cell, its value must equal the number of neighboring mines
# Neighbors are the 8 surrounding cells (orthogonal and diagonal)
neighbor_offsets = [(-1,-1), (-1,0), (-1,1),
                    (0,-1),          (0,1),
                    (1,-1),  (1,0),  (1,1)]

for (r, c) in mine_clue_cells:
    neighbor_mines = []
    for dr, dc in neighbor_offsets:
        nr, nc = r + dr, c + dc
        if 0 <= nr < 9 and 0 <= nc < 9:
            neighbor_mines.append(is_mine(grid[nr][nc]))
    # Count how many neighbors are mines using If(cond, 1, 0)
    mine_count = Sum([If(is_mine(grid[nr][nc]), 1, 0) for (nr, nc) in 
                      [(r+dr, c+dc) for dr, dc in neighbor_offsets 
                       if 0 <= r+dr < 9 and 0 <= c+dc < 9]])
    solver.add(grid[r][c] == mine_count)

# Now check if the solution exists
BENCHMARK_MODE = True
result = solver.check()

if result == sat:
    m = solver.model()
    print("STATUS: sat")
    
    # Build the grid
    solution = [[m.eval(grid[r][c]).as_long() for c in range(9)] for r in range(9)]
    
    print("Solution grid:")
    for r in range(9):
        row_str = " ".join(str(solution[r][c]) for c in range(9))
        print(row_str)
    
    # Find mines (even numbers)
    mines = []
    for r in range(9):
        for c in range(9):
            if solution[r][c] % 2 == 0:
                mines.append([r, c])
    
    print(f"\nMines (even cells): {mines}")
    print(f"Number of mines: {len(mines)}")
    
    # Check Sudoku validity
    is_valid_sudoku = True
    for r in range(9):
        if len(set(solution[r])) != 9:
            is_valid_sudoku = False
    for c in range(9):
        if len(set(solution[r][c] for r in range(9))) != 9:
            is_valid_sudoku = False
    for br in range(3):
        for bc in range(3):
            vals = [solution[br*3+r][bc*3+c] for r in range(3) for c in range(3)]
            if len(set(vals)) != 9:
                is_valid_sudoku = False
    
    print(f"is_valid_sudoku: {is_valid_sudoku}")
    
    # Check which clues are preserved
    clues_preserved = True
    for (r, c, val) in clue_cells:
        if solution[r][c] != val:
            clues_preserved = False
            print(f"Clue at ({r},{c}) changed from {val} to {solution[r][c]}")
    
    print(f"sudoku_clues_preserved: {clues_preserved}")
    
    # Check mine clues
    mine_clues_satisfied = True
    for (r, c) in mine_clue_cells:
        neighbor_mines_count = 0
        for dr, dc in neighbor_offsets:
            nr, nc = r + dr, c + dc
            if 0 <= nr < 9 and 0 <= nc < 9:
                if solution[nr][nc] % 2 == 0:
                    neighbor_mines_count += 1
        if solution[r][c] != neighbor_mines_count:
            mine_clues_satisfied = False
            print(f"Mine clue at ({r},{c}): value={solution[r][c]}, neighbor_mines={neighbor_mines_count}")
    
    print(f"mine_clues_satisfied: {mine_clues_satisfied}")
    
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")