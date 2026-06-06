from z3 import *

# Create solver
solver = Solver()

# Grid: 5x5, each cell is 0 (white) or 1 (black)
grid = [[Int(f"grid_{i}_{j}") for j in range(5)] for i in range(5)]

# Constraint 1: Each cell is 0 or 1
for i in range(5):
    for j in range(5):
        solver.add(Or(grid[i][j] == 0, grid[i][j] == 1))

# Helper function: encode line clues using a different approach
# We'll use a "run-length encoding" approach.
# For a line of length n with clues [c1, c2, ..., ck]:
# We need exactly k groups of consecutive 1s with lengths c1..ck.
# Between groups there must be at least one 0.
# Before the first group and after the last group there can be any number of 0s.
#
# We model this by creating variables for the number of leading zeros,
# then for each group: the group itself, then at least one zero (except after last group).
#
# Let lead = number of zeros before first group
# For each group i: group of c_i ones, then gap_i zeros (gap_i >= 1 for i < k-1, gap_{k-1} >= 0)
# lead + c1 + gap1 + c2 + gap2 + ... + ck + gap_{k-1} = n

def encode_line_clues(solver, cells, clues):
    k = len(clues)
    n = len(cells)
    
    if k == 0:
        for j in range(n):
            solver.add(cells[j] == 0)
        return
    
    # lead: zeros before first group
    lead = Int(f"lead_{id(cells)}")
    solver.add(lead >= 0)
    
    # gaps: zeros between groups (and after last group)
    gaps = [Int(f"gap_{id(cells)}_{i}") for i in range(k)]
    # gaps[0..k-2] must be >= 1 (at least one zero between groups)
    # gaps[k-1] must be >= 0 (zeros after last group)
    for i in range(k - 1):
        solver.add(gaps[i] >= 1)
    solver.add(gaps[k - 1] >= 0)
    
    # Total length constraint
    total = lead + clues[0] + gaps[0]
    for i in range(1, k):
        total = total + clues[i] + gaps[i]
    solver.add(total == n)
    
    # Now define each cell position
    # We need to know for each cell j whether it falls in a group or not.
    # We can compute the start position of each group:
    # start_i = lead + sum_{p < i} (clues[p] + gaps[p])
    # Then cell j is 1 iff start_i <= j < start_i + clues[i] for some i
    
    # Compute start positions symbolically
    starts = []
    for i in range(k):
        s = lead
        for p in range(i):
            s = s + clues[p] + gaps[p]
        starts.append(s)
    
    # For each cell j, it's 1 if it falls in any group
    for j in range(n):
        in_any = False
        for i in range(k):
            # j is in group i if starts[i] <= j < starts[i] + clues[i]
            cond = And(starts[i] <= j, j < starts[i] + clues[i])
            if in_any is False:
                in_any = cond
            else:
                in_any = Or(in_any, cond)
        solver.add(cells[j] == If(in_any, 1, 0))

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