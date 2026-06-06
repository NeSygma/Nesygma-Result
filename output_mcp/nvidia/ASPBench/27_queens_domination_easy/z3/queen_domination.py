from z3 import *

# Create boolean variables for each square
queen = [[Bool(f'q_{r}_{c}') for c in range(8)] for r in range(8)]

opt = Optimize()

# For each square (i,j), ensure it is dominated by at least one queen
for i in range(8):
    for j in range(8):
        dominators = []
        for r in range(8):
            for c in range(8):
                if r == i or c == j or abs(r - i) == abs(c - j):
                    dominators.append(If(queen[r][c], 1, 0))
        opt.add(Sum(dominators) >= 1)

# Objective: minimize total number of queens
total_queens = Sum([If(queen[r][c], 1, 0) for r in range(8) for c in range(8)])
opt.minimize(total_queens)

# Solve
result = opt.check()
if result == sat:
    model = opt.model()
    print("STATUS: sat")
    # Collect positions of queens
    placed = []
    for r in range(8):
        for c in range(8):
            if model[queen[r][c]] == True:
                placed.append([r, c])
    print(f"num_queens = {len(placed)}")
    print(f"queens = {placed}")
else:
    print("STATUS: unsat")