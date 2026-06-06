from z3 import *

def solve_sudoku():
    # Create a 9x9 grid of integer variables (1-9)
    grid = [[Int(f"cell_{i}_{j}") for j in range(9)] for i in range(9)]
    
    solver = Solver()
    
    # All cells must be between 1 and 9
    for i in range(9):
        for j in range(9):
            solver.add(grid[i][j] >= 1)
            solver.add(grid[i][j] <= 9)
    
    # Each row must contain all digits 1-9 exactly once
    for i in range(9):
        solver.add(Distinct([grid[i][j] for j in range(9)]))
    
    # Each column must contain all digits 1-9 exactly once
    for j in range(9):
        solver.add(Distinct([grid[i][j] for i in range(9)]))
    
    # Each 3x3 box must contain all digits 1-9 exactly once
    for box_row in range(0, 9, 3):
        for box_col in range(0, 9, 3):
            box_cells = []
            for i in range(box_row, box_row + 3):
                for j in range(box_col, box_col + 3):
                    box_cells.append(grid[i][j])
            solver.add(Distinct(box_cells))
    
    # Given clues (row, column, value)
    clues = [
        (0, 0, 5), (0, 1, 3), (0, 4, 7),
        (1, 0, 6), (1, 3, 1), (1, 4, 9), (1, 5, 5),
        (2, 1, 9), (2, 2, 8), (2, 7, 6),
        (3, 0, 8), (3, 4, 6), (3, 8, 3),
        (4, 0, 4), (4, 3, 8), (4, 5, 3), (4, 8, 1),
        (5, 0, 7), (5, 4, 2), (5, 8, 6),
        (6, 1, 6), (6, 6, 2), (6, 7, 8),
        (7, 3, 4), (7, 4, 1), (7, 5, 9), (7, 8, 5),
        (8, 4, 8), (8, 7, 7), (8, 8, 9)
    ]
    
    # Add clue constraints
    for row, col, val in clues:
        solver.add(grid[row][col] == val)
    
    # Check for solution
    result = solver.check()
    
    if result == sat:
        model = solver.model()
        print("STATUS: sat")
        print("Sudoku solution:")
        for i in range(9):
            row_vals = []
            for j in range(9):
                val = model[grid[i][j]]
                row_vals.append(str(val))
            print(" ".join(row_vals))
    elif result == unsat:
        print("STATUS: unsat")
        print("No solution exists - puzzle is unsatisfiable")
    else:
        print("STATUS: unknown")
        print("Solver could not determine satisfiability")

if __name__ == "__main__":
    solve_sudoku()