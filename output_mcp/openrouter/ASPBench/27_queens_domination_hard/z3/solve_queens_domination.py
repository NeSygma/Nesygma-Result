from z3 import *

# Board dimensions
N = 9

# Boolean variables: q[i][j] true if a queen is placed at (i,j)
q = [[Bool(f'q_{i}_{j}') for j in range(N)] for i in range(N)]

opt = Optimize()

# Objective: minimize total number of queens
total = Sum([If(q[i][j], 1, 0) for i in range(N) for j in range(N)])
opt.minimize(total)

# Domination constraints: each square must be dominated by at least one queen
for r in range(N):
    for c in range(N):
        # collect all queens that dominate (r,c)
        dominators = []
        for i in range(N):
            for j in range(N):
                if i == r or j == c or (i - j) == (r - c) or (i + j) == (r + c):
                    dominators.append(q[i][j])
        opt.add(Or(dominators))

# No other constraints (queens may attack each other)

result = opt.check()
if result == sat:
    m = opt.model()
    # Extract queen positions
    positions = []
    for i in range(N):
        for j in range(N):
            if is_true(m.eval(q[i][j])):
                positions.append((i, j))
    print("STATUS: sat")
    print("num_queens =", len(positions))
    for (i, j) in positions:
        print(f"queen = ({i}, {j})")
else:
    print("STATUS: unsat" if result == unsat else "STATUS: unknown")