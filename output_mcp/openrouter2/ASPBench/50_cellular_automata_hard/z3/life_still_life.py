from z3 import *

solver = Solver()

# Grid variables
grid = [[Int(f'cell_{i}_{j}') for j in range(14)] for i in range(14)]

# Pattern top-left coordinates
r_b = Int('r_b'); c_b = Int('c_b')
r_bo = Int('r_bo'); c_bo = Int('c_bo')
r_l = Int('r_l'); c_l = Int('c_l')

# Bounds for pattern placement
solver.add(r_b >= 0, r_b <= 12)
solver.add(c_b >= 0, c_b <= 12)
solver.add(r_bo >= 0, r_bo <= 11)
solver.add(c_bo >= 0, c_bo <= 11)
solver.add(r_l >= 0, r_l <= 10)
solver.add(c_l >= 0, c_l <= 10)

# Helper functions to check if a cell belongs to a pattern
def block_cell(i, j):
    return Or(And(i == r_b, j == c_b),
              And(i == r_b, j == c_b + 1),
              And(i == r_b + 1, j == c_b),
              And(i == r_b + 1, j == c_b + 1))

def boat_cell(i, j):
    return Or(And(i == r_bo, j == c_bo),
              And(i == r_bo, j == c_bo + 1),
              And(i == r_bo + 1, j == c_bo),
              And(i == r_bo + 1, j == c_bo + 2),
              And(i == r_bo + 2, j == c_bo + 1))

def loaf_cell(i, j):
    return Or(And(i == r_l, j == c_l + 1),
              And(i == r_l, j == c_l + 2),
              And(i == r_l + 1, j == c_l),
              And(i == r_l + 1, j == c_l + 3),
              And(i == r_l + 2, j == c_l + 1),
              And(i == r_l + 2, j == c_l + 3),
              And(i == r_l + 3, j == c_l + 2))

# Grid cell constraints
for i in range(14):
    for j in range(14):
        bc = block_cell(i, j)
        bo = boat_cell(i, j)
        lo = loaf_cell(i, j)
        # No overlapping
        solver.add(Sum([If(bc, 1, 0), If(bo, 1, 0), If(lo, 1, 0)]) <= 1)
        # Grid value equals 1 if covered by any pattern
        solver.add(grid[i][j] == If(Or(bc, bo, lo), 1, 0))
        # Domain
        solver.add(grid[i][j] >= 0, grid[i][j] <= 1)

# Still life constraints
for i in range(14):
    for j in range(14):
        neigh = []
        for di in [-1, 0, 1]:
            for dj in [-1, 0, 1]:
                if di == 0 and dj == 0:
                    continue
                ni, nj = i + di, j + dj
                if 0 <= ni < 14 and 0 <= nj < 14:
                    neigh.append(grid[ni][nj])
        neigh_sum = Sum(neigh)
        solver.add(Implies(grid[i][j] == 1, Or(neigh_sum == 2, neigh_sum == 3)))
        solver.add(Implies(grid[i][j] == 0, neigh_sum != 3))

# Solve
BENCHMARK_MODE = True
result = solver.check()

if result == sat:
    m = solver.model()
    print("STATUS: sat")
    for i in range(14):
        row = ""
        for j in range(14):
            val = m.evaluate(grid[i][j], model_completion=True)
            row += str(val.as_long())
        print(row)
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")