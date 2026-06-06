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

# Use a different approach: enumerate all possible placements for each line
# For a line of length n with clues [c1,...,ck], we can generate all valid
# binary strings and then use an OR constraint.

def generate_line_patterns(n, clues):
    """Generate all valid binary patterns for a line of length n with given clues."""
    k = len(clues)
    patterns = []
    
    if k == 0:
        patterns.append([0] * n)
        return patterns
    
    # Recursively generate
    def backtrack(pos, clue_idx, current):
        if clue_idx == k:
            # Fill rest with zeros
            current = current + [0] * (n - pos)
            patterns.append(current)
            return
        
        c = clues[clue_idx]
        # Need at least c cells for this block, plus (k - clue_idx - 1) cells for remaining blocks
        # plus (k - clue_idx - 1) cells for separators
        min_remaining = c
        for rem in range(clue_idx + 1, k):
            min_remaining += clues[rem] + 1  # block + separator
        
        max_start = n - min_remaining
        
        for start in range(pos, max_start + 1):
            # Place zeros from pos to start-1
            new_current = current + [0] * (start - pos)
            # Place the block
            new_current = new_current + [1] * c
            # If not last block, add a separator zero
            if clue_idx < k - 1:
                new_current = new_current + [0]
                backtrack(start + c + 1, clue_idx + 1, new_current)
            else:
                backtrack(start + c, clue_idx + 1, new_current)
    
    backtrack(0, 0, [])
    return patterns

# Encode row constraints
for i in range(5):
    patterns = generate_line_patterns(5, row_clues[i])
    # At least one pattern must match
    row_cells = [grid[i][j] for j in range(5)]
    pattern_conds = []
    for pat in patterns:
        cond = True
        for j in range(5):
            cond = And(cond, row_cells[j] == pat[j])
        pattern_conds.append(cond)
    solver.add(Or(pattern_conds))

# Encode column constraints
for j in range(5):
    patterns = generate_line_patterns(5, col_clues[j])
    col_cells = [grid[i][j] for i in range(5)]
    pattern_conds = []
    for pat in patterns:
        cond = True
        for i in range(5):
            cond = And(cond, col_cells[i] == pat[i])
        pattern_conds.append(cond)
    solver.add(Or(pattern_conds))

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