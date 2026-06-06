from z3 import *

# Grid dimensions
N = 14

# Create solver
solver = Solver()

# Grid cells: 1 = live, 0 = dead
grid = [[Bool(f"cell_{i}_{j}") for j in range(N)] for i in range(N)]

# Pattern placement variables (top-left corner)
block_r, block_c = Ints('block_r block_c')
boat_r, boat_c = Ints('boat_r boat_c')
loaf_r, loaf_c = Ints('loaf_r loaf_c')

# 1. Boundary constraints for pattern placements
solver.add(block_r >= 0, block_r <= N-2)  # Block is 2x2
solver.add(block_c >= 0, block_c <= N-2)
solver.add(boat_r >= 0, boat_r <= N-3)    # Boat is 3x3 bounding box
solver.add(boat_c >= 0, boat_c <= N-3)
solver.add(loaf_r >= 0, loaf_r <= N-4)    # Loaf is 4x4 bounding box
solver.add(loaf_c >= 0, loaf_c <= N-4)

# 2. Pattern definitions (relative positions)
# Block: 2x2 square at (0,0), (0,1), (1,0), (1,1)
block_cells = [(0,0), (0,1), (1,0), (1,1)]

# Boat: 5 cells at (0,0), (0,1), (1,0), (1,2), (2,1)
boat_cells = [(0,0), (0,1), (1,0), (1,2), (2,1)]

# Loaf: 7 cells at (0,1), (0,2), (1,0), (1,3), (2,1), (2,3), (3,2)
loaf_cells = [(0,1), (0,2), (1,0), (1,3), (2,1), (2,3), (3,2)]

# 3. Pattern placement constraints using Or-Loop pattern
# For each pattern cell, ensure it's live at the correct position
for dr, dc in block_cells:
    # grid[block_r + dr][block_c + dc] must be True
    # Use Or-Loop to handle symbolic indexing
    solver.add(Or([And(block_r + dr == i, block_c + dc == j, grid[i][j]) 
                   for i in range(N) for j in range(N)]))

for dr, dc in boat_cells:
    solver.add(Or([And(boat_r + dr == i, boat_c + dc == j, grid[i][j]) 
                   for i in range(N) for j in range(N)]))

for dr, dc in loaf_cells:
    solver.add(Or([And(loaf_r + dr == i, loaf_c + dc == j, grid[i][j]) 
                   for i in range(N) for j in range(N)]))

# 4. No overlapping between patterns
# Create a list of all pattern cell positions (symbolic)
all_pattern_positions = []
for dr, dc in block_cells:
    all_pattern_positions.append((block_r + dr, block_c + dc))
for dr, dc in boat_cells:
    all_pattern_positions.append((boat_r + dr, boat_c + dc))
for dr, dc in loaf_cells:
    all_pattern_positions.append((loaf_r + dr, loaf_c + dc))

# Ensure no two pattern cells occupy the same grid position
for i in range(len(all_pattern_positions)):
    for j in range(i+1, len(all_pattern_positions)):
        r1, c1 = all_pattern_positions[i]
        r2, c2 = all_pattern_positions[j]
        solver.add(Or(r1 != r2, c1 != c2))

# 5. Global stability constraints (Game of Life still life)
def count_live_neighbors(r, c):
    neighbors = []
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            nr, nc = r + dr, c + dc
            if 0 <= nr < N and 0 <= nc < N:
                neighbors.append(grid[nr][nc])
    # Convert Bool to Int (1 for True, 0 for False)
    neighbor_ints = [If(nb, 1, 0) for nb in neighbors]
    return Sum(neighbor_ints)

# Apply still life rules to ALL cells
for i in range(N):
    for j in range(N):
        neighbors = count_live_neighbors(i, j)
        # Rule: Live cell must have 2 or 3 neighbors
        # Rule: Dead cell must NOT have exactly 3 neighbors
        solver.add(Implies(grid[i][j], Or(neighbors == 2, neighbors == 3)))
        solver.add(Implies(Not(grid[i][j]), neighbors != 3))

# 6. Additional constraint: Only the specified patterns should be live
# All other cells must be dead
# First, create a boolean for each cell indicating if it's a pattern cell
is_pattern_cell = [[Bool(f"is_pattern_{i}_{j}") for j in range(N)] for i in range(N)]

# Mark pattern cells
for dr, dc in block_cells:
    for i in range(N):
        for j in range(N):
            solver.add(Implies(And(block_r + dr == i, block_c + dc == j), is_pattern_cell[i][j]))

for dr, dc in boat_cells:
    for i in range(N):
        for j in range(N):
            solver.add(Implies(And(boat_r + dr == i, boat_c + dc == j), is_pattern_cell[i][j]))

for dr, dc in loaf_cells:
    for i in range(N):
        for j in range(N):
            solver.add(Implies(And(loaf_r + dr == i, loaf_c + dc == j), is_pattern_cell[i][j]))

# Ensure non-pattern cells are dead
for i in range(N):
    for j in range(N):
        solver.add(Implies(Not(is_pattern_cell[i][j]), Not(grid[i][j])))

# Check for solution
result = solver.check()

if result == sat:
    print("STATUS: sat")
    m = solver.model()
    
    # Print grid
    print("\nGrid (1=live, 0=dead):")
    for i in range(N):
        row = []
        for j in range(N):
            cell_val = m.evaluate(grid[i][j])
            row.append('1' if cell_val else '0')
        print(' '.join(row))
    
    # Print pattern placements
    print(f"\nBlock placement: ({m[block_r]}, {m[block_c]})")
    print(f"Boat placement: ({m[boat_r]}, {m[boat_c]})")
    print(f"Loaf placement: ({m[loaf_r]}, {m[loaf_c]})")
    
    # Verify no overlap
    print("\nVerifying no overlap...")
    pattern_positions = set()
    for dr, dc in block_cells:
        pattern_positions.add((int(m[block_r]) + dr, int(m[block_c]) + dc))
    for dr, dc in boat_cells:
        pattern_positions.add((int(m[boat_r]) + dr, int(m[boat_c]) + dc))
    for dr, dc in loaf_cells:
        pattern_positions.add((int(m[loaf_r]) + dr, int(m[loaf_c]) + dc))
    
    if len(pattern_positions) == len(block_cells) + len(boat_cells) + len(loaf_cells):
        print("✓ No overlap detected")
    else:
        print("✗ Overlap detected!")
    
    # Verify stability
    print("\nVerifying stability...")
    stable = True
    for i in range(N):
        for j in range(N):
            cell_live = bool(m.evaluate(grid[i][j]))
            neighbors = 0
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr == 0 and dc == 0:
                        continue
                    nr, nc = i + dr, j + dc
                    if 0 <= nr < N and 0 <= nc < N:
                        if bool(m.evaluate(grid[nr][nc])):
                            neighbors += 1
            
            if cell_live and neighbors not in [2, 3]:
                print(f"✗ Cell ({i},{j}) is live but has {neighbors} neighbors")
                stable = False
            if not cell_live and neighbors == 3:
                print(f"✗ Cell ({i},{j}) is dead but has 3 neighbors (would birth)")
                stable = False
    
    if stable:
        print("✓ All cells satisfy still life rules")
    
elif result == unsat:
    print("STATUS: unsat")
    print("No valid configuration found")
else:
    print("STATUS: unknown")
    print("Solver returned unknown result")