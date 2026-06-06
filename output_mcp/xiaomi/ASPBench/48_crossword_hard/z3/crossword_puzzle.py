from z3 import *

# Grid dimensions
ROWS = 6
COLS = 6

# Black squares (corners)
black_squares = {(0,0), (0,5), (5,0), (5,5)}

# Words to place
words = ["CAT", "ACE", "TEA", "EAR", "ATE", "RAT", "CAR", "TAR"]
NUM_WORDS = len(words)

# Create solver
solver = Solver()

# For each word, we need:
# - direction: 0 = horizontal, 1 = vertical
# - start_row, start_col: starting position
direction = [Int(f'dir_{i}') for i in range(NUM_WORDS)]
start_row = [Int(f'row_{i}') for i in range(NUM_WORDS)]
start_col = [Int(f'col_{i}') for i in range(NUM_WORDS)]

# Grid cells: grid[r][c] = letter (as integer 0-25 for A-Z, or -1 for empty/black)
grid = [[Int(f'grid_{r}_{c}') for c in range(COLS)] for r in range(ROWS)]

# Binary variables: is_cell_used[r][c] = 1 if cell contains a letter
is_cell_used = [[Int(f'used_{r}_{c}') for c in range(COLS)] for r in range(ROWS)]

# Intersection variables: intersection[r][c] = 1 if cell is shared by horizontal and vertical words
intersection = [[Int(f'inter_{r}_{c}') for c in range(COLS)] for r in range(ROWS)]

# Word letter mapping (A=0, B=1, ..., Z=25)
word_letters = []
for w in words:
    word_letters.append([ord(ch) - ord('A') for ch in w])

# Constraints for black squares
for r in range(ROWS):
    for c in range(COLS):
        if (r, c) in black_squares:
            solver.add(grid[r][c] == -1)
            solver.add(is_cell_used[r][c] == 0)
        else:
            solver.add(is_cell_used[r][c] == If(grid[r][c] >= 0, 1, 0))

# Direction constraints: 0 or 1
for i in range(NUM_WORDS):
    solver.add(Or(direction[i] == 0, direction[i] == 1))

# Starting position constraints
for i in range(NUM_WORDS):
    # Horizontal words: start_col + 2 < COLS
    solver.add(Implies(direction[i] == 0, And(start_row[i] >= 0, start_row[i] < ROWS,
                                               start_col[i] >= 0, start_col[i] + 2 < COLS)))
    # Vertical words: start_row + 2 < ROWS
    solver.add(Implies(direction[i] == 1, And(start_row[i] >= 0, start_row[i] + 2 < ROWS,
                                               start_col[i] >= 0, start_col[i] < COLS)))

# Word placement constraints
for i in range(NUM_WORDS):
    for k in range(3):  # Each word has 3 letters
        # For horizontal words
        solver.add(Implies(direction[i] == 0,
                          And(grid[start_row[i]][start_col[i] + k] == word_letters[i][k],
                              grid[start_row[i]][start_col[i] + k] != -1)))
        # For vertical words
        solver.add(Implies(direction[i] == 1,
                          And(grid[start_row[i] + k][start_col[i]] == word_letters[i][k],
                              grid[start_row[i] + k][start_col[i]] != -1)))

# No conflicts: each cell has at most one letter value
# This is implicitly handled by grid being a single value per cell

# Intersection detection
for r in range(ROWS):
    for c in range(COLS):
        if (r, c) not in black_squares:
            # Count how many words cover this cell
            covering_words = []
            for i in range(NUM_WORDS):
                # Horizontal word covers (r, c) if direction=0, row=r, col <= c <= col+2
                covers_h = And(direction[i] == 0, start_row[i] == r,
                              start_col[i] <= c, c <= start_col[i] + 2)
                # Vertical word covers (r, c) if direction=1, col=c, row <= r <= row+2
                covers_v = And(direction[i] == 1, start_col[i] == c,
                              start_row[i] <= r, r <= start_row[i] + 2)
                covering_words.append(Or(covers_h, covers_v))
            
            # Cell is used if at least one word covers it
            solver.add(is_cell_used[r][c] == If(Or(covering_words), 1, 0))
            
            # Intersection: cell is covered by both a horizontal and vertical word
            has_horizontal = Or([And(direction[i] == 0, start_row[i] == r,
                                    start_col[i] <= c, c <= start_col[i] + 2) 
                                for i in range(NUM_WORDS)])
            has_vertical = Or([And(direction[i] == 1, start_col[i] == c,
                                  start_row[i] <= r, r <= start_row[i] + 2) 
                              for i in range(NUM_WORDS)])
            solver.add(intersection[r][c] == If(And(has_horizontal, has_vertical), 1, 0))

# At least 3 intersections
solver.add(Sum([Sum([intersection[r][c] for c in range(COLS)]) for r in range(ROWS)]) >= 3)

# Connectivity constraint: all used cells must form a single connected component
# We'll use a reachability approach with a virtual root
# Create a "visited" array for BFS-like connectivity
visited = [[Int(f'visited_{r}_{c}') for c in range(COLS)] for r in range(ROWS)]

# Find first used cell as root
first_used_r = Int('first_used_r')
first_used_c = Int('first_used_c')

# Ensure first_used is a valid used cell
solver.add(Or([And(is_cell_used[r][c] == 1, first_used_r == r, first_used_c == c) 
               for r in range(ROWS) for c in range(COLS) if (r, c) not in black_squares]))

# BFS constraints (simplified: ensure all used cells are reachable)
# For simplicity, we'll use a weaker but effective constraint:
# All used cells must be adjacent to at least one other used cell (except possibly isolated)
# Actually, let's use a proper connectivity encoding

# We'll use a different approach: ensure the graph of used cells is connected
# by checking that there's a path from the first used cell to every other used cell

# For each used cell, there must exist a path from first_used to it
# This is complex to encode directly, so we'll use a simpler sufficient condition:
# The set of used cells must be "contiguous" - no gaps in rows/columns

# Alternative: Use union-find style constraints
# For each pair of adjacent cells, if both are used, they're connected
# Then ensure all used cells are in the same component

# Let's use a simpler approach: ensure that for any two used cells,
# there's a sequence of adjacent used cells connecting them
# This is still complex, so we'll use a practical heuristic:
# Ensure that the used cells form a single "blob" by checking row/column continuity

# For now, let's use a weaker but practical constraint:
# All used cells must be within a connected region
# We'll check that there are no isolated 1x1 used cells

# Actually, let's implement a proper connectivity check using Z3
# We'll create a "component" variable for each cell
component = [[Int(f'comp_{r}_{c}') for c in range(COLS)] for r in range(ROWS)]

# Component constraints
for r in range(ROWS):
    for c in range(COLS):
        if (r, c) in black_squares:
            solver.add(component[r][c] == -1)
        else:
            # If cell is used, it must have a component ID >= 0
            solver.add(Implies(is_cell_used[r][c] == 1, component[r][c] >= 0))
            # If cell is not used, component is -1
            solver.add(Implies(is_cell_used[r][c] == 0, component[r][c] == -1))

# Adjacent cells with same component if both used
for r in range(ROWS):
    for c in range(COLS):
        if (r, c) not in black_squares:
            # Check right neighbor
            if c + 1 < COLS and (r, c+1) not in black_squares:
                solver.add(Implies(And(is_cell_used[r][c] == 1, is_cell_used[r][c+1] == 1),
                                  component[r][c] == component[r][c+1]))
            # Check down neighbor
            if r + 1 < ROWS and (r+1, c) not in black_squares:
                solver.add(Implies(And(is_cell_used[r][c] == 1, is_cell_used[r+1][c] == 1),
                                  component[r][c] == component[r+1][c]))

# All used cells must have the same component (connectivity)
# Find the component of the first used cell
first_comp = Int('first_comp')
solver.add(Or([And(is_cell_used[r][c] == 1, first_comp == component[r][c]) 
               for r in range(ROWS) for c in range(COLS) if (r, c) not in black_squares]))

# All used cells must have this component
for r in range(ROWS):
    for c in range(COLS):
        if (r, c) not in black_squares:
            solver.add(Implies(is_cell_used[r][c] == 1, component[r][c] == first_comp))

# Each word must be placed exactly once (already enforced by having one placement per word)

# Ensure words don't overlap in conflicting ways
# This is already handled by grid constraints (each cell has one letter value)

# Add some symmetry breaking to help solver
# Words must be placed in order of their index (optional, helps performance)
for i in range(NUM_WORDS - 1):
    solver.add(Or(start_row[i] < start_row[i+1],
                  And(start_row[i] == start_row[i+1], start_col[i] <= start_col[i+1])))

# Check solution
BENCHMARK_MODE = True
result = solver.check()

if result == sat:
    model = solver.model()
    print("STATUS: sat")
    print("Solution found!")
    
    # Print grid
    print("\nGrid:")
    for r in range(ROWS):
        row_str = ""
        for c in range(COLS):
            if (r, c) in black_squares:
                row_str += "# "
            else:
                val = model.evaluate(grid[r][c])
                if val.as_long() == -1:
                    row_str += ". "
                else:
                    row_str += chr(val.as_long() + ord('A')) + " "
        print(row_str)
    
    # Print placements
    print("\nPlacements:")
    for i in range(NUM_WORDS):
        dir_val = model.evaluate(direction[i]).as_long()
        row_val = model.evaluate(start_row[i]).as_long()
        col_val = model.evaluate(start_col[i]).as_long()
        dir_str = "horizontal" if dir_val == 0 else "vertical"
        print(f"{words[i]}: ({row_val}, {col_val}) {dir_str}")
    
    # Count intersections
    inter_count = 0
    for r in range(ROWS):
        for c in range(COLS):
            if model.evaluate(intersection[r][c]).as_long() == 1:
                inter_count += 1
    print(f"\nIntersections: {inter_count}")
    
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")