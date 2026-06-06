from z3 import *

# Grid size
N = 14

# Create grid variables
grid = [[Bool(f"cell_{r}_{c}") for c in range(N)] for r in range(N)]

solver = Solver()

# Pattern placement variables (top-left corner of each pattern's bounding box)
br = Int('block_r')
bc = Int('block_c')
or_ = Int('boat_r')
oc = Int('boat_c')
lr = Int('loaf_r')
lc = Int('loaf_c')

# Block relative positions (2x2 square)
block_cells = [(0,0), (0,1), (1,0), (1,1)]

# Boat relative positions (5-cell bilateral pattern)
boat_cells = [(0,0), (0,1), (1,0), (1,2), (2,1)]

# Loaf relative positions (7-cell pattern)
loaf_cells = [(0,1), (0,2), (1,0), (1,3), (2,1), (2,3), (3,2)]

# Boundary constraints for patterns
# Block: 2x2, needs br+1 < N and bc+1 < N
solver.add(br >= 0, br + 1 < N)
solver.add(bc >= 0, bc + 1 < N)

# Boat: max row is or_+2, max col is oc+2
solver.add(or_ >= 0, or_ + 2 < N)
solver.add(oc >= 0, oc + 2 < N)

# Loaf: max row is lr+3, max col is lc+3
solver.add(lr >= 0, lr + 3 < N)
solver.add(lc >= 0, lc + 3 < N)

# Define grid cells based on pattern coverage
for r in range(N):
    for c in range(N):
        block_cover = Or([And(br == r - dr, bc == c - dc) for dr, dc in block_cells])
        boat_cover = Or([And(or_ == r - dr, oc == c - dc) for dr, dc in boat_cells])
        loaf_cover = Or([And(lr == r - dr, lc == c - dc) for dr, dc in loaf_cells])
        any_cover = Or(block_cover, boat_cover, loaf_cover)
        solver.add(grid[r][c] == any_cover)

# No overlapping constraints
# Block-Boat
for dr1, dc1 in block_cells:
    for dr2, dc2 in boat_cells:
        solver.add(Not(And(br + dr1 == or_ + dr2, bc + dc1 == oc + dc2)))

# Block-Loaf
for dr1, dc1 in block_cells:
    for dr2, dc2 in loaf_cells:
        solver.add(Not(And(br + dr1 == lr + dr2, bc + dc1 == lc + dc2)))

# Boat-Loaf
for dr1, dc1 in boat_cells:
    for dr2, dc2 in loaf_cells:
        solver.add(Not(And(or_ + dr1 == lr + dr2, oc + dc1 == lc + dc2)))

# Helper function to count live neighbors
def count_live_neighbors(r, c):
    neighbors = []
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            nr, nc = r + dr, c + dc
            if 0 <= nr < N and 0 <= nc < N:
                neighbors.append(If(grid[nr][nc], 1, 0))
    return Sum(neighbors)

# Still Life Rules
for r in range(N):
    for c in range(N):
        live_neighbors = count_live_neighbors(r, c)
        # Live cell must have exactly 2 or 3 live neighbors
        solver.add(Implies(grid[r][c], And(live_neighbors >= 2, live_neighbors <= 3)))
        # Dead cell must NOT have exactly 3 live neighbors (prevents birth)
        solver.add(Implies(Not(grid[r][c]), live_neighbors != 3))

# Solve
BENCHMARK_MODE = True
result = solver.check()

if result == sat:
    m = solver.model()
    print("STATUS: sat")
    print(f"Block placed at top-left: ({m[br]}, {m[bc]})")
    print(f"Boat placed at top-left: ({m[or_]}, {m[oc]})")
    print(f"Loaf placed at top-left: ({m[lr]}, {m[lc]})")
    print()
    print("Grid (14x14):")
    print("   ", end="")
    for c in range(N):
        print(f"{c:2d}", end="")
    print()
    for r in range(N):
        print(f"{r:2d} ", end="")
        for c in range(N):
            if m.eval(grid[r][c]):
                print(" 1", end="")
            else:
                print(" 0", end="")
        print()
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")