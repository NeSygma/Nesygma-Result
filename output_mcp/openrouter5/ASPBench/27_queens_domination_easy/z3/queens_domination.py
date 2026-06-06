from z3 import *

# We'll use optimization to find the minimum number of queens.
# Board is 8x8, rows 0-7, cols 0-7.
# We'll use a grid of Bool variables: queen[r][c] = True if a queen is placed there.
# Then we add constraints that every square is dominated by at least one queen.
# Then minimize the total number of queens.

opt = Optimize()

# Decision variables
queen = [[Bool(f"q_{r}_{c}") for c in range(8)] for r in range(8)]

# For each square (r, c), it must be dominated by at least one queen.
# A queen at (qr, qc) dominates (r, c) if:
#   qr == r (same row) OR qc == c (same col) OR
#   qr - qc == r - c (same main diag) OR qr + qc == r + c (same anti diag)
# So for each (r,c), we need: Or over all (qr,qc) of (queen[qr][qc] AND condition)

for r in range(8):
    for c in range(8):
        # Build list of (qr, qc) that dominate (r,c)
        dominating_queens = []
        for qr in range(8):
            for qc in range(8):
                if (qr == r) or (qc == c) or (qr - qc == r - c) or (qr + qc == r + c):
                    dominating_queens.append(queen[qr][qc])
        # At least one of these must be True
        opt.add(Or(dominating_queens))

# Objective: minimize total number of queens
total_queens = Sum([If(queen[r][c], 1, 0) for r in range(8) for c in range(8)])
opt.minimize(total_queens)

# Solve
result = opt.check()

if result == sat:
    m = opt.model()
    num_q = sum([1 if is_true(m[queen[r][c]]) else 0 for r in range(8) for c in range(8)])
    print("STATUS: sat")
    print(f"num_queens = {num_q}")
    queens_positions = []
    for r in range(8):
        for c in range(8):
            if is_true(m[queen[r][c]]):
                queens_positions.append((r, c))
    print(f"queens = {queens_positions}")
    # Verify domination
    dominated = set()
    for (qr, qc) in queens_positions:
        for r in range(8):
            for c in range(8):
                if (qr == r) or (qc == c) or (qr - qc == r - c) or (qr + qc == r + c):
                    dominated.add((r, c))
    print(f"dominated_squares count = {len(dominated)}")
    print(f"dominated_squares = {sorted(dominated)}")
elif result == unsat:
    print("STATUS: unsat")
else:
    print("STATUS: unknown")