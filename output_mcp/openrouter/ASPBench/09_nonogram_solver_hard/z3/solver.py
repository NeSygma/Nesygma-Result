from z3 import *

N = 24
# Grid variables
grid = [[Int(f'g_{r}_{c}') for c in range(N)] for r in range(N)]
solver = Solver()
# Domain constraints
for r in range(N):
    for c in range(N):
        solver.add(And(grid[r][c] >= 0, grid[r][c] <= 3))
# Diagonal constraints
main_diag = [1,1,0,0,0,0,0,0,3,3,3,3,3,3,3,3,0,0,0,0,0,0,1,1]
antidiag = [1,1,0,0,0,0,0,0,3,3,3,3,3,3,3,3,0,0,0,0,0,0,1,1]
for i in range(N):
    solver.add(grid[i][i] == main_diag[i])
    solver.add(grid[i][N-1-i] == antidiag[i])
# Row clues
row_clues = [
    [(1,10),(2,4),(1,10)],
    [(1,10),(2,4),(1,10)],
    [(1,2),(2,4),(1,2)],
    [(1,2),(2,4),(1,2)],
    [(1,2),(2,4),(1,2)],
    [(1,2),(2,4),(1,2)],
    [(1,2),(2,4),(1,2)],
    [(1,2),(2,4),(1,2)],
    [(1,2),(3,8),(1,2)],
    [(1,2),(3,8),(1,2)],
    [(1,2),(2,6),(3,8),(2,6),(1,2)],
    [(1,2),(2,6),(3,8),(2,6),(1,2)],
    [(1,2),(2,6),(3,8),(2,6),(1,2)],
    [(1,2),(2,6),(3,8),(2,6),(1,2)],
    [(1,2),(3,8),(1,2)],
    [(1,2),(3,8),(1,2)],
    [(1,2),(2,4),(1,2)],
    [(1,2),(2,4),(1,2)],
    [(1,2),(2,4),(1,2)],
    [(1,2),(2,4),(1,2)],
    [(1,2),(2,4),(1,2)],
    [(1,2),(2,4),(1,2)],
    [(1,10),(2,4),(1,10)],
    [(1,10),(2,4),(1,10)],
]
# Column clues
col_clues = [
    [(1,24)],
    [(1,24)],
    [(1,2),(2,4),(1,2)],
    [(1,2),(2,4),(1,2)],
    [(1,2),(2,4),(1,2)],
    [(1,2),(2,4),(1,2)],
    [(1,2),(2,4),(1,2)],
    [(1,2),(2,4),(1,2)],
    [(1,2),(3,8),(1,2)],
    [(1,2),(3,8),(1,2)],
    [(2,8),(3,8),(2,8)],
    [(2,8),(3,8),(2,8)],
    [(2,8),(3,8),(2,8)],
    [(2,8),(3,8),(2,8)],
    [(1,2),(3,8),(1,2)],
    [(1,2),(3,8),(1,2)],
    [(1,2),(2,4),(1,2)],
    [(1,2),(2,4),(1,2)],
    [(1,2),(2,4),(1,2)],
    [(1,2),(2,4),(1,2)],
    [(1,2),(2,4),(1,2)],
    [(1,2),(2,4),(1,2)],
    [(1,24)],
    [(1,24)],
]
# Row start variables and constraints
row_starts = []
for r in range(N):
    clues = row_clues[r]
    k = len(clues)
    starts = [Int(f'rs_{r}_{i}') for i in range(k)]
    row_starts.append(starts)
    # start bounds
    for i, (col, length) in enumerate(clues):
        s = starts[i]
        solver.add(s >= 0)
        solver.add(s + length - 1 < N)
        # enforce color for cells within the run via implication
        for c in range(N):
            in_run = And(s <= c, c < s + length)
            solver.add(Implies(in_run, grid[r][c] == col))
    # ordering with required gap if same color
    for i in range(k-1):
        col_i, len_i = clues[i]
        col_j, len_j = clues[i+1]
        gap = 1 if col_i == col_j else 0
        solver.add(starts[i] + len_i + gap <= starts[i+1])
    # cells not in any run must be white
    for c in range(N):
        in_any = Or([And(starts[i] <= c, c < starts[i] + clues[i][1]) for i in range(k)])
        solver.add(Implies(Not(in_any), grid[r][c] == 0))
# Column start variables and constraints
col_starts = []
for c in range(N):
    clues = col_clues[c]
    k = len(clues)
    starts = [Int(f'cs_{c}_{i}') for i in range(k)]
    col_starts.append(starts)
    for i, (col, length) in enumerate(clues):
        s = starts[i]
        solver.add(s >= 0)
        solver.add(s + length - 1 < N)
        for r in range(N):
            in_run = And(s <= r, r < s + length)
            solver.add(Implies(in_run, grid[r][c] == col))
    for i in range(k-1):
        col_i, len_i = clues[i]
        col_j, len_j = clues[i+1]
        gap = 1 if col_i == col_j else 0
        solver.add(starts[i] + len_i + gap <= starts[i+1])
    for r in range(N):
        in_any = Or([And(starts[i] <= r, r < starts[i] + clues[i][1]) for i in range(k)])
        solver.add(Implies(Not(in_any), grid[r][c] == 0))
# Solve
result = solver.check()
if result == sat:
    m = solver.model()
    print("STATUS: sat")
    for r in range(N):
        row_vals = [m.evaluate(grid[r][c]).as_long() for c in range(N)]
        print(' '.join(str(v) for v in row_vals))
elif result == unsat:
    print("STATUS: unsat")
else:
    print("STATUS: unknown")