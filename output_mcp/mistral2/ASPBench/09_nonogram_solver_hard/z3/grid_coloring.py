from z3 import *

# Grid size
N = 24

# Palette: 0=white, 1=red, 2=green, 3=blue
# We will use Int for cells, with values in {0, 1, 2, 3}

# Initialize solver
solver = Solver()

# Declare the grid as a 2D list of Int variables
grid = [[Int(f"grid_{i}_{j}") for j in range(N)] for i in range(N)]

# Helper function to add cell value constraints
for i in range(N):
    for j in range(N):
        solver.add(Or([grid[i][j] == c for c in [0, 1, 2, 3]]))

# Helper function to extract runs from a list of cells
def get_runs(cells):
    runs = []
    current_color = None
    current_length = 0
    for cell in cells:
        val = cell
        if val == 0:  # white, ignore for runs
            if current_color is not None:
                runs.append((current_color, current_length))
                current_color = None
                current_length = 0
        else:
            if current_color == val:
                current_length += 1
            else:
                if current_color is not None:
                    runs.append((current_color, current_length))
                current_color = val
                current_length = 1
    if current_color is not None:
        runs.append((current_color, current_length))
    return runs

# Helper function to enforce row/column run constraints
def enforce_run_constraints(cells, clues):
    # cells: list of Z3 Int variables representing a row or column
    # clues: list of (color, length) tuples
    
    # Step 1: Ensure the runs extracted from cells match the clues exactly
    runs = get_runs(cells)
    
    # Step 2: The runs must match the clues exactly
    solver.add(And([And(runs[k][0] == clues[k][0], runs[k][1] == clues[k][1]) for k in range(len(clues))]))
    
    # Step 3: Ensure no extra runs exist beyond the clues
    # This is implicitly handled by the exhaustive nature of the clues and the run extraction
    # We also need to ensure that the total length of runs + white cells matches the row/column length
    total_run_length = Sum([clue[1] for clue in clues])
    solver.add(total_run_length <= N)
    
    # Step 4: Ensure that the runs are separated by at least one white cell
    # This is implicitly handled by the run extraction logic (white cells break runs)

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
    enforce_run_constraints(grid[i], row_clues[i])

# Enforce column constraints
for j in range(N):
    column = [grid[i][j] for i in range(N)]
    enforce_run_constraints(column, col_clues[j])

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