from z3 import *

# ---------- Problem Setup ----------
BENCHMARK_MODE = True  # Problem is guaranteed solvable

# Create a 9x9 board of Boolean variables: True if a queen is placed there
queen = [[Bool(f'q_{r}_{c}') for c in range(9)] for r in range(9)]

solver = Optimize()

# ---------- Domination Constraints ----------
# For each square (r,c), at least one queen must dominate it
for r in range(9):
    for c in range(9):
        dominators = []
        # Same row
        for cc in range(9):
            dominators.append(queen[r][cc])
        # Same column
        for rr in range(9):
            dominators.append(queen[rr][c])
        # Diagonal: up-left
        i, j = r-1, c-1
        while i >= 0 and j >= 0:
            dominators.append(queen[i][j])
            i -= 1; j -= 1
        # Diagonal: up-right
        i, j = r-1, c+1
        while i >= 0 and j < 9:
            dominators.append(queen[i][j])
            i -= 1; j += 1
        # Diagonal: down-left
        i, j = r+1, c-1
        while i < 9 and j >= 0:
            dominators.append(queen[i][j])
            i += 1; j -= 1
        # Diagonal: down-right
        i, j = r+1, c+1
        while i < 9 and j < 9:
            dominators.append(queen[i][j])
            i += 1; j += 1
        
        # At least one dominator must be True
        solver.add(Sum(dominators) >= 1)

# ---------- Objective: Minimize number of queens ----------
total_queens = Sum([queen[r][c] for r in range(9) for c in range(9)])
solver.minimize(total_queens)

# ---------- Solve ----------
result = solver.check()
if result == sat:
    model = solver.model()
    print("STATUS: sat")
    # Objective value
    opt_val = model.evaluate(total_queens)
    print(f"min_queens = {opt_val}")
    # Collect positions of queens in the optimal model
    positions = []
    for r in range(9):
        for c in range(9):
            if model.evaluate(queen[r][c]) == True:
                positions.append(f"[{r},{c}]")
    print("positions =", positions)
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")