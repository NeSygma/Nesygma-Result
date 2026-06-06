from z3 import *

# Board dimensions
N = 8

# Bool variables: q[r][c] true if a queen is placed at (r,c)
q = [[Bool(f"q_{r}_{c}") for c in range(N)] for r in range(N)]

opt = Optimize()

# Constraint: every square (i,j) must be dominated by at least one queen
for i in range(N):
    for j in range(N):
        dominates = []
        for r in range(N):
            for c in range(N):
                # queen at (r,c) dominates (i,j) if same row, column, or diagonal
                same_row = (r == i)
                same_col = (c == j)
                same_diag1 = (r - c == i - j)
                same_diag2 = (r + c == i + j)
                if same_row or same_col or same_diag1 or same_diag2:
                    dominates.append(q[r][c])
        # At least one queen dominates this square
        opt.add(Or(dominates))

# Objective: minimize total number of queens
total_queens = Sum([If(q[r][c], 1, 0) for r in range(N) for c in range(N)])
opt.minimize(total_queens)

# Solve
result = opt.check()
if result == sat:
    m = opt.model()
    # Extract queen positions
    queen_positions = []
    for r in range(N):
        for c in range(N):
            if is_true(m.eval(q[r][c])):
                queen_positions.append((r, c))
    num = len(queen_positions)
    print("STATUS: sat")
    print(f"num_queens = {num}")
    for (r, c) in queen_positions:
        print(f"queen: {r} {c}")
else:
    if result == unsat:
        print("STATUS: unsat")
    else:
        print("STATUS: unknown")