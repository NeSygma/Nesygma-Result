from z3 import *

# Grid is 5x5
GRID_SIZE = 5

# Word list
words_data = [
    ("CODE", 4),
    ("DATA", 4),
    ("TECH", 4),
    ("CHIP", 4),
    ("BYTE", 4),
    ("NET", 3)
]

word_strings = [w[0] for w in words_data]
word_lengths = [w[1] for w in words_data]
N = len(words_data)  # 6 words

# We'll model each word placement with:
# - start_row (0..4)
# - start_col (0..4)
# - direction: 0 = horizontal, 1 = vertical
# For each word, we need to ensure it fits within the grid.

# Decision variables
start_row = [Int(f"start_row_{i}") for i in range(N)]
start_col = [Int(f"start_col_{i}") for i in range(N)]
direction = [Int(f"dir_{i}") for i in range(N)]  # 0 = horizontal, 1 = vertical

# Grid cells: each cell (r,c) gets a letter (0-25 for A-Z, or -1 for empty)
# We'll use Int variables for grid cells
grid = [[Int(f"grid_{r}_{c}") for c in range(GRID_SIZE)] for r in range(GRID_SIZE)]

solver = Solver()

# Domain constraints
for i in range(N):
    solver.add(start_row[i] >= 0, start_row[i] < GRID_SIZE)
    solver.add(start_col[i] >= 0, start_col[i] < GRID_SIZE)
    solver.add(Or(direction[i] == 0, direction[i] == 1))

# Fitting constraints: word must fit within grid
for i in range(N):
    wlen = word_lengths[i]
    # If horizontal: start_col + wlen <= GRID_SIZE
    # If vertical: start_row + wlen <= GRID_SIZE
    solver.add(Implies(direction[i] == 0, start_col[i] + wlen <= GRID_SIZE))
    solver.add(Implies(direction[i] == 1, start_row[i] + wlen <= GRID_SIZE))

# Grid cell domain: 0-25 for A-Z, or -1 for empty
for r in range(GRID_SIZE):
    for c in range(GRID_SIZE):
        solver.add(Or(grid[r][c] == -1, And(grid[r][c] >= 0, grid[r][c] <= 25)))

# Map each word's letters to grid cells
# For each word i, for each position k in the word, the grid cell at that position must equal the letter value
# Letter values: A=0, B=1, ..., Z=25
def letter_val(ch):
    return ord(ch) - ord('A')

for i in range(N):
    w = word_strings[i]
    wlen = word_lengths[i]
    for k in range(wlen):
        ch_val = letter_val(w[k])
        r = start_row[i] + If(direction[i] == 1, k, 0)
        c = start_col[i] + If(direction[i] == 0, k, 0)
        # We need to assert grid[r][c] == ch_val
        # But r and c are symbolic expressions, so we use an Or-loop pattern
        # For each possible (r,c) pair that could be the position of letter k of word i
        # Actually, we can use the fact that r and c are linear expressions of start_row, start_col, direction, k
        # We need to assert: For the actual values of start_row[i], start_col[i], direction[i],
        # the grid cell at that position equals ch_val.
        # Use the approach: for each possible row/col, if the word's letter k lands there, set it.
        # Better: use a Z3 Array or use the approach with constraints.
        
        # Let's use a different approach: we'll create constraints that say:
        # For each cell (r,c), if word i's k-th letter falls on (r,c), then grid[r][c] == ch_val
        # And also, if grid[r][c] is not -1, then some word's letter must be there.
        
        # For each cell (r,c), we can add:
        # Implies(And(direction[i]==0, start_row[i]==r, start_col[i]+k==c), grid[r][c]==ch_val)
        # Implies(And(direction[i]==1, start_col[i]==c, start_row[i]+k==r), grid[r][c]==ch_val)
        
        # But this creates many constraints. Let's do it more efficiently.
        
        # Actually, let's use a simpler approach: iterate over all possible (r,c) cells
        # and add implications.
        pass

# Let's rethink. We'll use a cleaner approach with Z3.

# For each word i and each letter position k, we need to assert that
# the grid cell at (start_row[i] + (dir[i]==1 ? k : 0), start_col[i] + (dir[i]==0 ? k : 0))
# equals the letter value.

# We can do this by iterating over all possible grid cells and adding implications.

for i in range(N):
    w = word_strings[i]
    wlen = word_lengths[i]
    for k in range(wlen):
        ch_val = letter_val(w[k])
        # For each possible cell (r,c) that this letter could occupy
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                # Horizontal case: letter k is at (start_row[i], start_col[i] + k)
                cond_h = And(direction[i] == 0, start_row[i] == r, start_col[i] + k == c)
                # Vertical case: letter k is at (start_row[i] + k, start_col[i])
                cond_v = And(direction[i] == 1, start_col[i] == c, start_row[i] + k == r)
                solver.add(Implies(Or(cond_h, cond_v), grid[r][c] == ch_val))

# Each non-empty cell must be covered by at least one word letter
# For each cell (r,c), if grid[r][c] != -1, then some word's letter must be there
for r in range(GRID_SIZE):
    for c in range(GRID_SIZE):
        covered = False
        conditions = []
        for i in range(N):
            wlen = word_lengths[i]
            for k in range(wlen):
                # Horizontal: word i, letter k at (r,c) if start_row[i]==r and start_col[i]+k==c and dir[i]==0
                cond_h = And(direction[i] == 0, start_row[i] == r, start_col[i] + k == c)
                # Vertical: word i, letter k at (r,c) if start_col[i]==c and start_row[i]+k==r and dir[i]==1
                cond_v = And(direction[i] == 1, start_col[i] == c, start_row[i] + k == r)
                conditions.append(cond_h)
                conditions.append(cond_v)
        solver.add(Implies(grid[r][c] != -1, Or(conditions)))

# Each word must be placed (we already ensure this via the letter constraints above)

# Intersections: words should intersect where possible.
# We don't need to force specific intersections, but we need to ensure
# that when two words cross, the letters match (already handled by grid constraints).

# Let's also add that the grid should be "connected" in some sense, but that's complex.
# For now, let's just try to find any valid placement.

# Also, we need to ensure that each word's letters are placed contiguously
# (already ensured by the constraints above).

# Let's add a constraint that at least some intersections exist (to make it a proper crossword)
# Count intersections: for each pair of words (i,j) with i<j, check if they intersect
# An intersection occurs when for some k1 in word i and k2 in word j:
#   (dir_i==0 and dir_j==1 and start_row_i == start_row_j + k2 and start_col_i + k1 == start_col_j)
#   OR (dir_i==1 and dir_j==0 and start_row_i + k1 == start_row_j and start_col_i == start_col_j + k2)

# Let's count intersections and require at least some
intersection_conditions = []
for i in range(N):
    for j in range(i+1, N):
        for k1 in range(word_lengths[i]):
            for k2 in range(word_lengths[j]):
                # i horizontal, j vertical
                cond1 = And(direction[i]==0, direction[j]==1,
                           start_row[i] == start_row[j] + k2,
                           start_col[i] + k1 == start_col[j])
                # i vertical, j horizontal
                cond2 = And(direction[i]==1, direction[j]==0,
                           start_row[i] + k1 == start_row[j],
                           start_col[i] == start_col[j] + k2)
                intersection_conditions.append(Or(cond1, cond2))

# Require at least 3 intersections (to make it a proper crossword)
solver.add(Sum([If(c, 1, 0) for c in intersection_conditions]) >= 3)

# Also, each word should have at least one intersection with another word
for i in range(N):
    word_intersections = []
    for j in range(N):
        if i == j:
            continue
        for k1 in range(word_lengths[i]):
            for k2 in range(word_lengths[j]):
                cond1 = And(direction[i]==0, direction[j]==1,
                           start_row[i] == start_row[j] + k2,
                           start_col[i] + k1 == start_col[j])
                cond2 = And(direction[i]==1, direction[j]==0,
                           start_row[i] + k1 == start_row[j],
                           start_col[i] == start_col[j] + k2)
                word_intersections.append(Or(cond1, cond2))
    solver.add(Or(word_intersections))  # at least one intersection per word

print("Solving...")
result = solver.check()
print(f"Result: {result}")

if result == sat:
    m = solver.model()
    print("STATUS: sat")
    print()
    
    # Build the grid
    grid_chars = [[' ' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            val = m[grid[r][c]].as_long()
            if val >= 0:
                grid_chars[r][c] = chr(ord('A') + val)
    
    print("Grid:")
    for r in range(GRID_SIZE):
        print(' '.join(grid_chars[r]))
    print()
    
    # Print word placements
    print("Word Placements:")
    for i in range(N):
        sr = m[start_row[i]].as_long()
        sc = m[start_col[i]].as_long()
        d = m[direction[i]].as_long()
        dir_str = "horizontal" if d == 0 else "vertical"
        print(f"  {word_strings[i]}: ({sr}, {sc}) {dir_str}")
    print()
    
    # Find intersections
    print("Intersections:")
    for i in range(N):
        for j in range(i+1, N):
            for k1 in range(word_lengths[i]):
                for k2 in range(word_lengths[j]):
                    # Check if this is an intersection in the model
                    cond1 = And(direction[i]==0, direction[j]==1,
                               start_row[i] == start_row[j] + k2,
                               start_col[i] + k1 == start_col[j])
                    cond2 = And(direction[i]==1, direction[j]==0,
                               start_row[i] + k1 == start_row[j],
                               start_col[i] == start_col[j] + k2)
                    # Evaluate in model
                    val1 = m.eval(cond1)
                    val2 = m.eval(cond2)
                    if str(val1) == "True" or str(val2) == "True":
                        letter = word_strings[i][k1]
                        print(f"  {word_strings[i]}[{k1}] = {word_strings[j]}[{k2}] = '{letter}'")
else:
    print("STATUS: unsat")
    print("No solution found.")