from z3 import *

BENCHMARK_MODE = True

# Grid size
N = 14

# Declare grid variables
grid = [[Bool(f"cell_{i}_{j}") for j in range(N)] for i in range(N)]

# Pattern placement variables
r_b = Int('r_b')
c_b = Int('c_b')
r_boat = Int('r_boat')
c_boat = Int('c_boat')
r_loaf = Int('r_loaf')
c_loaf = Int('c_loaf')

solver = Solver()

# Bounds for pattern placements
solver.add(r_b >= 0, r_b <= 12, c_b >= 0, c_b <= 12)  # Block 2x2
solver.add(r_boat >= 0, r_boat <= 11, c_boat >= 0, c_boat <= 11)  # Boat 3x3
solver.add(r_loaf >= 0, r_loaf <= 10, c_loaf >= 0, c_loaf <= 10)  # Loaf 4x4

# Helper functions to check if a cell is in a pattern
def in_block(i, j):
    return Or(
        And(i == r_b, j == c_b),
        And(i == r_b, j == c_b + 1),
        And(i == r_b + 1, j == c_b),
        And(i == r_b + 1, j == c_b + 1)
    )

def in_boat(i, j):
    return Or(
        And(i == r_boat, j == c_boat),
        And(i == r_boat, j == c_boat + 1),
        And(i == r_boat + 1, j == c_boat),
        And(i == r_boat + 1, j == c_boat + 2),
        And(i == r_boat + 2, j == c_boat + 1)
    )

def in_loaf(i, j):
    return Or(
        And(i == r_loaf, j == c_loaf + 1),
        And(i == r_loaf, j == c_loaf + 2),
        And(i == r_loaf + 1, j == c_loaf),
        And(i == r_loaf + 1, j == c_loaf + 3),
        And(i == r_loaf + 2, j == c_loaf + 1),
        And(i == r_loaf + 2, j == c_loaf + 3),
        And(i == r_loaf + 3, j == c_loaf + 2)
    )

# Set grid cells based on pattern placements and ensure no overlap
for i in range(N):
    for j in range(N):
        block_expr = in_block(i, j)
        boat_expr = in_boat(i, j)
        loaf_expr = in_loaf(i, j)
        
        # Ensure at most one pattern claims this cell
        solver.add(Not(And(block_expr, boat_expr)))
        solver.add(Not(And(block_expr, loaf_expr)))
        solver.add(Not(And(boat_expr, loaf_expr)))
        
        # Grid cell is live if any pattern claims it
        solver.add(grid[i][j] == Or(block_expr, boat_expr, loaf_expr))

# Still life condition: neighbor counts
neighbors = [(-1, -1), (-1, 0), (-1, 1),
             (0, -1),           (0, 1),
             (1, -1),  (1, 0),  (1, 1)]

for i in range(N):
    for j in range(N):
        # Compute neighbor count
        count_exprs = []
        for di, dj in neighbors:
            ni, nj = i + di, j + dj
            if 0 <= ni < N and 0 <= nj < N:
                count_exprs.append(If(grid[ni][nj], 1, 0))
        count = Sum(count_exprs) if count_exprs else 0
        
        live = grid[i][j]
        # If live, count must be 2 or 3
        solver.add(Implies(live, Or(count == 2, count == 3)))
        # If dead, count must not be 3
        solver.add(Implies(Not(live), count != 3))

# Check satisfiability
result = solver.check()

if result == sat:
    model = solver.model()
    print("STATUS: sat")
    print("\nGrid (14x14):")
    for i in range(N):
        row = []
        for j in range(N):
            cell_val = model.evaluate(grid[i][j])
            row.append('1' if cell_val else '0')
        print(' '.join(row))
    
    print("\nPattern placements:")
    r_b_val = model.evaluate(r_b).as_long()
    c_b_val = model.evaluate(c_b).as_long()
    print(f"Block: top-left at ({r_b_val}, {c_b_val})")
    
    r_boat_val = model.evaluate(r_boat).as_long()
    c_boat_val = model.evaluate(c_boat).as_long()
    print(f"Boat: top-left at ({r_boat_val}, {c_boat_val})")
    
    r_loaf_val = model.evaluate(r_loaf).as_long()
    c_loaf_val = model.evaluate(c_loaf).as_long()
    print(f"Loaf: top-left at ({r_loaf_val}, {c_loaf_val})")
    
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")