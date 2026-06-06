from z3 import *

# BENCHMARK_MODE: ON (since the problem is guaranteed solvable)
BENCHMARK_MODE = True

# Create an optimizer
opt = Optimize()

# Board size
N = 8

# Declare boolean variables for queen placement: is_queen[r][c]
is_queen = [[Bool(f"queen_{r}_{c}") for c in range(N)] for r in range(N)]

# Declare boolean variables for dominated squares: is_dominated[r][c]
is_dominated = [[Bool(f"dominated_{r}_{c}") for c in range(N)] for r in range(N)]

# Flatten the is_queen variables for summation
queen_vars = [is_queen[r][c] for r in range(N) for c in range(N)]

# Objective: minimize the number of queens
opt.minimize(Sum(queen_vars))

# Constraints:
# 1. For each square (r, c), it must be dominated by at least one queen
for r in range(N):
    for c in range(N):
        # A square (r, c) is dominated if:
        # - There is a queen in the same row, or
        # - There is a queen in the same column, or
        # - There is a queen on the same diagonal (top-left to bottom-right), or
        # - There is a queen on the same diagonal (top-right to bottom-left)
        dominated_by_queen = Or(
            Or([is_queen[r][qc] for qc in range(N)]),  # same row
            Or([is_queen[qr][c] for qr in range(N)]),  # same column
            Or([is_queen[qr][qc] for qr, qc in zip(range(r, N), range(c, N))] +  # diagonal 1 (top-left to bottom-right)
               [is_queen[qr][qc] for qr, qc in zip(range(r, -1, -1), range(c, -1, -1))][1:]),  # diagonal 1 (top-right to bottom-left)
            Or([is_queen[qr][qc] for qr, qc in zip(range(r, N), range(c, -1, -1))] +  # diagonal 2 (top-right to bottom-left)
               [is_queen[qr][qc] for qr, qc in zip(range(r, -1, -1), range(c, N))][1:])   # diagonal 2 (top-left to bottom-right)
        )
        opt.add(is_dominated[r][c] == dominated_by_queen)

# Every square must be dominated
for r in range(N):
    for c in range(N):
        opt.add(is_dominated[r][c])

# Check and print result
result = opt.check()

if result == sat:
    model = opt.model()
    # Extract the number of queens and their positions
    num_queens = sum(1 for r in range(N) for c in range(N) if model[is_queen[r][c]] == True)
    queens_positions = [(r, c) for r in range(N) for c in range(N) if model[is_queen[r][c]] == True]
    dominated_squares = [(r, c) for r in range(N) for c in range(N) if model[is_dominated[r][c]] == True]

    print("STATUS: sat")
    print(f"num_queens = {num_queens}")
    print("queens =", queens_positions)
    print("dominated_squares =", dominated_squares)
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")