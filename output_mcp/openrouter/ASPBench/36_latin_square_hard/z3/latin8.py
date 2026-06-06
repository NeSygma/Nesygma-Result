from z3 import *

N = 8
solver = Solver()
# grid variables
grid = [[Int(f'g_{r}_{c}') for c in range(N)] for r in range(N)]
# domain constraints
for r in range(N):
    for c in range(N):
        solver.add(grid[r][c] >= 1, grid[r][c] <= N)
# Latin square rows and columns distinct
for r in range(N):
    solver.add(Distinct(grid[r]))
for c in range(N):
    col = [grid[r][c] for r in range(N)]
    solver.add(Distinct(col))
# prefilled cells (1-indexed in description)
prefilled = {
    (1,1):1,
    (1,8):8,
    (2,2):6,
    (3,3):4,
    (4,4):5,
    (5,5):7,
    (6,6):4,
    (7,7):6,
    (8,8):3,
    (8,1):8,
}
for (r,c), val in prefilled.items():
    solver.add(grid[r-1][c-1] == val)
# Adjacent horizontal sum >5
for r in range(N):
    for c in range(N-1):
        solver.add(grid[r][c] + grid[r][c+1] > 5)
# Quadrant parity
# top-left rows 0-3, cols 0-3: exactly 8 even numbers
even_cnt_tl = Sum([If(grid[r][c] % 2 == 0, 1, 0) for r in range(0,4) for c in range(0,4)])
solver.add(even_cnt_tl == 8)
# bottom-right rows 4-7, cols 4-7: exactly 8 odd numbers
odd_cnt_br = Sum([If(grid[r][c] % 2 == 1, 1, 0) for r in range(4,8) for c in range(4,8)])
solver.add(odd_cnt_br == 8)
# Partial sums
row1_sum = Sum([grid[0][c] for c in range(0,4)])
solver.add(row1_sum == 14)
col1_sum = Sum([grid[r][0] for r in range(0,4)])
solver.add(col1_sum == 10)

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