from z3 import *

# Problem data
words = ["CAT", "ACE", "TEA", "EAR", "ATE", "RAT", "CAR", "TAR"]
black_squares = [(0,0), (0,5), (5,0), (5,5)]
grid_size = 6

# Create solver
solver = Solver()

# For each word, create placement variables
# word_placement[word_index] = (direction, start_row, start_col)
# direction: 0 = horizontal, 1 = vertical
word_dir = [Int(f"dir_{i}") for i in range(8)]
word_row = [Int(f"row_{i}") for i in range(8)]
word_col = [Int(f"col_{i}") for i in range(8)]

# Grid representation: 6x6 array of letters (Int values 0-25 for A-Z, -1 for empty, -2 for black)
grid = [[Int(f"cell_{r}_{c}") for c in range(grid_size)] for r in range(grid_size)]

# Initialize black squares
for r, c in black_squares:
    solver.add(grid[r][c] == -2)  # -2 represents black square

# Initialize other cells as empty
for r in range(grid_size):
    for c in range(grid_size):
        if (r, c) not in black_squares:
            solver.add(grid[r][c] >= -1)  # -1 or letter value
            solver.add(grid[r][c] <= 25)  # A-Z

# Word placement constraints
for i, word in enumerate(words):
    # Direction: 0 = horizontal, 1 = vertical
    solver.add(Or(word_dir[i] == 0, word_dir[i] == 1))
    
    # Starting position constraints based on direction
    solver.add(If(word_dir[i] == 0, 
                  And(word_row[i] >= 0, word_row[i] < grid_size,
                      word_col[i] >= 0, word_col[i] <= grid_size - 3),  # horizontal: col <= 3
                  And(word_row[i] >= 0, word_row[i] <= grid_size - 3,  # vertical: row <= 3
                      word_col[i] >= 0, word_col[i] < grid_size)))
    
    # Cannot start on black squares
    for br, bc in black_squares:
        solver.add(Or(word_row[i] != br, word_col[i] != bc))
    
    # Place each letter of the word
    for j, letter in enumerate(word):
        letter_val = ord(letter) - ord('A')
        solver.add(If(word_dir[i] == 0,  # horizontal
                      grid[word_row[i]][word_col[i] + j] == letter_val,
                      grid[word_row[i] + j][word_col[i]] == letter_val))
    
    # Ensure word doesn't cross black squares (except at start which we already checked)
    for j in range(1, 3):  # check positions 1 and 2
        solver.add(If(word_dir[i] == 0,  # horizontal
                      Or(word_col[i] + j >= grid_size, 
                         And(word_col[i] + j < grid_size, 
                             grid[word_row[i]][word_col[i] + j] != -2)),
                      Or(word_row[i] + j >= grid_size,
                         And(word_row[i] + j < grid_size,
                             grid[word_row[i] + j][word_col[i]] != -2))))

# Ensure each word is placed exactly once (no two words occupy same starting position)
for i in range(8):
    for j in range(i+1, 8):
        # Different starting positions or different directions
        solver.add(Or(word_row[i] != word_row[j],
                      word_col[i] != word_col[j],
                      word_dir[i] != word_dir[j]))

# Count intersections (at least 3)
# An intersection occurs when a horizontal word and vertical word share a cell
intersection_count = Int("intersection_count")
solver.add(intersection_count >= 3)

# Calculate intersections
intersection_vars = []
for i in range(8):
    for j in range(8):
        if i != j:
            # Check if word i (horizontal) and word j (vertical) intersect
            # For horizontal word i and vertical word j
            # They intersect if: row_i == row_j + k and col_i + l == col_j
            # where k is position in vertical word, l is position in horizontal word
            intersect = Bool(f"intersect_{i}_{j}")
            
            # Check all possible intersection points
            possible_intersections = []
            for pos_h in range(3):  # position in horizontal word
                for pos_v in range(3):  # position in vertical word
                    # Horizontal word i at (row_i, col_i + pos_h)
                    # Vertical word j at (row_j + pos_v, col_j)
                    # They intersect if these coordinates are the same
                    same_cell = And(
                        word_row[i] == word_row[j] + pos_v,
                        word_col[i] + pos_h == word_col[j]
                    )
                    # And they must be in different directions
                    different_dirs = And(word_dir[i] == 0, word_dir[j] == 1)
                    possible_intersections.append(And(same_cell, different_dirs))
            
            if possible_intersections:
                solver.add(intersect == Or(possible_intersections))
                intersection_vars.append(intersect)

# Sum of intersections
if intersection_vars:
    solver.add(Sum([If(iv, 1, 0) for iv in intersection_vars]) >= 3)

# Connectivity constraint: all placed letters must form a single connected component
# We'll use a simpler approach: ensure there's a path between any two placed letters
# For simplicity, we'll check that the number of connected components is 1

# Create a connectivity graph using BFS-like constraints
# For each cell, we'll track which component it belongs to
component = [[Int(f"comp_{r}_{c}") for c in range(grid_size)] for r in range(grid_size)]

# Initialize component numbers
for r in range(grid_size):
    for c in range(grid_size):
        solver.add(component[r][c] >= 0)
        solver.add(component[r][c] < grid_size * grid_size)

# Adjacent cells (up, down, left, right) must have same component if both are filled
for r in range(grid_size):
    for c in range(grid_size):
        if (r, c) not in black_squares:
            # Check right neighbor
            if c + 1 < grid_size and (r, c+1) not in black_squares:
                solver.add(Implies(
                    And(grid[r][c] >= 0, grid[r][c+1] >= 0),
                    component[r][c] == component[r][c+1]
                ))
            # Check down neighbor
            if r + 1 < grid_size and (r+1, c) not in black_squares:
                solver.add(Implies(
                    And(grid[r][c] >= 0, grid[r+1][c] >= 0),
                    component[r][c] == component[r+1][c]
                ))

# All filled cells must have the same component number
filled_cells = []
for r in range(grid_size):
    for c in range(grid_size):
        if (r, c) not in black_squares:
            filled_cells.append((r, c))

if filled_cells:
    first_r, first_c = filled_cells[0]
    for r, c in filled_cells[1:]:
        solver.add(Implies(
            And(grid[first_r][first_c] >= 0, grid[r][c] >= 0),
            component[first_r][first_c] == component[r][c]
        ))

# Check for solution
print("Checking for crossword puzzle solution...")
result = solver.check()

if result == sat:
    print("STATUS: sat")
    m = solver.model()
    
    # Print grid
    print("\nGrid:")
    for r in range(grid_size):
        row_str = ""
        for c in range(grid_size):
            cell_val = m.eval(grid[r][c])
            if cell_val.as_long() == -2:
                row_str += "# "
            elif cell_val.as_long() == -1:
                row_str += ". "
            else:
                row_str += chr(ord('A') + cell_val.as_long()) + " "
        print(row_str)
    
    # Print placements
    print("\nPlacements:")
    for i, word in enumerate(words):
        dir_str = "horizontal" if m.eval(word_dir[i]).as_long() == 0 else "vertical"
        row = m.eval(word_row[i]).as_long()
        col = m.eval(word_col[i]).as_long()
        print(f"{word}: {dir_str} at ({row}, {col})")
    
    # Count intersections
    if intersection_vars:
        intersection_count_val = sum(1 for iv in intersection_vars if m.eval(iv).as_long() == 1)
        print(f"\nIntersections: {intersection_count_val}")
    
elif result == unsat:
    print("STATUS: unsat")
    print("No solution found - constraints are unsatisfiable")
else:
    print("STATUS: unknown")
    print("Solver returned unknown result")