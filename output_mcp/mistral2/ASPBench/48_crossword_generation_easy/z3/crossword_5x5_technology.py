from z3 import *

# BENCHMARK_MODE: ON (model-finding mode)
BENCHMARK_MODE = True

# Problem: Place 6 technology-themed words on a 5x5 grid with proper intersections
# Words: CODE, DATA, TECH, CHIP, BYTE, NET

# Declare the grid as a 5x5 array of characters (we'll use Int to represent letters as ASCII codes)
# We'll use 0 to represent empty space (or a space character)
Grid = [[Int(f"grid_{i}_{j}") for j in range(5)] for i in range(5)]

# Helper function to convert a letter to its ASCII code
# We'll use 0 to represent empty space
space = 0

def letter_to_int(letter):
    return ord(letter)

# Word list
words = ["CODE", "DATA", "TECH", "CHIP", "BYTE", "NET"]
word_lengths = {w: len(w) for w in words}

# Directions
HORIZONTAL = 0
VERTICAL = 1

# We need to place each word exactly once
# For each word, we need to choose a starting position and direction
# We'll use a list of tuples: (word, row, col, direction)
# We'll use Int variables to represent the choice of position and direction for each word

# For each word, we'll have:
# - A variable for the starting row (0-4)
# - A variable for the starting column (0-4)
# - A variable for the direction (0=horizontal, 1=vertical)

# We'll use a solver to find a valid placement
solver = Solver()

# Decision variables for each word's placement
# For each word, we'll have:
# - row: Int (0-4)
# - col: Int (0-4)
# - direction: Int (0=horizontal, 1=vertical)
placements = []
for w in words:
    row = Int(f"row_{w}")
    col = Int(f"col_{w}")
    direction = Int(f"dir_{w}")
    placements.append((w, row, col, direction))
    # Constraints: row and col must be within bounds
    solver.add(row >= 0, row < 5)
    solver.add(col >= 0, col < 5)
    # Direction must be 0 or 1
    solver.add(direction >= 0, direction <= 1)

# All words must be placed exactly once
# We'll ensure that the placements are unique by constraining the (row, col, direction) tuples to be unique
for i in range(len(placements)):
    for j in range(i+1, len(placements)):
        w1, r1, c1, d1 = placements[i]
        w2, r2, c2, d2 = placements[j]
        # Either the starting positions or directions must differ
        solver.add(Or(r1 != r2, c1 != c2, d1 != d2))

# Place each word on the grid according to its placement
for w, r, c, d in placements:
    L = word_lengths[w]
    # For horizontal placement: letters go from (r, c) to (r, c+L-1)
    # For vertical placement: letters go from (r, c) to (r+L-1, c)
    for i in range(L):
        if d == HORIZONTAL:
            # Horizontal: (r, c+i)
            solver.add(Grid[r][c+i] == letter_to_int(w[i]))
        else:
            # Vertical: (r+i, c)
            solver.add(Grid[r+i][c] == letter_to_int(w[i]))

# No conflicts: If two words intersect, their letters must match
# We need to check all pairs of words for intersections
for i in range(len(placements)):
    for j in range(i+1, len(placements)):
        w1, r1, c1, d1 = placements[i]
        w2, r2, c2, d2 = placements[j]
        L1 = word_lengths[w1]
        L2 = word_lengths[w2]
        
        # Check for intersection
        # Case 1: w1 is horizontal, w2 is vertical
        if d1 == HORIZONTAL and d2 == VERTICAL:
            # w1: (r1, c1) to (r1, c1+L1-1)
            # w2: (r2, c2) to (r2+L2-1, c2)
            # Intersection if r1 == r2 and c1 <= c2 < c1+L1 and c2 == c1 + offset
            for offset in range(L1):
                solver.add(Implies(
                    And(r1 == r2, c1 + offset == c2, c2 >= c1, c2 < c1 + L1),
                    Grid[r1][c1+offset] == Grid[r2][c2]
                ))
        # Case 2: w1 is vertical, w2 is horizontal
        elif d1 == VERTICAL and d2 == HORIZONTAL:
            # w1: (r1, c1) to (r1+L1-1, c1)
            # w2: (r2, c2) to (r2, c2+L2-1)
            # Intersection if c1 == c2 and r1 <= r2 < r1+L1 and r2 == r1 + offset
            for offset in range(L1):
                solver.add(Implies(
                    And(c1 == c2, r1 + offset == r2, r2 >= r1, r2 < r1 + L1),
                    Grid[r1+offset][c1] == Grid[r2][c2]
                ))
        # Case 3: Both horizontal or both vertical: no intersection possible (parallel)

# Ensure all grid cells are either empty (0) or contain a letter
for i in range(5):
    for j in range(5):
        solver.add(Or(Grid[i][j] == space, 
                      And(Grid[i][j] >= letter_to_int('A'), Grid[i][j] <= letter_to_int('Z'))))

# Check if a solution exists
result = solver.check()

if result == sat:
    model = solver.model()
    print("STATUS: sat")
    # Extract the grid
    grid_solution = [[model[Grid[i][j]] for j in range(5)] for i in range(5)]
    # Print the grid
    print("Grid:")
    for i in range(5):
        row_str = ""
        for j in range(5):
            val = model[Grid[i][j]]
            if val == space:
                row_str += "."
            else:
                row_str += chr(val.as_long())
        print(row_str)
    # Print the placements
    print("\nPlacements:")
    for w, r, c, d in placements:
        r_val = model[r]
        c_val = model[c]
        d_val = model[d]
        direction_str = "horizontal" if d_val.as_long() == HORIZONTAL else "vertical"
        print(f"{w}: start=({r_val},{c_val}), direction={direction_str}")
    # Print the intersections (if any)
    print("\nIntersections:")
    intersections = []
    for i in range(len(placements)):
        for j in range(i+1, len(placements)):
            w1, r1, c1, d1 = placements[i]
            w2, r2, c2, d2 = placements[j]
            L1 = word_lengths[w1]
            L2 = word_lengths[w2]
            
            if d1 == HORIZONTAL and d2 == VERTICAL:
                for offset in range(L1):
                    r1_val = model[r1]
                    c1_val = model[c1]
                    r2_val = model[r2]
                    c2_val = model[c2]
                    d1_val = model[d1]
                    d2_val = model[d2]
                    if (model.eval(And(r1_val == r2_val, c1_val + offset == c2_val, c2_val >= c1_val, c2_val < c1_val + L1), True)):
                        letter = chr(model[Grid[r1_val][c1_val+offset]].as_long())
                        intersections.append((w1, w2, offset, 0, letter))
            elif d1 == VERTICAL and d2 == HORIZONTAL:
                for offset in range(L1):
                    r1_val = model[r1]
                    c1_val = model[c1]
                    r2_val = model[r2]
                    c2_val = model[c2]
                    d1_val = model[d1]
                    d2_val = model[d2]
                    if (model.eval(And(c1_val == c2_val, r1_val + offset == r2_val, r2_val >= r1_val, r2_val < r1_val + L1), True)):
                        letter = chr(model[Grid[r1_val+offset][c1_val]].as_long())
                        intersections.append((w1, w2, 0, offset, letter))
    for w1, w2, pos1, pos2, letter in intersections:
        print(f"{w1}[{pos1}] and {w2}[{pos2}] intersect at '{letter}'")
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")