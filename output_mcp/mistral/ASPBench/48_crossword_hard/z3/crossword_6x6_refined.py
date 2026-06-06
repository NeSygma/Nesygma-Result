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

# 1. Declare grid as a Z3 Array to allow symbolic access
# We'll use IntSort() for cells: -1=black, 0-25=A-Z, -2=empty
Grid = Array('grid', IntSort(), IntSort())

# 2. Black squares at corners
black_positions = [(0,0), (0,5), (5,0), (5,5)]
for (i, j) in black_positions:
    solver.add(Select(Grid, i * N + j) == -1)  # Mark as black

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

# 4. Place words on grid
# For each word, if used, place it on the grid
letter_to_val = {chr(ord('A') + i): i for i in range(26)}
for word in words:
    r, c, d, used = placements[word]
    for idx, letter in enumerate(word):
        if d == 0:  # horizontal
            solver.add(Implies(used, And(
                c + idx < N,  # Must fit in grid
                Select(Grid, r * N + (c + idx)) == letter_to_val[letter]
            )))
        else:  # vertical
            solver.add(Implies(used, And(
                r + idx < N,  # Must fit in grid
                Select(Grid, (r + idx) * N + c) == letter_to_val[letter]
            )))

# 5. No conflicts: same cell cannot have different letters
# We need to ensure that if two words write to the same cell, they write the same letter
# We'll collect all constraints for each cell
for i in range(N):
    for j in range(N):
        cell_index = i * N + j
        if (i, j) in black_positions:
            continue  # black squares already handled
        # Collect all words that could write to (i,j)
        # For horizontal words: row=i, col<=j<=col+2
        # For vertical words: col=j, row<=i<=row+2
        constraints = []
        for word in words:
            r, c, d, used = placements[word]
            if d == 0:  # horizontal
                if i == r and c <= j < c + len(word):  # Ensure word fits
                    letter_idx = j - c
                    letter_val = letter_to_val[word[letter_idx]]
                    constraints.append(If(used, Select(Grid, cell_index) == letter_val, True))
            else:  # vertical
                if j == c and r <= i < r + len(word):  # Ensure word fits
                    letter_idx = i - r
                    letter_val = letter_to_val[word[letter_idx]]
                    constraints.append(If(used, Select(Grid, cell_index) == letter_val, True))
        # If any word writes to this cell, the cell must equal that letter
        if constraints:
            solver.add(Or([placements[word][3] for word in words if (placements[word][0] == i and placements[word][2] == 0 and placements[word][1] <= j < placements[word][1] + len(word)) or (placements[word][1] == j and placements[word][2] == 1 and placements[word][0] <= i < placements[word][0] + len(word))]))
            solver.add(Select(Grid, cell_index) >= 0)  # Must be a letter, not black or empty

# 6. At least 3 intersection points
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
        cell_index = i * N + j
        if (i, j) in black_positions:
            continue
        # Check if any horizontal word writes to (i,j)
        horiz_writes = []
        for word in words:
            r, c, d, used = placements[word]
            if d == 0 and r == i and c <= j < c + len(word):
                horiz_writes.append(used)
        # Check if any vertical word writes to (i,j)
        vert_writes = []
        for word in words:
            r, c, d, used = placements[word]
            if d == 1 and c == j and r <= i < r + len(word):
                vert_writes.append(used)
        # Cell is intersection if at least one horizontal AND one vertical word write to it
        if horiz_writes and vert_writes:
            solver.add(is_intersection[i][j] == And(Or(horiz_writes), Or(vert_writes)))
        else:
            solver.add(Not(is_intersection[i][j]))

# Count intersections
solver.add(intersection_count == Sum([If(is_intersection[i][j], 1, 0) for i in range(N) for j in range(N)]))

# 7. Connectivity: All placed letters must form a single connected component
# We'll use a graph where nodes are cells with letters, and edges are adjacent cells
# We need to ensure there's exactly one connected component with all letter cells

# First, collect all cells that have letters (not black, not empty)
has_letter = [[Bool(f"has_letter_{i}_{j}") for j in range(N)] for i in range(N)]
for i in range(N):
    for j in range(N):
        if (i, j) in black_positions:
            solver.add(Not(has_letter[i][j]))
        else:
            # Cell has a letter if it's written by any word
            constraints = []
            for word in words:
                r, c, d, used = placements[word]
                if d == 0:  # horizontal
                    if i == r and c <= j < c + len(word):
                        constraints.append(used)
                else:  # vertical
                    if j == c and r <= i < r + len(word):
                        constraints.append(used)
            solver.add(has_letter[i][j] == Or(constraints))

# Now, we need to ensure connectivity
# We'll use a union-find approach with Z3
# For each letter cell, assign a component id
comp_id = [[Int(f"comp_id_{i}_{j}") for j in range(N)] for i in range(N)]

# Initially, each cell is its own component
for i in range(N):
    for j in range(N):
        solver.add(Implies(has_letter[i][j], comp_id[i][j] >= 0))
        solver.add(Implies(has_letter[i][j], comp_id[i][j] < N * N))

# For each adjacent pair of letter cells, if they are connected, they must have the same component id
for i in range(N):
    for j in range(N):
        if has_letter[i][j]:
            # Check right neighbor
            if j + 1 < N and has_letter[i][j+1]:
                solver.add(Implies(And(has_letter[i][j], has_letter[i][j+1]), 
                                   comp_id[i][j] == comp_id[i][j+1]))
            # Check down neighbor
            if i + 1 < N and has_letter[i+1][j]:
                solver.add(Implies(And(has_letter[i][j], has_letter[i+1][j]), 
                                   comp_id[i][j] == comp_id[i+1][j]))

# Ensure all letter cells have the same component id (single connected component)
letter_cells = [(i, j) for i in range(N) for j in range(N) if (i, j) not in black_positions]
if letter_cells:
    root_comp = comp_id[letter_cells[0][0]][letter_cells[0][1]]
    for (i, j) in letter_cells[1:]:
        solver.add(comp_id[i][j] == root_comp)

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
            cell_index = i * N + j
            val = model.eval(Select(Grid, cell_index), model_completion=True)
            if val.as_long() == -1:
                row_str += "# "
            elif val.as_long() >= 0 and val.as_long() < 26:
                letter = chr(ord('A') + val.as_long())
                row_str += letter + " "
            else:
                row_str += ". "
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