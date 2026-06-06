from z3 import *

# Create solver
solver = Optimize()

# Board size
N = 8

# Queen variables
queen = [[Bool(f"q_{r}_{c}") for c in range(N)] for r in range(N)]

# Dominance constraints: each square must be dominated by at least one queen
for i in range(N):
    for j in range(N):
        dominating = []
        for r in range(N):
            for c in range(N):
                if r == i or c == j or abs(r - i) == abs(c - j):
                    dominating.append(queen[r][c])
        # At least one queen dominates (i,j)
        solver.add(Or(dominating))

# Objective: minimize number of queens
num_queens_expr = Sum([If(queen[r][c], 1, 0) for r in range(N) for c in range(N)])
solver.minimize(num_queens_expr)

# Solve
result = solver.check()

if result == sat:
    model = solver.model()
    # Extract queen positions
    positions = []
    for r in range(N):
        for c in range(N):
            if is_true(model[queen[r][c]]):
                positions.append((r, c))
    num_queens = len(positions)
    # Dominated squares: all squares (by construction)
    dominated = [(i, j) for i in range(N) for j in range(N)]
    # Output
    print("STATUS: sat")
    print(f"num_queens = {num_queens}")
    print("queens = [" + ", ".join(f"({r},{c})" for r,c in positions) + "]")
    print("dominated_squares = [" + ", ".join(f"({i},{j})" for i,j in dominated) + "]")
else:
    print("STATUS: unsat")
    if result == unknown:
        print("RAW_RESULT: unknown")