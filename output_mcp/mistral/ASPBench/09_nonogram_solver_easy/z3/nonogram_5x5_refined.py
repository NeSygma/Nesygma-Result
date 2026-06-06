from z3 import *

# BENCHMARK_MODE: ON (problem is guaranteed solvable)
BENCHMARK_MODE = True

# Create a 5x5 grid of Int variables (0=white, 1=black)
# grid[i][j] for row i, column j (0-indexed)
grid = [[Int(f"grid_{i}_{j}") for j in range(5)] for i in range(5)]

# Each cell is 0 or 1
solver = Solver()
for i in range(5):
    for j in range(5):
        solver.add(Or(grid[i][j] == 0, grid[i][j] == 1))

# Helper function to encode a single line (row or column) with a given clue
# clue: list of group lengths (e.g., [2] or [1,1])
# line: list of Z3 variables representing the line (row or column)
def encode_line(clue, line):
    n = len(line)
    m = len(clue)
    
    # If the clue is empty, the line must be all white
    if m == 0:
        for cell in line:
            solver.add(cell == 0)
        return
    
    # Total length of all groups plus required separators
    total_required = sum(clue) + max(0, m - 1)
    
    # The line must have at least total_required cells
    # (This is always true for n >= total_required, but we assert it for clarity)
    solver.add(total_required <= n)
    
    # We'll use a list of positions where groups start
    starts = [Int(f"start_{i}") for i in range(m)]
    
    # Each start must be in [0, n - clue[i]]
    for i in range(m):
        solver.add(starts[i] >= 0)
        solver.add(starts[i] <= n - clue[i])
    
    # Groups must not overlap and must be separated by at least one white cell
    for i in range(m):
        # Group i occupies [starts[i], starts[i] + clue[i] - 1]
        # Ensure all cells in the group are black
        for k in range(clue[i]):
            solver.add(line[starts[i] + k] == 1)
        
        # Ensure the cell before the group (if exists) is white
        if starts[i] > 0:
            solver.add(line[starts[i] - 1] == 0)
        
        # Ensure the cell after the group (if exists) is white
        if starts[i] + clue[i] < n:
            solver.add(line[starts[i] + clue[i]] == 0)
    
    # Ensure groups are in order and separated
    for i in range(m - 1):
        # Group i must end before group i+1 starts
        solver.add(starts[i] + clue[i] < starts[i + 1])
    
    # Ensure no other black cells outside the groups
    # We'll add constraints to ensure that the total number of black cells
    # is exactly sum(clue)
    total_black = Sum(line)
    solver.add(total_black == sum(clue))

# Row clues (0-indexed rows)
row_clues = [
    [2],      # Row 0
    [1],      # Row 1
    [3],      # Row 2
    [1, 1],   # Row 3
    [2]       # Row 4
]

# Encode row constraints
for i in range(5):
    encode_line(row_clues[i], grid[i])

# Column clues (0-indexed columns)
col_clues = [
    [1, 1],   # Column 0
    [1, 3],   # Column 1
    [2],      # Column 2
    [1],      # Column 3
    [1]       # Column 4
]

# Encode column constraints
for j in range(5):
    column = [grid[i][j] for i in range(5)]
    encode_line(col_clues[j], column)

# Check for a solution
result = solver.check()

if result == sat:
    model = solver.model()
    print("STATUS: sat")
    print("valid = True")
    # Print the grid
    for i in range(5):
        row_str = "".join([str(model[grid[i][j]]) for j in range(5)])
        print(f"grid[{i}] = {row_str}")
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")