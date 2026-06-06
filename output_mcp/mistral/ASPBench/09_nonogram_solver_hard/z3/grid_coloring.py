from z3 import *

# Create a 24x24 grid of integer variables
N = 24
solver = Solver()
grid = [[Int(f"grid_{i}_{j}") for j in range(N)] for i in range(N)]

# Each cell must be in {0, 1, 2, 3}
for i in range(N):
    for j in range(N):
        solver.add(grid[i][j] >= 0, grid[i][j] <= 3)

# Main diagonal constraints
diag_seq = [1, 1, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0, 0, 0, 0, 0, 1, 1]
for i in range(N):
    solver.add(grid[i][i] == diag_seq[i])

# Anti-diagonal constraints
anti_diag_seq = [1, 1, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0, 0, 0, 0, 0, 1, 1]
for i in range(N):
    solver.add(grid[i][N-1-i] == anti_diag_seq[i])

# Helper function to encode row constraints
def encode_row_constraints(solver, grid, row_idx, clues):
    n = N
    k = len(clues)
    
    # Total colored cells required
    total_colored = sum(length for color, length in clues)
    
    # Create run segment variables: start and end positions for each run
    starts = [Int(f"row{row_idx}_run{run_idx}_start") for run_idx in range(k)]
    ends = [Int(f"row{row_idx}_run{run_idx}_end") for run_idx in range(k)]
    
    # Each run must have the correct length
    for run_idx, (color, length) in enumerate(clues):
        solver.add(ends[run_idx] - starts[run_idx] + 1 == length)
        # All cells in this run must have the correct color
        for j in range(n):
            in_run = And(starts[run_idx] <= j, j <= ends[run_idx])
            solver.add(Implies(in_run, grid[row_idx][j] == color))
    
    # Runs must be in order and non-overlapping
    for run_idx in range(k-1):
        solver.add(ends[run_idx] < starts[run_idx+1])
    
    # Runs must be within bounds
    solver.add(starts[0] >= 0)
    solver.add(ends[k-1] < n)
    
    # All colored cells must be part of some run
    for j in range(n):
        is_colored = grid[row_idx][j] != 0
        in_some_run = Or([And(starts[run_idx] <= j, j <= ends[run_idx]) for run_idx in range(k)])
        solver.add(Implies(is_colored, in_some_run))

# Helper function to encode column constraints
def encode_col_constraints(solver, grid, col_idx, clues):
    n = N
    k = len(clues)
    
    # Total colored cells required
    total_colored = sum(length for color, length in clues)
    
    # Create run segment variables: start and end positions for each run
    starts = [Int(f"col{col_idx}_run{run_idx}_start") for run_idx in range(k)]
    ends = [Int(f"col{col_idx}_run{run_idx}_end") for run_idx in range(k)]
    
    # Each run must have the correct length
    for run_idx, (color, length) in enumerate(clues):
        solver.add(ends[run_idx] - starts[run_idx] + 1 == length)
        # All cells in this run must have the correct color
        for i in range(n):
            in_run = And(starts[run_idx] <= i, i <= ends[run_idx])
            solver.add(Implies(in_run, grid[i][col_idx] == color))
    
    # Runs must be in order and non-overlapping
    for run_idx in range(k-1):
        solver.add(ends[run_idx] < starts[run_idx+1])
    
    # Runs must be within bounds
    solver.add(starts[0] >= 0)
    solver.add(ends[k-1] < n)
    
    # All colored cells must be part of some run
    for i in range(n):
        is_colored = grid[i][col_idx] != 0
        in_some_run = Or([And(starts[run_idx] <= i, i <= ends[run_idx]) for run_idx in range(k)])
        solver.add(Implies(is_colored, in_some_run))

# Row clues (color, length)
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

# Column clues (color, length)
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

# Add row constraints
for i in range(N):
    encode_row_constraints(solver, grid, i, row_clues[i])

# Add column constraints
for j in range(N):
    encode_col_constraints(solver, grid, j, col_clues[j])

# Check for a solution
BENCHMARK_MODE = True
result = solver.check()

if result == sat:
    model = solver.model()
    print("STATUS: sat")
    # Print a small portion of the grid to verify
    print("Sample of grid values:")
    for i in range(min(5, N)):
        row_str = "".join(str(model.eval(grid[i][j], model_completion=True)) for j in range(min(24, 10)))
        print(f"Row {i}: {row_str}")
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")