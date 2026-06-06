from z3 import *

solver = Solver()
solver.set("timeout", 180000)

N = 14

# Grid: 14x14 Bool variables
grid = [[Bool(f'g_{i}_{j}') for j in range(N)] for i in range(N)]

# Placement variables (top-left of bounding box)
block_r, block_c = Int('block_r'), Int('block_c')
boat_r, boat_c = Int('boat_r'), Int('boat_c')
loaf_r, loaf_c = Int('loaf_r'), Int('loaf_c')

# Pattern cell offsets (relative to top-left)
block_cells = [(0,0), (0,1), (1,0), (1,1)]
boat_cells  = [(0,0), (0,1), (1,0), (1,2), (2,1)]
loaf_cells  = [(0,1), (0,2), (1,0), (1,3), (2,1), (2,3), (3,2)]

# Boundary constraints: all pattern cells must fit in 14x14
solver.add(block_r >= 0, block_r + 1 <= N - 1)
solver.add(block_c >= 0, block_c + 1 <= N - 1)
solver.add(boat_r >= 0,  boat_r + 2  <= N - 1)
solver.add(boat_c >= 0,  boat_c + 2  <= N - 1)
solver.add(loaf_r >= 0,  loaf_r + 3  <= N - 1)
solver.add(loaf_c >= 0,  loaf_c + 3  <= N - 1)

# For each cell: pattern membership, grid linking, non-overlap
for i in range(N):
    for j in range(N):
        in_b = Or([And(i == block_r + dr, j == block_c + dc) for dr, dc in block_cells])
        in_o = Or([And(i == boat_r + dr, j == boat_c + dc) for dr, dc in boat_cells])
        in_l = Or([And(i == loaf_r + dr, j == loaf_c + dc) for dr, dc in loaf_cells])

        # Cell alive iff part of any pattern
        solver.add(grid[i][j] == Or(in_b, in_o, in_l))
        # Non-overlap: at most one pattern claims this cell
        solver.add(If(in_b, 1, 0) + If(in_o, 1, 0) + If(in_l, 1, 0) <= 1)

# Still life constraints for every cell
for i in range(N):
    for j in range(N):
        # Collect valid neighbors
        nbrs = []
        for di in [-1, 0, 1]:
            for dj in [-1, 0, 1]:
                if di == 0 and dj == 0:
                    continue
                ni, nj = i + di, j + dj
                if 0 <= ni < N and 0 <= nj < N:
                    nbrs.append(grid[ni][nj])
        nc = Sum([If(n, 1, 0) for n in nbrs])

        # Still life rule:
        #   alive cell  -> exactly 2 or 3 live neighbors
        #   dead cell   -> NOT exactly 3 live neighbors (no birth)
        solver.add(If(grid[i][j], And(nc >= 2, nc <= 3), nc != 3))

BENCHMARK_MODE = True
result = solver.check()

if result == sat:
    m = solver.model()
    print("STATUS: sat")

    br_v = m.eval(block_r, model_completion=True).as_long()
    bc_v = m.eval(block_c, model_completion=True).as_long()
    or_v = m.eval(boat_r, model_completion=True).as_long()
    oc_v = m.eval(boat_c, model_completion=True).as_long()
    lr_v = m.eval(loaf_r, model_completion=True).as_long()
    lc_v = m.eval(loaf_c, model_completion=True).as_long()

    print(f"\nPatterns:")
    print(f"  block: bbox [{br_v}, {bc_v}, {br_v+1}, {bc_v+1}]")
    print(f"  boat:  bbox [{or_v}, {oc_v}, {or_v+2}, {oc_v+2}]")
    print(f"  loaf:  bbox [{lr_v}, {lc_v}, {lr_v+3}, {lc_v+3}]")

    print(f"\nGrid (# = live, . = dead):")
    for i in range(N):
        row_str = ""
        for j in range(N):
            row_str += "#" if is_true(m.eval(grid[i][j], model_completion=True)) else "."
        print(row_str)

    print(f"\nGrid array (0/1):")
    for i in range(N):
        vals = []
        for j in range(N):
            vals.append("1" if is_true(m.eval(grid[i][j], model_completion=True)) else "0")
        print("[" + ", ".join(vals) + "]")

    # Verification: count live cells
    live_count = sum(1 for i in range(N) for j in range(N)
                     if is_true(m.eval(grid[i][j], model_completion=True)))
    print(f"\nTotal live cells: {live_count} (expected 16)")

elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")