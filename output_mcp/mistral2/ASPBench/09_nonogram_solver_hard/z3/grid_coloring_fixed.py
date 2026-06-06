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
    # We also need to ensure that the runs do not overlap and are separated properly.
    
    # Start by setting all cells to white (0)
    for cell in cells:
        solver.add(cell == 0)
    
    # Place the runs in the correct positions
    pos = 0
    for color, length in clues:
        # Ensure the run fits in the remaining cells
        if pos + length > N:
            return False  # Run does not fit
        
        # Place the run of 'length' cells of 'color' starting at 'pos'
        for k in range(length):
            solver.add(cells[pos + k] == color)
        
        # Move the position to the end of the run
        pos += length
        
        # Ensure the next cell is white (0) if there are more clues
        if pos < N and clues.index((color, length)) < len(clues) - 1:
            solver.add(cells[pos] == 0)
            pos += 1
    
    return True

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
    if not enforce_runs([grid[i][j] for j in range(N)], row_clues[i]):
        print("STATUS: unsat")
        print("RAW_RESULT: unsat (run does not fit in row; modeling error)")
        exit()

# Enforce column constraints
for j in range(N):
    if not enforce_runs([grid[i][j] for i in range(N)], col_clues[j]):
        print("STATUS: unsat")
        print("RAW_RESULT: unsat (run does not fit in column; modeling error)")
        exit()

# Main diagonal constraint: grid[i][i] for i in 0..23
main_diag = [grid[i][i] for i in range(N)]
expected_main_diag = [1, 1, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0, 0, 0, 0, 1, 1]
for i in range(N):
    solver.add(main_diag[i] == expected_main_diag[i])

# Anti-diagonal constraint: grid[i][23-i] for i in 0..23
anti_diag = [grid[i][N-1-i] for i in range(N)]
expected_anti_diag = [1, 1, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0, 0, 0, 0, 1, 1]
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
        row_str = " ".join([str(model[grid[i][j]]) for j in range(N)])
        print(f"Row {i+1}: {row_str}")
    print("Valid solution found!")
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")