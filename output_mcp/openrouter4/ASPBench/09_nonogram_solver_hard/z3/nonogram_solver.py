from z3 import *
import time

solver = Solver()
solver.set("timeout", 600000)  # 10 minutes timeout

N = 24

# Grid variables: grid[r][c] ∈ {0, 1, 2, 3}
grid = [[Int(f'g_{r}_{c}') for c in range(N)] for r in range(N)]

# Cell domains
for r in range(N):
    for c in range(N):
        solver.add(And(grid[r][c] >= 0, grid[r][c] <= 3))

# ---------- DIAGONAL CONSTRAINTS ----------
main_diag = [1, 1, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0, 0, 0, 0, 0, 1, 1]
anti_diag = [1, 1, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0, 0, 0, 0, 0, 1, 1]

for i in range(N):
    solver.add(grid[i][i] == main_diag[i])
    solver.add(grid[i][N - 1 - i] == anti_diag[i])

# ---------- CLUES ----------
row_clues = [
    [(1,10), (2,4), (1,10)],
    [(1,10), (2,4), (1,10)],
    [(1,2), (2,4), (1,2)],
    [(1,2), (2,4), (1,2)],
    [(1,2), (2,4), (1,2)],
    [(1,2), (2,4), (1,2)],
    [(1,2), (2,4), (1,2)],
    [(1,2), (2,4), (1,2)],
    [(1,2), (3,8), (1,2)],
    [(1,2), (3,8), (1,2)],
    [(1,2), (2,6), (3,8), (2,6), (1,2)],
    [(1,2), (2,6), (3,8), (2,6), (1,2)],
    [(1,2), (2,6), (3,8), (2,6), (1,2)],
    [(1,2), (2,6), (3,8), (2,6), (1,2)],
    [(1,2), (3,8), (1,2)],
    [(1,2), (3,8), (1,2)],
    [(1,2), (2,4), (1,2)],
    [(1,2), (2,4), (1,2)],
    [(1,2), (2,4), (1,2)],
    [(1,2), (2,4), (1,2)],
    [(1,2), (2,4), (1,2)],
    [(1,2), (2,4), (1,2)],
    [(1,10), (2,4), (1,10)],
    [(1,10), (2,4), (1,10)]
]

col_clues = [
    [(1,24)],
    [(1,24)],
    [(1,2), (2,4), (1,2)],
    [(1,2), (2,4), (1,2)],
    [(1,2), (2,4), (1,2)],
    [(1,2), (2,4), (1,2)],
    [(1,2), (2,4), (1,2)],
    [(1,2), (2,4), (1,2)],
    [(1,2), (3,8), (1,2)],
    [(1,2), (3,8), (1,2)],
    [(2,8), (3,8), (2,8)],
    [(2,8), (3,8), (2,8)],
    [(2,8), (3,8), (2,8)],
    [(2,8), (3,8), (2,8)],
    [(1,2), (3,8), (1,2)],
    [(1,2), (3,8), (1,2)],
    [(1,2), (2,4), (1,2)],
    [(1,2), (2,4), (1,2)],
    [(1,2), (2,4), (1,2)],
    [(1,2), (2,4), (1,2)],
    [(1,2), (2,4), (1,2)],
    [(1,2), (2,4), (1,2)],
    [(1,24)],
    [(1,24)]
]

def add_run_constraints(solver, grid, N, is_row, idx, clues):
    """Add run constraints for a row (is_row=True) or column (is_row=False)."""
    m = len(clues)
    if m == 0:
        for p in range(N):
            if is_row:
                solver.add(grid[idx][p] == 0)
            else:
                solver.add(grid[p][idx] == 0)
        return
    
    colors = [c for c, l in clues]
    lengths = [l for c, l in clues]
    
    # Start positions for each run
    starts = [Int(f'{"R" if is_row else "C"}_{idx}_s_{j}') for j in range(m)]
    
    for j in range(m):
        solver.add(starts[j] >= 0)
        solver.add(starts[j] + lengths[j] <= N)
    
    # Ordering constraints between runs
    for j in range(m - 1):
        sep = 1 if colors[j] == colors[j + 1] else 0
        solver.add(starts[j] + lengths[j] + sep <= starts[j + 1])
    
    # For each position p
    for p in range(N):
        # Build list of (in_run_j, color_j) conditions
        in_run_conditions = []
        for j in range(m):
            in_run_conditions.append(And(starts[j] <= p, p < starts[j] + lengths[j]))
        
        in_any_run = Or(in_run_conditions)
        
        # If p is in run j, cell must have the run's color
        for j in range(m):
            cell = grid[idx][p] if is_row else grid[p][idx]
            solver.add(Implies(
                And(starts[j] <= p, p < starts[j] + lengths[j]),
                cell == colors[j]
            ))
        
        # Exhaustiveness: if cell is not white, it must be in some run
        cell = grid[idx][p] if is_row else grid[p][idx]
        solver.add(Implies(cell != 0, in_any_run))

print(f"Adding row constraints...")
for r in range(N):
    add_run_constraints(solver, grid, N, True, r, row_clues[r])

print(f"Adding column constraints...")
for c in range(N):
    add_run_constraints(solver, grid, N, False, c, col_clues[c])

print(f"Starting solver...")
start_time = time.time()
result = solver.check()
elapsed = time.time() - start_time

print(f"Solver finished in {elapsed:.2f}s with result: {result}")

if result == sat:
    m = solver.model()
    print("STATUS: sat")
    print("Solution found!")
    print()
    # Print the grid
    print("Grid (0=white, 1=red, 2=green, 3=blue):")
    for r in range(N):
        row_vals = [m.eval(grid[r][c]).as_long() for c in range(N)]
        print(' '.join(str(v) for v in row_vals))
    
    # Verify diagonals
    print()
    print("Main diagonal:")
    md = [m.eval(grid[i][i]).as_long() for i in range(N)]
    print(md)
    print("Expected:", main_diag)
    print("Match:", md == main_diag)
    
    print()
    print("Anti diagonal:")
    ad = [m.eval(grid[i][N-1-i]).as_long() for i in range(N)]
    print(ad)
    print("Expected:", anti_diag)
    print("Match:", ad == anti_diag)
    
elif result == unsat:
    print("STATUS: unsat")
    print("No solution exists.")
    if True:  # BENCHMARK_MODE is ON
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")