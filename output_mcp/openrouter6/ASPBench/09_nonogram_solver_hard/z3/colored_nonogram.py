from z3 import *

# Problem data
GRID_SIZE = 24
COLORS = [0, 1, 2, 3]  # 0=white, 1=red, 2=green, 3=blue

# Row clues (color, length)
row_clues = [
    [(1,10), (2,4), (1,10)],  # Row 1
    [(1,10), (2,4), (1,10)],  # Row 2
    [(1,2), (2,4), (1,2)],    # Row 3
    [(1,2), (2,4), (1,2)],    # Row 4
    [(1,2), (2,4), (1,2)],    # Row 5
    [(1,2), (2,4), (1,2)],    # Row 6
    [(1,2), (2,4), (1,2)],    # Row 7
    [(1,2), (2,4), (1,2)],    # Row 8
    [(1,2), (3,8), (1,2)],    # Row 9
    [(1,2), (3,8), (1,2)],    # Row 10
    [(1,2), (2,6), (3,8), (2,6), (1,2)],  # Row 11
    [(1,2), (2,6), (3,8), (2,6), (1,2)],  # Row 12
    [(1,2), (2,6), (3,8), (2,6), (1,2)],  # Row 13
    [(1,2), (2,6), (3,8), (2,6), (1,2)],  # Row 14
    [(1,2), (3,8), (1,2)],    # Row 15
    [(1,2), (3,8), (1,2)],    # Row 16
    [(1,2), (2,4), (1,2)],    # Row 17
    [(1,2), (2,4), (1,2)],    # Row 18
    [(1,2), (2,4), (1,2)],    # Row 19
    [(1,2), (2,4), (1,2)],    # Row 20
    [(1,2), (2,4), (1,2)],    # Row 21
    [(1,2), (2,4), (1,2)],    # Row 22
    [(1,10), (2,4), (1,10)],  # Row 23
    [(1,10), (2,4), (1,10)],  # Row 24
]

# Column clues (color, length)
col_clues = [
    [(1,24)],  # Column 1
    [(1,24)],  # Column 2
    [(1,2), (2,4), (1,2)],    # Column 3
    [(1,2), (2,4), (1,2)],    # Column 4
    [(1,2), (2,4), (1,2)],    # Column 5
    [(1,2), (2,4), (1,2)],    # Column 6
    [(1,2), (2,4), (1,2)],    # Column 7
    [(1,2), (2,4), (1,2)],    # Column 8
    [(1,2), (3,8), (1,2)],    # Column 9
    [(1,2), (3,8), (1,2)],    # Column 10
    [(2,8), (3,8), (2,8)],    # Column 11
    [(2,8), (3,8), (2,8)],    # Column 12
    [(2,8), (3,8), (2,8)],    # Column 13
    [(2,8), (3,8), (2,8)],    # Column 14
    [(1,2), (3,8), (1,2)],    # Column 15
    [(1,2), (3,8), (1,2)],    # Column 16
    [(1,2), (2,4), (1,2)],    # Column 17
    [(1,2), (2,4), (1,2)],    # Column 18
    [(1,2), (2,4), (1,2)],    # Column 19
    [(1,2), (2,4), (1,2)],    # Column 20
    [(1,2), (2,4), (1,2)],    # Column 21
    [(1,2), (2,4), (1,2)],    # Column 22
    [(1,24)],  # Column 23
    [(1,24)],  # Column 24
]

# Diagonal sequences
main_diag = [1, 1, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0, 0, 0, 0, 0, 1, 1]
anti_diag = [1, 1, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0, 0, 0, 0, 0, 1, 1]

# Create solver
solver = Solver()

# Create grid variables
grid = [[Int(f'grid_{i}_{j}') for j in range(GRID_SIZE)] for i in range(GRID_SIZE)]

# Add domain constraints for grid cells
for i in range(GRID_SIZE):
    for j in range(GRID_SIZE):
        solver.add(grid[i][j] >= 0)
        solver.add(grid[i][j] <= 3)

# Add diagonal constraints
for i in range(GRID_SIZE):
    solver.add(grid[i][i] == main_diag[i])
    solver.add(grid[i][GRID_SIZE - 1 - i] == anti_diag[i])

# Function to add row constraints
def add_row_constraints(row_idx, clues):
    """Add constraints for a single row"""
    if not clues:
        return
    
    N = len(clues)
    # Create start position variables for each run
    starts = [Int(f'row_{row_idx}_start_{k}') for k in range(N)]
    
    # First run starts at or after 0
    solver.add(starts[0] >= 0)
    
    # Each run must fit within grid
    for k in range(N):
        color, length = clues[k]
        solver.add(starts[k] + length - 1 < GRID_SIZE)
    
    # Consecutive runs must have at least one white cell between them
    for k in range(N - 1):
        color_k, length_k = clues[k]
        solver.add(starts[k + 1] >= starts[k] + length_k + 1)
    
    # For each cell in the row, determine its color based on run positions
    for col in range(GRID_SIZE):
        # Build color expression using If conditions
        color_expr = 0  # Default white
        
        # Check each run in reverse order to build nested If
        for k in range(N - 1, -1, -1):
            color_k, length_k = clues[k]
            # If col is in this run, color should be color_k
            in_run = And(col >= starts[k], col < starts[k] + length_k)
            color_expr = If(in_run, color_k, color_expr)
        
        # Add constraint: grid cell equals computed color
        solver.add(grid[row_idx][col] == color_expr)

# Function to add column constraints
def add_col_constraints(col_idx, clues):
    """Add constraints for a single column"""
    if not clues:
        return
    
    N = len(clues)
    # Create start position variables for each run (start row index)
    starts = [Int(f'col_{col_idx}_start_{k}') for k in range(N)]
    
    # First run starts at or after 0
    solver.add(starts[0] >= 0)
    
    # Each run must fit within grid
    for k in range(N):
        color, length = clues[k]
        solver.add(starts[k] + length - 1 < GRID_SIZE)
    
    # Consecutive runs must have at least one white cell between them
    for k in range(N - 1):
        color_k, length_k = clues[k]
        solver.add(starts[k + 1] >= starts[k] + length_k + 1)
    
    # For each cell in the column, determine its color based on run positions
    for row in range(GRID_SIZE):
        # Build color expression using If conditions
        color_expr = 0  # Default white
        
        # Check each run in reverse order to build nested If
        for k in range(N - 1, -1, -1):
            color_k, length_k = clues[k]
            # If row is in this run, color should be color_k
            in_run = And(row >= starts[k], row < starts[k] + length_k)
            color_expr = If(in_run, color_k, color_expr)
        
        # Add constraint: grid cell equals computed color
        solver.add(grid[row][col_idx] == color_expr)

# Add all row constraints
for i in range(GRID_SIZE):
    add_row_constraints(i, row_clues[i])

# Add all column constraints
for j in range(GRID_SIZE):
    add_col_constraints(j, col_clues[j])

# Check and print results
BENCHMARK_MODE = True
result = solver.check()

if result == sat:
    model = solver.model()
    print("STATUS: sat")
    print("Solution found!")
    print("\nGrid (24x24):")
    for i in range(GRID_SIZE):
        row_vals = []
        for j in range(GRID_SIZE):
            val = model.eval(grid[i][j])
            row_vals.append(str(val))
        print(' '.join(row_vals))
    
    # Verify diagonals
    print("\nMain diagonal verification:")
    main_diag_vals = [model.eval(grid[i][i]) for i in range(GRID_SIZE)]
    print(f"Computed: {main_diag_vals}")
    print(f"Expected: {main_diag}")
    
    print("\nAnti-diagonal verification:")
    anti_diag_vals = [model.eval(grid[i][GRID_SIZE-1-i]) for i in range(GRID_SIZE)]
    print(f"Computed: {anti_diag_vals}")
    print(f"Expected: {anti_diag}")
    
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")