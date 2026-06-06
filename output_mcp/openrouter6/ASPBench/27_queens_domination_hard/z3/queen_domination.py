from z3 import *

# Board size
N = 9

# Create boolean variables for queen placement (0/1 integers)
Q = [[Int(f'Q_{i}_{j}') for j in range(N)] for i in range(N)]

solver = Optimize()

# Add domain constraints: each Q[i][j] is 0 or 1
for i in range(N):
    for j in range(N):
        solver.add(Q[i][j] >= 0)
        solver.add(Q[i][j] <= 1)

# Domination constraints: for each square (r,c), at least one queen dominates it
for r in range(N):
    for c in range(N):
        # Sum of queens that dominate square (r,c)
        domination_sum = 0
        for i in range(N):
            for j in range(N):
                # Check if queen at (i,j) dominates (r,c)
                same_row = (i == r)
                same_col = (j == c)
                same_main_diag = (i - j == r - c)
                same_anti_diag = (i + j == r + c)
                if same_row or same_col or same_main_diag or same_anti_diag:
                    domination_sum += Q[i][j]
        # At least one queen must dominate this square
        solver.add(domination_sum >= 1)

# Objective: minimize total number of queens
total_queens = Sum([Q[i][j] for i in range(N) for j in range(N)])
solver.minimize(total_queens)

# Check
BENCHMARK_MODE = True
result = solver.check()

if result == sat:
    model = solver.model()
    print("STATUS: sat")
    
    # Extract queen positions
    queens = []
    for i in range(N):
        for j in range(N):
            if model.evaluate(Q[i][j]) == 1:
                queens.append([i, j])
    
    print(f"Minimum queens: {len(queens)}")
    print("Queen positions (row, col):")
    for pos in queens:
        print(f"  {pos}")
    
    # Verify domination (optional check)
    print("\nVerification:")
    all_dominated = True
    for r in range(N):
        for c in range(N):
            dominated = False
            for (qi, qj) in queens:
                if qi == r or qj == c or (qi - qj == r - c) or (qi + qj == r + c):
                    dominated = True
                    break
            if not dominated:
                print(f"Square ({r},{c}) NOT dominated!")
                all_dominated = False
    if all_dominated:
        print("All squares dominated ✓")
    
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")