from z3 import *

# Create solver
solver = Solver()

# Grid: 5x5, each cell is 0 (white) or 1 (black)
grid = [[Int(f"grid_{i}_{j}") for j in range(5)] for i in range(5)]

# Constraint 1: Each cell is 0 or 1
for i in range(5):
    for j in range(5):
        solver.add(Or(grid[i][j] == 0, grid[i][j] == 1))

# Row clues
row_clues = [
    [2],
    [1],
    [3],
    [1, 1],
    [2]
]

# Column clues
col_clues = [
    [1, 1],
    [1, 3],
    [2],
    [1],
    [1]
]

# Helper: encode line clues using a different approach
# We'll use a "block position" approach.
# For clues [c1, c2, ..., ck] on a line of length n:
# Let start_i be the starting position (0-indexed) of the i-th block.
# Constraints:
#   start_i >= 0
#   start_i + c_i <= n
#   start_i + c_i + 1 <= start_{i+1}  (at least one white between blocks)
#   For each cell j: cell[j] = 1 iff start_i <= j < start_i + c_i for some i

def encode_line(solver, cells, clues):
    n = len(cells)
    k = len(clues)
    
    if k == 0:
        for j in range(n):
            solver.add(cells[j] == 0)
        return
    
    starts = [Int(f"start_{id(cells)}_{i}") for i in range(k)]
    
    for i in range(k):
        solver.add(starts[i] >= 0)
        solver.add(starts[i] + clues[i] <= n)
    
    for i in range(k - 1):
        solver.add(starts[i] + clues[i] + 1 <= starts[i+1])
    
    # For each cell j, it's 1 if it falls in any block
    for j in range(n):
        in_block = False
        for i in range(k):
            cond = And(starts[i] <= j, j < starts[i] + clues[i])
            if in_block is False:
                in_block = cond
            else:
                in_block = Or(in_block, cond)
        solver.add(cells[j] == If(in_block, 1, 0))

# Encode row constraints
for i in range(5):
    encode_line(solver, [grid[i][j] for j in range(5)], row_clues[i])

# Encode column constraints
for j in range(5):
    encode_line(solver, [grid[i][j] for i in range(5)], col_clues[j])

# Solve
BENCHMARK_MODE = True
result = solver.check()

if result == sat:
    m = solver.model()
    print("STATUS: sat")
    print("Solution found:")
    for i in range(5):
        row_str = ""
        for j in range(5):
            val = m.eval(grid[i][j]).as_long()
            row_str += str(val) + " "
        print(f"Row {i}: {row_str}")
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")