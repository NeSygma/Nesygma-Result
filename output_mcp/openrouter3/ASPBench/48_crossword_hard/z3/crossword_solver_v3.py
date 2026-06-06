from z3 import *

# Problem data
words = ["CAT", "ACE", "TEA", "EAR", "ATE", "RAT", "CAR", "TAR"]
black_squares = [(0,0), (0,5), (5,0), (5,5)]
grid_size = 6

# Create solver
solver = Solver()

# For each word, create placement variables
word_dir = [Int(f"dir_{i}") for i in range(8)]
word_row = [Int(f"row_{i}") for i in range(8)]
word_col = [Int(f"col_{i}") for i in range(8)]

# Grid representation using Z3 Array
# Array from (row, col) to letter value (-2 for black, -1 for empty, 0-25 for A-Z)
grid = Array('grid', IntSort(), IntSort())

# Initialize black squares
for r, c in black_squares:
    solver.add(grid[r * grid_size + c] == -2)

# Initialize other cells as empty
for r in range(grid_size):
    for c in range(grid_size):
        if (r, c) not in black_squares:
            solver.add(grid[r * grid_size + c] >= -1)
            solver.add(grid[r * grid_size + c] <= 25)

# Word placement constraints
for i, word in enumerate(words):
    # Direction: 0 = horizontal, 1 = vertical
    solver.add(Or(word_dir[i] == 0, word_dir[i] == 1))
    
    # Starting position constraints based on direction
    solver.add(If(word_dir[i] == 0, 
                  And(word_row[i] >= 0, word_row[i] < grid_size,
                      word_col[i] >= 0, word_col[i] <= grid_size - 3),
                  And(word_row[i] >= 0, word_row[i] <= grid_size - 3,
                      word_col[i] >= 0, word_col[i] < grid_size)))
    
    # Cannot start on black squares
    for br, bc in black_squares:
        solver.add(Or(word_row[i] != br, word_col[i] != bc))
    
    # Place each letter of the word
    for j, letter in enumerate(word):
        letter_val = ord(letter) - ord('A')
        # Use If to select the correct cell based on direction
        cell_index = If(word_dir[i] == 0,
                        word_row[i] * grid_size + (word_col[i] + j),
                        (word_row[i] + j) * grid_size + word_col[i])
        solver.add(grid[cell_index] == letter_val)
    
    # Ensure word doesn't cross black squares (except at start which we already checked)
    for j in range(1, 3):  # check positions 1 and 2
        cell_index = If(word_dir[i] == 0,
                        word_row[i] * grid_size + (word_col[i] + j),
                        (word_row[i] + j) * grid_size + word_col[i])
        solver.add(grid[cell_index] != -2)

# Ensure each word is placed exactly once (no two words occupy same starting position)
for i in range(8):
    for j in range(i+1, 8):
        # Different starting positions or different directions
        solver.add(Or(word_row[i] != word_row[j],
                      word_col[i] != word_col[j],
                      word_dir[i] != word_dir[j]))

# Count intersections (at least 3)
# An intersection occurs when a horizontal word and vertical word share a cell
intersection_vars = []
for i in range(8):
    for j in range(8):
        if i != j:
            # Check if word i (horizontal) and word j (vertical) intersect
            intersect = Bool(f"intersect_{i}_{j}")
            
            # Check all possible intersection points
            possible_intersections = []
            for pos_h in range(3):  # position in horizontal word
                for pos_v in range(3):  # position in vertical word
                    # They intersect if: row_i == row_j + pos_v and col_i + pos_h == col_j
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
component = Array('component', IntSort(), IntSort())

# Initialize component numbers
for r in range(grid_size):
    for c in range(grid_size):
        idx = r * grid_size + c
        solver.add(component[idx] >= 0)
        solver.add(component[idx] < grid_size * grid_size)

# Adjacent cells (up, down, left, right) must have same component if both are filled
for r in range(grid_size):
    for c in range(grid_size):
        idx = r * grid_size + c
        # Check right neighbor
        if c + 1 < grid_size:
            idx_right = r * grid_size + (c + 1)
            solver.add(Implies(
                And(grid[idx] >= 0, grid[idx_right] >= 0),
                component[idx] == component[idx_right]
            ))
        # Check down neighbor
        if r + 1 < grid_size:
            idx_down = (r + 1) * grid_size + c
            solver.add(Implies(
                And(grid[idx] >= 0, grid[idx_down] >= 0),
                component[idx] == component[idx_down]
            ))

# All filled cells must have the same component number
filled_indices = []
for r in range(grid_size):
    for c in range(grid_size):
        if (r, c) not in black_squares:
            filled_indices.append(r * grid_size + c)

if filled_indices:
    first_idx = filled_indices[0]
    for idx in filled_indices[1:]:
        solver.add(Implies(
            And(grid[first_idx] >= 0, grid[idx] >= 0),
            component[first_idx] == component[idx]
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
            idx = r * grid_size + c
            cell_val = m.eval(grid[idx])
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
        intersection_count_val = 0
        for iv in intersection_vars:
            # Evaluate the boolean variable
            val = m.eval(iv)
            if is_true(val):
                intersection_count_val += 1
        print(f"\nIntersections: {intersection_count_val}")
    
elif result == unsat:
    print("STATUS: unsat")
    print("No solution found - constraints are unsatisfiable")
else:
    print("STATUS: unknown")
    print("Solver returned unknown result")