from z3 import *

# Grid size
N = 24

# Palette: 0=white, 1=red, 2=green, 3=blue
# We'll use Int variables with domain {0,1,2,3}

# Create grid variables
grid = [[Int(f"g_{r}_{c}") for c in range(N)] for r in range(N)]

solver = Solver()

# Constraint 6: Each cell in {0,1,2,3}
for r in range(N):
    for c in range(N):
        solver.add(And(grid[r][c] >= 0, grid[r][c] <= 3))

# Helper: encode run clues for a sequence of N cells
# Given clues = list of (color, length) tuples, we need to encode that the sequence
# contains exactly those runs in order, with white (0) cells separating them,
# and no other colored cells.
#
# Approach: We'll use a "segment" encoding.
# Let there be K clues. We have K colored segments, each of exact length.
# Between segments there can be zero or more white cells.
# Before the first segment and after the last segment there can be zero or more white cells.
#
# We'll use integer variables for the start positions of each segment.
# For clue i (0-indexed), let start_i be the starting column (0-indexed).
# Then cells from start_i to start_i + length_i - 1 are of the given color.
# All other cells are white (0).
#
# Constraints:
# 0 <= start_0
# start_i + length_i <= start_{i+1}  (segments don't overlap, at least one cell gap)
# start_{K-1} + length_{K-1} <= N
# For each cell in segment i: grid[row][col] == color_i
# For cells not in any segment: grid[row][col] == 0

def add_row_clues(solver, row_idx, clues):
    K = len(clues)
    starts = [Int(f"rs_{row_idx}_{i}") for i in range(K)]
    for i in range(K):
        solver.add(starts[i] >= 0)
        solver.add(starts[i] < N)
    # Ordering: segments must be in order with at least one gap
    for i in range(K - 1):
        solver.add(starts[i] + clues[i][1] <= starts[i + 1])
    # Last segment must fit
    solver.add(starts[K - 1] + clues[K - 1][1] <= N)
    
    # For each cell, determine if it belongs to a segment
    for c in range(N):
        # Check if cell c is in any segment
        in_any_segment = False
        for i in range(K):
            color, length = clues[i]
            in_seg = And(starts[i] <= c, c < starts[i] + length)
            if in_any_segment is False:
                in_any_segment = in_seg
            else:
                in_any_segment = Or(in_any_segment, in_seg)
        # If in a segment, the color must match; otherwise white
        # We need to handle multiple segments: for each segment, if c is in that segment, color must match
        # Build implication for each segment
        for i in range(K):
            color, length = clues[i]
            solver.add(Implies(And(starts[i] <= c, c < starts[i] + length), grid[row_idx][c] == color))
        # If not in any segment, must be white
        solver.add(Implies(Not(in_any_segment), grid[row_idx][c] == 0))

def add_col_clues(solver, col_idx, clues):
    K = len(clues)
    starts = [Int(f"cs_{col_idx}_{i}") for i in range(K)]
    for i in range(K):
        solver.add(starts[i] >= 0)
        solver.add(starts[i] < N)
    for i in range(K - 1):
        solver.add(starts[i] + clues[i][1] <= starts[i + 1])
    solver.add(starts[K - 1] + clues[K - 1][1] <= N)
    
    for r in range(N):
        in_any_segment = False
        for i in range(K):
            color, length = clues[i]
            in_seg = And(starts[i] <= r, r < starts[i] + length)
            if in_any_segment is False:
                in_any_segment = in_seg
            else:
                in_any_segment = Or(in_any_segment, in_seg)
        for i in range(K):
            color, length = clues[i]
            solver.add(Implies(And(starts[i] <= r, r < starts[i] + length), grid[r][col_idx] == color))
        solver.add(Implies(Not(in_any_segment), grid[r][col_idx] == 0))

# Row clues
row_clues = [
    [(1,10), (2,4), (1,10)],   # row 0
    [(1,10), (2,4), (1,10)],   # row 1
    [(1,2), (2,4), (1,2)],     # row 2
    [(1,2), (2,4), (1,2)],     # row 3
    [(1,2), (2,4), (1,2)],     # row 4
    [(1,2), (2,4), (1,2)],     # row 5
    [(1,2), (2,4), (1,2)],     # row 6
    [(1,2), (2,4), (1,2)],     # row 7
    [(1,2), (3,8), (1,2)],     # row 8
    [(1,2), (3,8), (1,2)],     # row 9
    [(1,2), (2,6), (3,8), (2,6), (1,2)],  # row 10
    [(1,2), (2,6), (3,8), (2,6), (1,2)],  # row 11
    [(1,2), (2,6), (3,8), (2,6), (1,2)],  # row 12
    [(1,2), (2,6), (3,8), (2,6), (1,2)],  # row 13
    [(1,2), (3,8), (1,2)],     # row 14
    [(1,2), (3,8), (1,2)],     # row 15
    [(1,2), (2,4), (1,2)],     # row 16
    [(1,2), (2,4), (1,2)],     # row 17
    [(1,2), (2,4), (1,2)],     # row 18
    [(1,2), (2,4), (1,2)],     # row 19
    [(1,2), (2,4), (1,2)],     # row 20
    [(1,2), (2,4), (1,2)],     # row 21
    [(1,10), (2,4), (1,10)],   # row 22
    [(1,10), (2,4), (1,10)],   # row 23
]

# Column clues
col_clues = [
    [(1,24)],                   # col 0
    [(1,24)],                   # col 1
    [(1,2), (2,4), (1,2)],     # col 2
    [(1,2), (2,4), (1,2)],     # col 3
    [(1,2), (2,4), (1,2)],     # col 4
    [(1,2), (2,4), (1,2)],     # col 5
    [(1,2), (2,4), (1,2)],     # col 6
    [(1,2), (2,4), (1,2)],     # col 7
    [(1,2), (3,8), (1,2)],     # col 8
    [(1,2), (3,8), (1,2)],     # col 9
    [(2,8), (3,8), (2,8)],     # col 10
    [(2,8), (3,8), (2,8)],     # col 11
    [(2,8), (3,8), (2,8)],     # col 12
    [(2,8), (3,8), (2,8)],     # col 13
    [(1,2), (3,8), (1,2)],     # col 14
    [(1,2), (3,8), (1,2)],     # col 15
    [(1,2), (2,4), (1,2)],     # col 16
    [(1,2), (2,4), (1,2)],     # col 17
    [(1,2), (2,4), (1,2)],     # col 18
    [(1,2), (2,4), (1,2)],     # col 19
    [(1,2), (2,4), (1,2)],     # col 20
    [(1,2), (2,4), (1,2)],     # col 21
    [(1,24)],                   # col 22
    [(1,24)],                   # col 23
]

# Add row clues
for r in range(N):
    add_row_clues(solver, r, row_clues[r])

# Add column clues
for c in range(N):
    add_col_clues(solver, c, col_clues[c])

# Main diagonal constraint
main_diag = [1, 1, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0, 0, 0, 0, 0, 1, 1]
for i in range(N):
    solver.add(grid[i][i] == main_diag[i])

# Anti-diagonal constraint
anti_diag = [1, 1, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0, 0, 0, 0, 0, 1, 1]
for i in range(N):
    solver.add(grid[i][N - 1 - i] == anti_diag[i])

print("Solving...")
result = solver.check()
print(f"Result: {result}")

if result == sat:
    m = solver.model()
    print("STATUS: sat")
    print("Solution found!")
    for r in range(N):
        row_vals = [m.eval(grid[r][c]).as_long() for c in range(N)]
        print(f"Row {r:2d}: {''.join(str(v) for v in row_vals)}")
else:
    print("STATUS: unsat")
    print("No solution found.")