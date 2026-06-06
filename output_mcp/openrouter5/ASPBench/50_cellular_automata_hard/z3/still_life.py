from z3 import *

# Grid size
N = 14

# Use Z3 Array for the grid so we can index symbolically
grid = Array('grid', IntSort(), ArraySort(IntSort(), IntSort()))

solver = Solver()

# Each cell is either 0 or 1
for r in range(N):
    for c in range(N):
        solver.add(Or(Select(Select(grid, r), c) == 0, Select(Select(grid, r), c) == 1))

# Pattern definitions (relative coordinates)
block_cells = [(0,0), (0,1), (1,0), (1,1)]
boat_cells = [(0,0), (0,1), (1,0), (1,2), (2,1)]
loaf_cells = [(0,1), (0,2), (1,0), (1,3), (2,1), (2,3), (3,2)]

# We'll place each pattern by choosing its top-left corner (row, col)
block_r = Int('block_r')
block_c = Int('block_c')
boat_r = Int('boat_r')
boat_c = Int('boat_c')
loaf_r = Int('loaf_r')
loaf_c = Int('loaf_c')

# Domain constraints: pattern must fit within grid
solver.add(block_r >= 0, block_r <= N - 2)
solver.add(block_c >= 0, block_c <= N - 2)
solver.add(boat_r >= 0, boat_r <= N - 3)
solver.add(boat_c >= 0, boat_c <= N - 3)
solver.add(loaf_r >= 0, loaf_r <= N - 4)
solver.add(loaf_c >= 0, loaf_c <= N - 4)

# Constraint: cells covered by each pattern must be live (1)
for dr, dc in block_cells:
    solver.add(Select(Select(grid, block_r + dr), block_c + dc) == 1)

for dr, dc in boat_cells:
    solver.add(Select(Select(grid, boat_r + dr), boat_c + dc) == 1)

for dr, dc in loaf_cells:
    solver.add(Select(Select(grid, loaf_r + dr), loaf_c + dc) == 1)

# Constraint: No overlapping between patterns
# For each pair of cells from different patterns, they must not be the same grid cell
for dr1, dc1 in block_cells:
    for dr2, dc2 in boat_cells:
        solver.add(Not(And(block_r + dr1 == boat_r + dr2, block_c + dc1 == boat_c + dc2)))

for dr1, dc1 in block_cells:
    for dr2, dc2 in loaf_cells:
        solver.add(Not(And(block_r + dr1 == loaf_r + dr2, block_c + dc1 == loaf_c + dc2)))

for dr1, dc1 in boat_cells:
    for dr2, dc2 in loaf_cells:
        solver.add(Not(And(boat_r + dr1 == loaf_r + dr2, boat_c + dc1 == loaf_c + dc2)))

# Helper: count live neighbors for a cell
def count_live_neighbors(r, c):
    neighbors = []
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            nr, nc = r + dr, c + dc
            if 0 <= nr < N and 0 <= nc < N:
                neighbors.append(Select(Select(grid, nr), nc))
    return Sum(neighbors)

# Global still life constraints
for r in range(N):
    for c in range(N):
        live_neighbors = count_live_neighbors(r, c)
        cell_val = Select(Select(grid, r), c)
        solver.add(Implies(cell_val == 1, Or(live_neighbors == 2, live_neighbors == 3)))
        solver.add(Implies(cell_val == 0, live_neighbors != 3))

# Constraint: any live cell must belong to one of the three patterns
for r in range(N):
    for c in range(N):
        in_block = Or([And(block_r + dr == r, block_c + dc == c) for dr, dc in block_cells])
        in_boat = Or([And(boat_r + dr == r, boat_c + dc == c) for dr, dc in boat_cells])
        in_loaf = Or([And(loaf_r + dr == r, loaf_c + dc == c) for dr, dc in loaf_cells])
        solver.add(Implies(Select(Select(grid, r), c) == 1, Or(in_block, in_boat, in_loaf)))

print("Solving...")
result = solver.check()
print(f"Result: {result}")

if result == sat:
    m = solver.model()
    print("STATUS: sat")
    print(f"Block at: ({m[block_r]}, {m[block_c]})")
    print(f"Boat at: ({m[boat_r]}, {m[boat_c]})")
    print(f"Loaf at: ({m[loaf_r]}, {m[loaf_c]})")
    
    # Print grid
    print("\nGrid (1=live, 0=dead):")
    for r in range(N):
        row_str = ""
        for c in range(N):
            val = m.eval(Select(Select(grid, r), c))
            row_str += str(val) + " "
        print(row_str)
else:
    print("STATUS: unsat")
    print("No solution found.")