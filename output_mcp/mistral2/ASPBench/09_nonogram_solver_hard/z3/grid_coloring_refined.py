from z3 import *

# Grid size
N = 24

# Initialize solver
solver = Solver()

# Declare the grid as a 2D list of Int variables
grid = [[Int(f"grid_{i}_{j}") for j in range(N)] for i in range(N)]

# Helper function to add cell value constraints
for i in range(N):
    for j in range(N):
        solver.add(Or([grid[i][j] == c for c in [0, 1, 2, 3]]))

# Helper function to enforce a sequence of runs in a list of cells
def enforce_runs(cells, clues):
    # cells: list of Z3 Int variables representing a row or column
    # clues: list of (color, length) tuples
    
    # We will encode the runs directly by placing the runs in the correct positions
    # and ensuring the rest are white (0).
    
    # Start with all cells as white (0)
    for cell in cells:
        solver.add(cell == 0)
    
    # Place the runs in the correct positions
    pos = 0
    for color, length in clues:
        # Place the run of 'length' cells of 'color' starting at 'pos'
        for k in range(length):
            solver.add(cells[pos + k] == color)
        pos += length
        # Ensure the next cell is white (0) if there are more clues
        if pos < N:
            solver.add(cells[pos] == 0)
            pos += 1

# Row clues
row_clues = [
    [(1,10), (2,4), (1,10)],
    [(1,10), (2,4), (1,10)],
    [(1,2), (2,4), (1,2)],
    [(1,2), (2,4), (1,2)],
    [(1,2), (2,4), (1,2)],
    [(1,2), (2,4), (1,2)],
    [(1,2), (2,4), (1,2)],
    [(1,2), (2,4), (1,2)],
    [(1,2), (3,8), (1,2)],
    [(1,2), (3,8), (1,2)],
    [(1,2), (2,6), (3,8), (2,6), (1,2)],
    [(1,2), (2,6), (3,8), (2,6), (1,2)],
    [(1,2), (2,6), (3,8), (2,6), (1,2)],
    [(1,2), (2,6), (3,8), (2,6), (1,2)],
    [(1,2), (3,8), (1,2)],
    [(1,2), (3,8), (1,2)],
    [(1,2), (2,4), (1,2)],
    [(1,2), (2,4), (1,2)],
    [(1,2), (2,4), (1,2)],
    [(1,2), (2,4), (1,2)],
    [(1,2), (2,4), (1,2)],
    [(1,2), (2,4), (1,2)],
    [(1,10), (2,4), (1,10)],
    [(1,10), (2,4), (1,10)]
]

# Column clues
col_clues = [
    [(1,24)],
    [(1,24)],
    [(1,2), (2,4), (1,2)],
    [(1,2), (2,4), (1,2)],
    [(1,2), (2,4), (1,2)],
    [(1,2), (2,4), (1,2)],
    [(1,2), (2,4), (1,2)],
    [(1,2), (2,4), (1,2)],
    [(1,2), (3,8), (1,2)],
    [(1,2), (3,8), (1,2)],
    [(2,8), (3,8), (2,8)],
    [(2,8), (3,8), (2,8)],
    [(2,8), (3,8), (2,8)],
    [(2,8), (3,8), (2,8)],
    [(1,2), (3,8), (1,2)],
    [(1,2), (3,8), (1,2)],
    [(1,2), (2,4), (1,2)],
    [(1,2), (2,4), (1,2)],
    [(1,2), (2,4), (1,2)],
    [(1,2), (2,4), (1,2)],
    [(1,2), (2,4), (1,2)],
    [(1,2), (2,4), (1,2)],
    [(1,24)],
    [(1,24)]
]

# Enforce row constraints
for i in range(N):
    enforce_runs(grid[i], row_clues[i])

# Enforce column constraints
for j in range(N):
    column = [grid[i][j] for i in range(N)]
    enforce_runs(column, col_clues[j])

# Main diagonal constraint: grid[i][i] for i in 0..23
main_diag = [grid[i][i] for i in range(N)]
expected_main_diag = [1, 1, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0, 0, 0, 0, 0, 1, 1]
for i in range(N):
    solver.add(main_diag[i] == expected_main_diag[i])

# Anti-diagonal constraint: grid[i][23-i] for i in 0..23
anti_diag = [grid[i][N-1-i] for i in range(N)]
expected_anti_diag = [1, 1, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0, 0, 0, 0, 0, 1, 1]
for i in range(N):
    solver.add(anti_diag[i] == expected_anti_diag[i])

# Check for a solution
BENCHMARK_MODE = True
result = solver.check()

if result == sat:
    model = solver.model()
    print("STATUS: sat")
    # Print the grid in a readable format
    for i in range(N):
        row_str = " ".join(str(model[grid[i][j]]) for j in range(N))
        print(f"Row {i+1}: {row_str}")
    print("Valid solution found!")
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")