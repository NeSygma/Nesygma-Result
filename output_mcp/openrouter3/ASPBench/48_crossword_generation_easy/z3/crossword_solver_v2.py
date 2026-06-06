from z3 import *

# Problem parameters
GRID_SIZE = 5
WORDS = [
    ("CODE", "Programming instructions"),
    ("DATA", "Information"),
    ("TECH", "Technology short"),
    ("CHIP", "Computer component"),
    ("BYTE", "Data unit"),
    ("NET", "Internet short")
]

# Create solver
solver = Solver()

# Use Z3 Array for grid to allow symbolic indexing
grid = Array('grid', IntSort(), IntSort())

# For each word, we need starting position and direction
word_positions = []
word_directions = []

for idx, (word, clue) in enumerate(WORDS):
    # Starting position (row, col) - must be within bounds
    row = Int(f"word_{idx}_row")
    col = Int(f"word_{idx}_col")
    # Direction: 0 = horizontal, 1 = vertical
    direction = Int(f"word_{idx}_dir")
    
    # Constraints for valid placement
    solver.add(row >= 0, row < GRID_SIZE)
    solver.add(col >= 0, col < GRID_SIZE)
    solver.add(Or(direction == 0, direction == 1))
    
    # Word length
    word_len = len(word)
    
    # Ensure word fits in grid
    solver.add(Implies(direction == 0, col + word_len <= GRID_SIZE))
    solver.add(Implies(direction == 1, row + word_len <= GRID_SIZE))
    
    word_positions.append((row, col))
    word_directions.append(direction)
    
    # Place word in grid using Or-loop pattern
    for pos, char in enumerate(word):
        char_code = ord(char)
        # For horizontal placement: grid[row * GRID_SIZE + (col + pos)] = char_code
        # For vertical placement: grid[(row + pos) * GRID_SIZE + col] = char_code
        solver.add(Implies(
            direction == 0,
            Select(grid, row * GRID_SIZE + (col + pos)) == char_code
        ))
        solver.add(Implies(
            direction == 1,
            Select(grid, (row + pos) * GRID_SIZE + col) == char_code
        ))

# Ensure intersections match
for i in range(len(WORDS)):
    for j in range(i + 1, len(WORDS)):
        row_i, col_i = word_positions[i]
        row_j, col_j = word_positions[j]
        dir_i = word_directions[i]
        dir_j = word_directions[j]
        word_i = WORDS[i][0]
        word_j = WORDS[j][0]
        len_i = len(word_i)
        len_j = len(word_j)
        
        # Check all possible intersection positions
        for pos_i in range(len_i):
            for pos_j in range(len_j):
                # Horizontal i, vertical j
                solver.add(Implies(
                    And(dir_i == 0, dir_j == 1,
                        row_i == row_j + pos_j,
                        col_i + pos_i == col_j),
                    Select(grid, row_i * GRID_SIZE + (col_i + pos_i)) == 
                    Select(grid, (row_j + pos_j) * GRID_SIZE + col_j)
                ))
                
                # Vertical i, horizontal j
                solver.add(Implies(
                    And(dir_i == 1, dir_j == 0,
                        row_i + pos_i == row_j,
                        col_i == col_j + pos_j),
                    Select(grid, (row_i + pos_i) * GRID_SIZE + col_i) == 
                    Select(grid, row_j * GRID_SIZE + (col_j + pos_j))
                ))

# Ensure at least one intersection exists
# We'll count intersections by checking all pairs
intersection_vars = []
for i in range(len(WORDS)):
    for j in range(i + 1, len(WORDS)):
        row_i, col_i = word_positions[i]
        row_j, col_j = word_positions[j]
        dir_i = word_directions[i]
        dir_j = word_directions[j]
        word_i = WORDS[i][0]
        word_j = WORDS[j][0]
        len_i = len(word_i)
        len_j = len(word_j)
        
        # Create a variable to indicate if these words intersect
        intersects = Bool(f"intersects_{i}_{j}")
        intersection_vars.append(intersects)
        
        # They intersect if there exists pos_i, pos_j such that:
        # (dir_i=0, dir_j=1, row_i == row_j+pos_j, col_i+pos_i == col_j) OR
        # (dir_i=1, dir_j=0, row_i+pos_i == row_j, col_i == col_j+pos_j)
        intersection_conditions = []
        for pos_i in range(len_i):
            for pos_j in range(len_j):
                intersection_conditions.append(
                    Or(
                        And(dir_i == 0, dir_j == 1,
                            row_i == row_j + pos_j,
                            col_i + pos_i == col_j),
                        And(dir_i == 1, dir_j == 0,
                            row_i + pos_i == row_j,
                            col_i == col_j + pos_j)
                    )
                )
        
        solver.add(intersects == Or(intersection_conditions))

# At least one intersection must exist
solver.add(Or(intersection_vars))

# Check for solution
result = solver.check()

if result == sat:
    model = solver.model()
    print("STATUS: sat")
    print("\nGrid layout:")
    
    # Build and print grid
    grid_chars = [[' ' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            cell_val = model.eval(Select(grid, i * GRID_SIZE + j))
            if cell_val.is_num():
                grid_chars[i][j] = chr(int(str(cell_val)))
    
    for row in grid_chars:
        print(' '.join(row))
    
    print("\nWord placements:")
    for idx, (word, clue) in enumerate(WORDS):
        row = int(str(model.eval(word_positions[idx][0])))
        col = int(str(model.eval(word_positions[idx][1])))
        dir_val = int(str(model.eval(word_directions[idx])))
        direction = "horizontal" if dir_val == 0 else "vertical"
        print(f"{word}: position [{row}, {col}], direction {direction}, clue: {clue}")
    
    # Find intersections
    print("\nIntersections:")
    for i in range(len(WORDS)):
        for j in range(i + 1, len(WORDS)):
            row_i = int(str(model.eval(word_positions[i][0])))
            col_i = int(str(model.eval(word_positions[i][1])))
            dir_i = int(str(model.eval(word_directions[i])))
            row_j = int(str(model.eval(word_positions[j][0])))
            col_j = int(str(model.eval(word_positions[j][1])))
            dir_j = int(str(model.eval(word_directions[j])))
            
            word_i = WORDS[i][0]
            word_j = WORDS[j][0]
            len_i = len(word_i)
            len_j = len(word_j)
            
            # Check for intersection
            for pos_i in range(len_i):
                for pos_j in range(len_j):
                    if dir_i == 0 and dir_j == 1:
                        if row_i == row_j + pos_j and col_i + pos_i == col_j:
                            cell_idx = row_i * GRID_SIZE + (col_i + pos_i)
                            letter = chr(int(str(model.eval(Select(grid, cell_idx)))))
                            print(f"  {word_i} (pos {pos_i}) intersects {word_j} (pos {pos_j}) at letter '{letter}'")
                    elif dir_i == 1 and dir_j == 0:
                        if row_i + pos_i == row_j and col_i == col_j + pos_j:
                            cell_idx = (row_i + pos_i) * GRID_SIZE + col_i
                            letter = chr(int(str(model.eval(Select(grid, cell_idx)))))
                            print(f"  {word_i} (pos {pos_i}) intersects {word_j} (pos {pos_j}) at letter '{letter}'")
    
elif result == unsat:
    print("STATUS: unsat")
    print("No valid crossword layout found")
else:
    print("STATUS: unknown")
    print("Solver returned unknown result")