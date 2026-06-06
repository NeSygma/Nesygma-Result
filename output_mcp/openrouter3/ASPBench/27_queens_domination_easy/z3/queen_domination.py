from z3 import *

# Board dimensions
N = 8

# Create solver with optimization
opt = Optimize()

# Boolean variables: queen[i][j] = True if there's a queen at (i,j)
queen = [[Bool(f"q_{i}_{j}") for j in range(N)] for i in range(N)]

# For each square (r,c), it must be dominated by at least one queen
for r in range(N):
    for c in range(N):
        # List of all queens that dominate square (r,c)
        dominators = []
        for i in range(N):
            for j in range(N):
                # Queen at (i,j) dominates (r,c) if:
                # 1. Same row: i == r
                # 2. Same column: j == c  
                # 3. Same diagonal: |i-r| == |j-c|
                # 4. Same square: i == r and j == c
                if i == r or j == c or abs(i - r) == abs(j - c):
                    dominators.append(queen[i][j])
        
        # At least one dominator must be True
        opt.add(Or(dominators))

# Objective: minimize total number of queens
total_queens = Sum([If(queen[i][j], 1, 0) for i in range(N) for j in range(N)])
opt.minimize(total_queens)

# Check and print results
BENCHMARK_MODE = True
result = opt.check()

if result == sat:
    model = opt.model()
    print("STATUS: sat")
    
    # Extract queen positions
    queen_positions = []
    for i in range(N):
        for j in range(N):
            if is_true(model[queen[i][j]]):
                queen_positions.append((i, j))
    
    num_queens = len(queen_positions)
    print(f"num_queens = {num_queens}")
    print(f"queens = {queen_positions}")
    
    # Verify all squares are dominated
    dominated = set()
    for (r, c) in queen_positions:
        for i in range(N):
            for j in range(N):
                if i == r or j == c or abs(i - r) == abs(j - c):
                    dominated.add((i, j))
    
    print(f"dominated_squares count = {len(dominated)}")
    print(f"All 64 squares dominated: {len(dominated) == 64}")
    
    # Print dominated squares (all 64)
    dominated_list = sorted(list(dominated))
    print(f"dominated_squares = {dominated_list}")
    
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")