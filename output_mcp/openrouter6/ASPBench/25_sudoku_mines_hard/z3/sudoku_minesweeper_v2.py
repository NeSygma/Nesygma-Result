from z3 import *

# Create solver
solver = Solver()

# 9x9 grid of integers 1-9
grid = [[Int(f'cell_{r}_{c}') for c in range(9)] for r in range(9)]

# Domain constraints: each cell between 1 and 9
for r in range(9):
    for c in range(9):
        solver.add(grid[r][c] >= 1)
        solver.add(grid[r][c] <= 9)

# Sudoku constraints: each row, column, 3x3 box must have digits 1-9 exactly once
for r in range(9):
    # Row constraints
    solver.add(Distinct([grid[r][c] for c in range(9)]))
    # Column constraints
    solver.add(Distinct([grid[c][r] for c in range(9)]))

# 3x3 box constraints
for br in range(0, 9, 3):
    for bc in range(0, 9, 3):
        cells = [grid[br + i][bc + j] for i in range(3) for j in range(3)]
        solver.add(Distinct(cells))

# Mine-count clue cells
clue_cells = [(0,1), (3,1), (5,7)]

# Helper to get neighbors (8 directions) for a given cell
def get_neighbors(r, c):
    neighbors = []
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            nr, nc = r + dr, c + dc
            if 0 <= nr < 9 and 0 <= nc < 9:
                neighbors.append((nr, nc))
    return neighbors

# Add mine-count constraints
for (r, c) in clue_cells:
    neighbors = get_neighbors(r, c)
    # Sum of mines (even digits) among neighbors
    neighbor_mines = Sum([If(grid[nr][nc] % 2 == 0, 1, 0) for (nr, nc) in neighbors])
    # The clue cell's value must equal that sum
    solver.add(grid[r][c] == neighbor_mines)
    # Clue cells cannot be mines themselves (must be odd)
    solver.add(grid[r][c] % 2 == 1)

# Pre-filled Sudoku clues (as hints, not enforced)
prefilled = {
    (0,0): 5, (0,4): 7, (0,8): 2,
    (4,0): 4, (4,4): 5, (4,8): 1,
    (8,0): 3, (8,4): 8, (8,8): 9
}

# Add pre-filled cells as soft constraints (prefer to keep them)
# We'll use a different approach: try to satisfy them, but allow changes
# For now, let's just add them as constraints and see if we get a solution
# If unsat, we'll remove them
for (r, c), val in prefilled.items():
    solver.add(grid[r][c] == val)

# Solve
result = solver.check()
if result == sat:
    model = solver.model()
    # Extract grid
    solution = [[0 for _ in range(9)] for _ in range(9)]
    for r in range(9):
        for c in range(9):
            solution[r][c] = model.evaluate(grid[r][c]).as_long()
    
    # Compute mines list (even digits)
    mines = []
    for r in range(9):
        for c in range(9):
            if solution[r][c] % 2 == 0:
                mines.append([r, c])
    
    # Check sudoku_clues_preserved
    sudoku_clues_preserved = True
    for (r, c), val in prefilled.items():
        if solution[r][c] != val:
            sudoku_clues_preserved = False
            break
    
    # Check mine_clues_satisfied (should be true by constraints)
    mine_clues_satisfied = True
    for (r, c) in clue_cells:
        neighbors = get_neighbors(r, c)
        count = sum(1 for (nr, nc) in neighbors if solution[nr][nc] % 2 == 0)
        if solution[r][c] != count:
            mine_clues_satisfied = False
            break
    
    # Output
    print("STATUS: sat")
    print("Grid:")
    for row in solution:
        print(' '.join(str(x) for x in row))
    print("Mines (coordinates):")
    for m in mines:
        print(m)
    print(f"sudoku_clues_preserved: {sudoku_clues_preserved}")
    print(f"mine_clues_satisfied: {mine_clues_satisfied}")
elif result == unsat:
    print("STATUS: unsat")
    print("No solution found with pre-filled cells")
    print("Trying without pre-filled cells...")
    
    # Remove pre-filled constraints and try again
    solver2 = Solver()
    
    # Recreate grid
    grid2 = [[Int(f'cell2_{r}_{c}') for c in range(9)] for r in range(9)]
    
    # Domain constraints
    for r in range(9):
        for c in range(9):
            solver2.add(grid2[r][c] >= 1)
            solver2.add(grid2[r][c] <= 9)
    
    # Sudoku constraints
    for r in range(9):
        solver2.add(Distinct([grid2[r][c] for c in range(9)]))
        solver2.add(Distinct([grid2[c][r] for c in range(9)]))
    
    # 3x3 box constraints
    for br in range(0, 9, 3):
        for bc in range(0, 9, 3):
            cells = [grid2[br + i][bc + j] for i in range(3) for j in range(3)]
            solver2.add(Distinct(cells))
    
    # Mine-count constraints
    for (r, c) in clue_cells:
        neighbors = get_neighbors(r, c)
        neighbor_mines = Sum([If(grid2[nr][nc] % 2 == 0, 1, 0) for (nr, nc) in neighbors])
        solver2.add(grid2[r][c] == neighbor_mines)
        solver2.add(grid2[r][c] % 2 == 1)
    
    # Solve without pre-filled cells
    result2 = solver2.check()
    if result2 == sat:
        model2 = solver2.model()
        solution2 = [[0 for _ in range(9)] for _ in range(9)]
        for r in range(9):
            for c in range(9):
                solution2[r][c] = model2.evaluate(grid2[r][c]).as_long()
        
        mines2 = []
        for r in range(9):
            for c in range(9):
                if solution2[r][c] % 2 == 0:
                    mines2.append([r, c])
        
        sudoku_clues_preserved2 = True
        for (r, c), val in prefilled.items():
            if solution2[r][c] != val:
                sudoku_clues_preserved2 = False
                break
        
        mine_clues_satisfied2 = True
        for (r, c) in clue_cells:
            neighbors = get_neighbors(r, c)
            count = sum(1 for (nr, nc) in neighbors if solution2[nr][nc] % 2 == 0)
            if solution2[r][c] != count:
                mine_clues_satisfied2 = False
                break
        
        print("STATUS: sat")
        print("Grid:")
        for row in solution2:
            print(' '.join(str(x) for x in row))
        print("Mines (coordinates):")
        for m in mines2:
            print(m)
        print(f"sudoku_clues_preserved: {sudoku_clues_preserved2}")
        print(f"mine_clues_satisfied: {mine_clues_satisfied2}")
    elif result2 == unsat:
        print("STATUS: unsat")
        print("No solution found even without pre-filled cells")
    else:
        print("STATUS: unknown")
        print("Solver returned unknown")
else:
    print("STATUS: unknown")
    print("Solver returned unknown")