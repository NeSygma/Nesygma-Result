from z3 import *

# BENCHMARK_MODE: ON (model-finding mode)
BENCHMARK_MODE = True

# Create solver
solver = Solver()

# Word list
words = ["CAT", "ACE", "TEA", "EAR", "ATE", "RAT", "CAR", "TAR"]
word_to_id = {word: i for i, word in enumerate(words)}

# Grid size
N = 6

# 1. Declare grid: 0-25 for A-Z, -1 for black/empty
# We'll use Int for each cell
Grid = [[Int(f"grid_{i}_{j}") for j in range(N)] for i in range(N)]

# 2. Black squares at corners
black_positions = [(0,0), (0,5), (5,0), (5,5)]
for (i, j) in black_positions:
    solver.add(Grid[i][j] == -1)  # Mark as black

# 3. Each word is placed exactly once, either horizontal or vertical
# For each word, we need to decide: row, col, direction
# We'll use a tuple for each word: (row, col, direction, used)
# direction: 0=horizontal, 1=vertical
placements = {}
for word in words:
    r = Int(f"row_{word}")
    c = Int(f"col_{word}")
    d = Int(f"dir_{word}")  # 0=horizontal, 1=vertical
    used = Bool(f"used_{word}")
    placements[word] = (r, c, d, used)
    solver.add(Or(d == 0, d == 1))  # direction is either 0 or 1

# Each word must be used exactly once
solver.add(Distinct([placements[word][3] for word in words]))
for word in words:
    solver.add(Implies(placements[word][3], And(
        placements[word][0] >= 0,
        placements[word][0] < N,
        placements[word][1] >= 0,
        placements[word][1] < N,
        placements[word][2] >= 0,
        placements[word][2] < 2
    )))

# 4. Place words on grid
# For each word, if used, place it on the grid
for word in words:
    r, c, d, used = placements[word]
    solver.add(Implies(used, And(
        # Word must fit in grid
        If(d == 0, c + 2 < N, True),  # horizontal: c+2 < N
        If(d == 1, r + 2 < N, True),  # vertical: r+2 < N
        # Starting cell must not be black
        Not(And(r == 0, c == 0)),
        Not(And(r == 0, c == 5)),
        Not(And(r == 5, c == 0)),
        Not(And(r == 5, c == 5)),
        # If horizontal, cells (r,c), (r,c+1), (r,c+2) must not be black
        If(d == 0, And(
            Not(And(r == 0, c == 0)),
            Not(And(r == 0, c + 1 == 0)),
            Not(And(r == 0, c + 2 == 0)),
            Not(And(r == 0, c == 5)),
            Not(And(r == 0, c + 1 == 5)),
            Not(And(r == 0, c + 2 == 5)),
            Not(And(r == 5, c == 0)),
            Not(And(r == 5, c + 1 == 0)),
            Not(And(r == 5, c + 2 == 0)),
            Not(And(r == 5, c == 5)),
            Not(And(r == 5, c + 1 == 5)),
            Not(And(r == 5, c + 2 == 5))
        ), True),
        # If vertical, cells (r,c), (r+1,c), (r+2,c) must not be black
        If(d == 1, And(
            Not(And(r == 0, c == 0)),
            Not(And(r + 1 == 0, c == 0)),
            Not(And(r + 2 == 0, c == 0)),
            Not(And(r == 0, c == 5)),
            Not(And(r + 1 == 0, c == 5)),
            Not(And(r + 2 == 0, c == 5)),
            Not(And(r == 5, c == 0)),
            Not(And(r + 1 == 5, c == 0)),
            Not(And(r + 2 == 5, c == 0)),
            Not(And(r == 5, c == 5)),
            Not(And(r + 1 == 5, c == 5)),
            Not(And(r + 2 == 5, c == 5))
        ), True)
    )))

# 5. Place letters on grid for each word
letter_to_val = {chr(ord('A') + i): i for i in range(26)}
for word in words:
    r, c, d, used = placements[word]
    for idx, letter in enumerate(word):
        if d == 0:  # horizontal
            solver.add(Implies(used, Grid[r][c + idx] == letter_to_val[letter]))
        else:  # vertical
            solver.add(Implies(used, Grid[r + idx][c] == letter_to_val[letter]))

# 6. No conflicts: same cell cannot have different letters
# We need to ensure that if two words write to the same cell, they write the same letter
# We'll collect all constraints for each cell
for i in range(N):
    for j in range(N):
        if (i, j) in black_positions:
            solver.add(Grid[i][j] == -1)
            continue  # black squares already handled
        # Collect all words that could write to (i,j)
        # For horizontal words: row=i, col<=j<=col+2
        # For vertical words: col=j, row<=i<=row+2
        constraints = []
        for word in words:
            r, c, d, used = placements[word]
            if d == 0:  # horizontal
                if i == r and c <= j <= c + 2:
                    letter_idx = j - c
                    letter_val = letter_to_val[word[letter_idx]]
                    constraints.append(If(used, Grid[i][j] == letter_val, True))
            else:  # vertical
                if j == c and r <= i <= r + 2:
                    letter_idx = i - r
                    letter_val = letter_to_val[word[letter_idx]]
                    constraints.append(If(used, Grid[i][j] == letter_val, True))
        # If any word writes to this cell, the cell must equal that letter
        # If multiple words write to this cell, they must agree
        if constraints:
            solver.add(Or([placements[word][3] for word in words if (placements[word][0] == i and placements[word][2] == 0 and placements[word][1] <= j <= placements[word][1] + 2) or (placements[word][1] == j and placements[word][2] == 1 and placements[word][0] <= i <= placements[word][0] + 2)]))
            solver.add(Grid[i][j] >= 0)  # Must be a letter, not black or empty

# 7. At least 3 intersection points
# An intersection is a cell where a horizontal word and a vertical word cross
# We need to count such cells
intersection_count = Int("intersection_count")
solver.add(intersection_count >= 3)

# To count intersections, we need to track which cells are intersections
is_intersection = [[Bool(f"is_intersection_{i}_{j}") for j in range(N)] for i in range(N)]

# A cell is an intersection if:
# - It is written by a horizontal word AND a vertical word
# - The letters match (already ensured by no-conflict)
for i in range(N):
    for j in range(N):
        if (i, j) in black_positions:
            continue
        # Check if any horizontal word writes to (i,j)
        horiz_writes = []
        for word in words:
            r, c, d, used = placements[word]
            if d == 0 and r == i and c <= j <= c + 2:
                horiz_writes.append(used)
        # Check if any vertical word writes to (i,j)
        vert_writes = []
        for word in words:
            r, c, d, used = placements[word]
            if d == 1 and c == j and r <= i <= r + 2:
                vert_writes.append(used)
        # Cell is intersection if at least one horizontal AND one vertical word write to it
        if horiz_writes and vert_writes:
            solver.add(is_intersection[i][j] == And(Or(horiz_writes), Or(vert_writes)))
        else:
            solver.add(Not(is_intersection[i][j]))

# Count intersections
solver.add(intersection_count == Sum([If(is_intersection[i][j], 1, 0) for i in range(N) for j in range(N)]))

# 8. Connectivity: All placed letters must form a single connected component
# We'll use a graph where nodes are cells with letters, and edges are adjacent cells
# We need to ensure there's exactly one connected component with all letter cells

# First, collect all cells that have letters (not black, not empty)
letter_cells = []
for i in range(N):
    for j in range(N):
        if (i, j) not in black_positions:
            # Cell has a letter if it's written by any word
            has_letter = Bool(f"has_letter_{i}_{j}")
            constraints = []
            for word in words:
                r, c, d, used = placements[word]
                if d == 0:  # horizontal
                    if i == r and c <= j <= c + 2:
                        constraints.append(used)
                else:  # vertical
                    if j == c and r <= i <= r + 2:
                        constraints.append(used)
            solver.add(has_letter == Or(constraints))
            letter_cells.append((i, j, has_letter))

# Now, we need to ensure connectivity
# We'll use a union-find or BFS approach in Z3
# For simplicity, we'll use a spanning tree constraint
# We need to select a set of edges (adjacent letter cells) that connect all letter cells

# Collect all adjacent pairs of letter cells
adjacent_pairs = []
for i in range(N):
    for j in range(N):
        if (i, j) not in black_positions:
            # Check right neighbor
            if j + 1 < N and (i, j + 1) not in black_positions:
                adjacent_pairs.append(((i, j), (i, j + 1)))
            # Check down neighbor
            if i + 1 < N and (i + 1, j) not in black_positions:
                adjacent_pairs.append(((i, j), (i + 1, j)))

# For each adjacent pair, decide if they are connected
connected = {}
for (cell1, cell2) in adjacent_pairs:
    conn = Bool(f"conn_{cell1[0]}_{cell1[1]}_{cell2[0]}_{cell2[1]}")
    connected[(cell1, cell2)] = conn

# If both cells have letters, they can be connected
for (cell1, cell2) in adjacent_pairs:
    i1, j1 = cell1
    i2, j2 = cell2
    has_letter1 = Bool(f"has_letter_{i1}_{j1}")
    has_letter2 = Bool(f"has_letter_{i2}_{j2}")
    solver.add(Implies(And(has_letter1, has_letter2), 
                       connected[(cell1, cell2)] == True))
    solver.add(Implies(Or(Not(has_letter1), Not(has_letter2)), 
                       connected[(cell1, cell2)] == False))

# Now, we need to ensure that the graph is connected
# We'll use a spanning tree constraint: exactly (num_letter_cells - 1) edges in the spanning tree
# But Z3 doesn't have a direct spanning tree constraint, so we'll use a simpler approach:
# Ensure that for every partition of letter cells into two non-empty sets, there is at least one edge connecting them
# This is complex, so we'll use a simpler heuristic: ensure that all letter cells are reachable from one root

# For simplicity, we'll pick the first letter cell as root and ensure all others are reachable
if letter_cells:
    root_i, root_j, root_has_letter = letter_cells[0]
    # We need to ensure that all letter cells are reachable from (root_i, root_j)
    # We'll use a BFS-like constraint
    # For each letter cell, there must be a path to the root
    # This is complex to encode directly, so we'll use a simpler constraint:
    # The number of connected components is 1
    # We'll use a union-find approach with Z3
    parent = {}
    for (i, j, has_letter) in letter_cells:
        parent[(i, j)] = Int(f"parent_{i}_{j}")
        solver.add(parent[(i, j)] >= 0)
        solver.add(parent[(i, j)] < N * N)
    
    # Each cell is its own parent initially
    for (i, j, has_letter) in letter_cells:
        solver.add(Implies(has_letter, parent[(i, j)] == (i * N + j)))
    
    # For each connected edge, union the sets
    for ((i1, j1), (i2, j2)) in adjacent_pairs:
        has_letter1 = Bool(f"has_letter_{i1}_{j1}")
        has_letter2 = Bool(f"has_letter_{i2}_{j2}")
        conn = connected[((i1, j1), (i2, j2))]
        solver.add(Implies(And(has_letter1, has_letter2, conn), 
                           parent[(i1, j1)] == parent[(i2, j2)]))
    
    # All letter cells must have the same parent as the root
    for (i, j, has_letter) in letter_cells:
        solver.add(Implies(has_letter, parent[(i, j)] == parent[(root_i, root_j)]))

# Check if the problem is satisfiable
result = solver.check()

if result == sat:
    model = solver.model()
    print("STATUS: sat")
    print("A valid crossword placement exists!")
    
    # Print grid
    print("\nGrid:")
    for i in range(N):
        row_str = ""
        for j in range(N):
            if (i, j) in black_positions:
                row_str += "# "
            else:
                val = model[Grid[i][j]]
                if val is None:
                    row_str += ". "
                else:
                    if val.as_long() == -1:
                        row_str += "# "
                    else:
                        letter = chr(ord('A') + val.as_long())
                        row_str += letter + " "
        print(row_str)
    
    # Print placements
    print("\nPlacements:")
    for word in words:
        r, c, d, used = placements[word]
        if model[used]:
            direction = "horizontal" if model[d].as_long() == 0 else "vertical"
            start_r = model[r].as_long()
            start_c = model[c].as_long()
            placed_word = word
            print(f"{word}: ({start_r}, {start_c}) {direction}")
    
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")