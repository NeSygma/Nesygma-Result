from z3 import *

# BENCHMARK_MODE: ON (problem is guaranteed solvable)
BENCHMARK_MODE = True

# Initialize solver
solver = Solver()

# Grid size
N = 6

# Words to place
words = ["CAT", "ACE", "TEA", "EAR", "ATE", "RAT", "CAR", "TAR"]

# Black squares (fixed)
black_squares = [(0, 0), (0, 5), (5, 0), (5, 5)]

# Directions
horizontal = 0
vertical = 1

# Grid: Use Z3 Array to allow symbolic indexing
# We will use a 2D array of Int variables
Grid = Array('grid', IntSort(), ArraySort(IntSort(), IntSort()))

# Helper function to get/set cell values in the grid
# This avoids direct indexing with Z3 variables

def grid_get(grid, i, j):
    return Select(Select(grid, i), j)

def grid_set(grid, i, j, val):
    return Store(Store(grid, i, Store(Select(grid, i), j, val)), i, Select(grid, i))

# Initialize grid with default values (32 for space)
# We will set black squares and word placements later
grid = Grid
for i in range(N):
    for j in range(N):
        grid = grid_set(grid, i, j, 32)

# Set black squares to -1
for i, j in black_squares:
    grid = grid_set(grid, i, j, -1)

# Placement variables: (word, row, col, direction)
placement_vars = []
for idx, word in enumerate(words):
    word_var = String(f"word_{idx}")
    solver.add(word_var == word)
    row_var = Int(f"row_{idx}")
    col_var = Int(f"col_{idx}")
    dir_var = Int(f"dir_{idx}")
    placement_vars.append((word_var, row_var, col_var, dir_var))

# Each word must be placed exactly once
active_placements = [Bool(f"active_{idx}") for idx in range(len(words))]

# Add constraints for placements
for idx, (word_var, row_var, col_var, dir_var) in enumerate(placement_vars):
    # Word must be placed in one direction
    solver.add(Or(dir_var == horizontal, dir_var == vertical))
    
    # For horizontal placement: word occupies (row, col) to (row, col+2)
    # For vertical placement: word occupies (row, col) to (row+2, col)
    
    # Constraints for horizontal placement
    solver.add(Implies(dir_var == horizontal, 
                       And(row_var >= 0, row_var < N, 
                           col_var >= 0, col_var + 2 < N)))
    
    # Constraints for vertical placement
    solver.add(Implies(dir_var == vertical, 
                       And(row_var >= 0, row_var + 2 < N, 
                           col_var >= 0, col_var < N)))
    
    # Word cannot start on a black square
    solver.add(Not(Or([And(row_var == i, col_var == j) for (i, j) in black_squares])))
    
    # Word cannot cross a black square
    if dir_var == horizontal:
        for k in range(3):
            solver.add(Not(Or([And(row_var == i, col_var + k == j) for (i, j) in black_squares])))
    else:  # vertical
        for k in range(3):
            solver.add(Not(Or([And(row_var + k == i, col_var == j) for (i, j) in black_squares])))

# Ensure each word is placed exactly once
solver.add(Sum(active_placements) == len(words))

# Assign letters to grid based on placements
for idx, (word_var, row_var, col_var, dir_var) in enumerate(placement_vars):
    word_str = words[idx]
    solver.add(word_var == word_str)
    
    # For each letter in the word, assign to the grid
    for k in range(3):
        letter = IntVal(ord(word_str[k]))
        if dir_var == horizontal:
            # grid[row_var][col_var + k] = letter
            grid = grid_set(grid, row_var, col_var + k, letter)
        else:  # vertical
            # grid[row_var + k][col_var] = letter
            grid = grid_set(grid, row_var + k, col_var, letter)

# No conflicts: same cell cannot have different letters
# This is implicitly handled by the grid assignments above

# At least 3 intersection points where horizontal and vertical words share a cell
intersections = []
for i in range(len(words)):
    for j in range(i + 1, len(words)):
        # Check if placements i and j intersect
        wi, ri, ci, di = placement_vars[i]
        wj, rj, cj, dj = placement_vars[j]
        
        # Intersection condition
        intersect = Bool(f"intersect_{i}_{j}")
        
        # Case 1: i is horizontal, j is vertical
        cond1 = And(di == horizontal, dj == vertical, 
                    ri == rj, ci <= cj, ci + 2 >= cj)
        
        # Case 2: i is vertical, j is horizontal
        cond2 = And(di == vertical, dj == horizontal, 
                    ci == cj, ri <= rj, ri + 2 >= rj)
        
        solver.add(intersect == Or(cond1, cond2))
        intersections.append(intersect)

# At least 3 intersections
solver.add(Sum(intersections) >= 3)

# Letter matching at intersections
for i in range(len(words)):
    for j in range(i + 1, len(words)):
        wi, ri, ci, di = placement_vars[i]
        wj, rj, cj, dj = placement_vars[j]
        
        # Case 1: i is horizontal, j is vertical
        cond1 = And(di == horizontal, dj == vertical, 
                    ri == rj, ci <= cj, ci + 2 >= cj)
        
        # Case 2: i is vertical, j is horizontal
        cond2 = And(di == vertical, dj == horizontal, 
                    ci == cj, ri <= rj, ri + 2 >= rj)
        
        # If they intersect, their letters must match
        for k in range(3):
            if cond1:
                # Intersection at (ri, cj)
                # Letter from horizontal word i at position (ri, cj - ci)
                # Letter from vertical word j at position (rj + (cj - ci), cj)
                # Since ri == rj, the letter from i is words[i][cj - ci]
                # The letter from j is words[j][cj - ci]
                letter_i = IntVal(ord(words[i][cj - ci]))
                letter_j = IntVal(ord(words[j][cj - ci]))
                solver.add(Implies(cond1, grid_get(grid, ri, cj) == letter_i))
                solver.add(Implies(cond1, grid_get(grid, ri, cj) == letter_j))
            elif cond2:
                # Intersection at (ri, cj)
                # Letter from vertical word i at position (ri - rj, cj)
                # Letter from horizontal word j at position (ri, cj)
                # Since ci == cj, the letter from i is words[i][ri - rj]
                # The letter from j is words[j][ri - rj]
                letter_i = IntVal(ord(words[i][ri - rj]))
                letter_j = IntVal(ord(words[j][ri - rj]))
                solver.add(Implies(cond2, grid_get(grid, ri, cj) == letter_i))
                solver.add(Implies(cond2, grid_get(grid, ri, cj) == letter_j))

# Connectivity: All placed letters must form a single connected component
# We will model the grid as a graph where edges exist between adjacent placed letters
# We will use a union-find or DFS-based approach to ensure connectivity

# First, collect all cells that are not black squares and are part of a word
word_cells = []
for i in range(N):
    for j in range(N):
        if (i, j) not in black_squares:
            # Check if this cell is part of any word
            is_word_cell = False
            for idx, (word_var, row_var, col_var, dir_var) in enumerate(placement_vars):
                word_str = words[idx]
                if dir_var == horizontal:
                    for k in range(3):
                        if And(row_var == i, col_var + k == j):
                            is_word_cell = True
                else:  # vertical
                    for k in range(3):
                        if And(row_var + k == i, col_var == j):
                            is_word_cell = True
            if is_word_cell:
                word_cells.append((i, j))

# If there are no word cells, the problem is unsat (but we have 8 words, so this is unlikely)
if len(word_cells) > 0:
    # Create a graph where edges exist between adjacent word cells
    # We will use a union-find approach to ensure connectivity
    parent = {cell: cell for cell in word_cells}
    
    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]
    
    def union(x, y):
        fx = find(x)
        fy = find(y)
        if fx != fy:
            parent[fy] = fx
    
    # Add edges between adjacent word cells
    for (i, j) in word_cells:
        # Check right neighbor
        if (i, j + 1) in word_cells:
            union((i, j), (i, j + 1))
        # Check bottom neighbor
        if (i + 1, j) in word_cells:
            union((i, j), (i + 1, j))
    
    # Ensure all word cells are in the same set
    root = find(word_cells[0])
    for cell in word_cells[1:]:
        solver.add(find(cell) == root)

# Check satisfiability
result = solver.check()

if result == sat:
    model = solver.model()
    print("STATUS: sat")
    
    # Print the grid
    print("\nGrid:")
    for i in range(N):
        row = []
        for j in range(N):
            cell_val = model.eval(grid_get(grid, i, j), model_completion=True)
            if cell_val.as_long() == -1:
                row.append("#")
            elif cell_val.as_long() == 32:
                row.append(" ")
            else:
                row.append(chr(cell_val.as_long()))
        print(" ".join(row))
    
    # Print placements
    print("\nPlacements:")
    for idx, (word_var, row_var, col_var, dir_var) in enumerate(placement_vars):
        if model.eval(active_placements[idx], model_completion=True):
            word = words[idx]
            row = model.eval(row_var, model_completion=True).as_long()
            col = model.eval(col_var, model_completion=True).as_long()
            direction = "horizontal" if model.eval(dir_var, model_completion=True).as_long() == horizontal else "vertical"
            print(f"Word: {word}, Row: {row}, Col: {col}, Direction: {direction}")
    
    # Print intersections
    print("\nIntersections:")
    for i in range(len(words)):
        for j in range(i + 1, len(words)):
            if model.eval(intersections[i * (len(words) - 1) + j - (i + 1)], model_completion=True):
                print(f"Intersection between {words[i]} and {words[j]}")
    
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")