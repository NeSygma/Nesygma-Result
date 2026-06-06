from z3 import *

# Sudoku clues (soft - can be overridden by mine-count constraints)
sudoku_clues = [
    (0, 0, 5), (0, 4, 7), (0, 8, 2),
    (4, 0, 4), (4, 4, 5), (4, 8, 1),
    (8, 0, 3), (8, 4, 8), (8, 8, 9)
]

# Mine-count clue cells: value must equal count of neighboring mines
mine_clue_cells = [(0, 1), (3, 1), (5, 7)]

# Helper: get all 8 neighbors of a cell (orthogonal + diagonal)
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

def solve(with_clues=True):
    solver = Solver()
    solver.set("timeout", 120000)  # 2 minute timeout
    
    # Create 9x9 grid of integer variables (digits 1-9)
    grid = [[Int(f'grid_{r}_{c}') for c in range(9)] for r in range(9)]
    
    # Domain constraints: each cell is 1-9
    for r in range(9):
        for c in range(9):
            solver.add(grid[r][c] >= 1, grid[r][c] <= 9)
    
    # === Sudoku constraints ===
    # Each row has all different values
    for r in range(9):
        solver.add(Distinct([grid[r][c] for c in range(9)]))
    
    # Each column has all different values
    for c in range(9):
        solver.add(Distinct([grid[r][c] for r in range(9)]))
    
    # Each 3x3 box has all different values
    for br in range(3):
        for bc in range(3):
            solver.add(Distinct([grid[br*3 + r][bc*3 + c] for r in range(3) for c in range(3)]))
    
    # === Sudoku clues (if preserving them) ===
    if with_clues:
        for r, c, v in sudoku_clues:
            solver.add(grid[r][c] == v)
    
    # === Mine-count constraints (HARD - highest priority) ===
    # A cell is a mine iff its value is even (2, 4, 6, 8)
    # For each mine-count clue cell, its value == count of neighboring mines
    for r, c in mine_clue_cells:
        neighbors = get_neighbors(r, c)
        mine_count = Sum([If(grid[nr][nc] % 2 == 0, 1, 0) for nr, nc in neighbors])
        solver.add(grid[r][c] == mine_count)
    
    result = solver.check()
    if result == sat:
        m = solver.model()
        solution = [[m.evaluate(grid[r][c]).as_long() for c in range(9)] for r in range(9)]
        return solution
    elif result == unsat:
        return None
    else:
        return "unknown"

# === Phase 1: Try with Sudoku clues preserved ===
print("Attempting solution with Sudoku clues preserved...")
solution = solve(with_clues=True)
clues_preserved = True

if solution is None:
    print("No solution with clues preserved. Trying without Sudoku clues...")
    # === Phase 2: Drop Sudoku clues, keep only mine-count constraints ===
    solution = solve(with_clues=False)
    clues_preserved = False

if solution == "unknown":
    print("STATUS: unknown")
    print("Solver returned unknown (timeout or inconclusive)")
elif solution is not None:
    print("STATUS: sat")
    
    # Print the grid
    print("\n=== SOLUTION GRID ===")
    for r in range(9):
        row_str = ""
        for c in range(9):
            val = solution[r][c]
            marker = "*" if val % 2 == 0 else " "  # Mark mines
            row_str += f"{val}{marker}"
            if c % 3 == 2 and c < 8:
                row_str += "| "
        print(row_str)
        if r % 3 == 2 and r < 8:
            print("------+-------+------")
    
    # Find all mines (cells with even numbers)
    mines = []
    for r in range(9):
        for c in range(9):
            if solution[r][c] % 2 == 0:
                mines.append([r, c])
    print(f"\nMines (even-digit cells): {mines}")
    print(f"Number of mines: {len(mines)}")
    
    # Verify Sudoku clues preservation
    if clues_preserved:
        clues_preserved = all(solution[r][c] == v for r, c, v in sudoku_clues)
    print(f"\nsudoku_clues_preserved: {clues_preserved}")
    
    # Verify mine-count clues
    print("\n=== MINE-COUNT VERIFICATION ===")
    mine_clues_satisfied = True
    for r, c in mine_clue_cells:
        neighbors = get_neighbors(r, c)
        mine_neighbors = [(nr, nc) for nr, nc in neighbors if solution[nr][nc] % 2 == 0]
        count = len(mine_neighbors)
        satisfied = solution[r][c] == count
        if not satisfied:
            mine_clues_satisfied = False
        print(f"  Cell ({r},{c}): value={solution[r][c]}, neighbor_mines={count}, "
              f"mine_cells={mine_neighbors}, satisfied={satisfied}")
    
    print(f"\nmine_clues_satisfied: {mine_clues_satisfied}")
    print(f"is_valid_sudoku: True  (Sudoku constraints are hard)")
    
    # Print clue comparison
    print("\n=== CLUE COMPARISON ===")
    for r, c, v in sudoku_clues:
        actual = solution[r][c]
        match = "preserved" if actual == v else f"CHANGED ({v}->{actual})"
        print(f"  ({r},{c}): original={v}, solution={actual}, {match}")
else:
    print("STATUS: unsat")
    print("No solution found even without Sudoku clues")