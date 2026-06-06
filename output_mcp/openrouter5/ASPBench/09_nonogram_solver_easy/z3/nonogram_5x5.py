from z3 import *

# Create solver
solver = Solver()

# Grid: 5x5, each cell is 0 (white) or 1 (black)
grid = [[Int(f"grid_{i}_{j}") for j in range(5)] for i in range(5)]

# Constraint 1: Each cell is 0 or 1
for i in range(5):
    for j in range(5):
        solver.add(Or(grid[i][j] == 0, grid[i][j] == 1))

# Helper function: encode line clues (groups of consecutive 1s)
# For a line of length n with clues [c1, c2, ..., ck], we need to place
# k groups of consecutive 1s of lengths c1..ck, separated by at least one 0.
#
# We model this by introducing start positions for each group.
# Let s_i be the start index (0-based) of group i.
# Constraints:
#   0 <= s_1
#   s_i + c_i <= s_{i+1} - 1  (at least one 0 between groups)
#   s_k + c_k <= n
# Then for each cell j:
#   cell[j] = 1 iff there exists a group i such that s_i <= j < s_i + c_i

def encode_line_clues(solver, cells, clues):
    """cells is a list of n Int variables (0/1), clues is a list of group lengths."""
    k = len(clues)
    n = len(cells)
    
    if k == 0:
        # No groups: all cells must be 0
        for j in range(n):
            solver.add(cells[j] == 0)
        return
    
    # Create start positions for each group
    starts = [Int(f"start_{i}") for i in range(k)]
    
    # Domain constraints for starts
    for i in range(k):
        solver.add(starts[i] >= 0)
        solver.add(starts[i] < n)
    
    # Ordering and separation: groups must be in order with at least one 0 between
    for i in range(k - 1):
        solver.add(starts[i] + clues[i] + 1 <= starts[i + 1])
    
    # Last group must fit within the line
    solver.add(starts[k - 1] + clues[k - 1] <= n)
    
    # Now define each cell: cell[j] = 1 iff it falls within some group
    for j in range(n):
        # cell[j] is 1 if j is in [s_i, s_i + c_i) for some i
        in_any_group = Or([And(starts[i] <= j, j < starts[i] + clues[i]) for i in range(k)])
        solver.add(cells[j] == If(in_any_group, 1, 0))

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

# Encode row constraints
for i in range(5):
    encode_line_clues(solver, [grid[i][j] for j in range(5)], row_clues[i])

# Encode column constraints
for j in range(5):
    encode_line_clues(solver, [grid[i][j] for i in range(5)], col_clues[j])

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