from z3 import *

# Problem: Find minimum queens to dominate 9x9 board
# Board size: 9x9 (rows 0-8, columns 0-8)

# Create solver
solver = Optimize()

# Maximum possible queens (we'll minimize from this)
MAX_QUEENS = 9  # Upper bound

# Decision variables: queen positions
# We'll use a fixed number of potential queen positions and decide which are active
queen_active = [Bool(f'q_active_{i}') for i in range(MAX_QUEENS)]
queen_row = [Int(f'q_row_{i}') for i in range(MAX_QUEENS)]
queen_col = [Int(f'q_col_{i}') for i in range(MAX_QUEENS)]

# Add constraints for queen positions (only valid if active)
for i in range(MAX_QUEENS):
    # If queen is active, row and column must be in range 0-8
    solver.add(If(queen_active[i], And(queen_row[i] >= 0, queen_row[i] <= 8, 
                                       queen_col[i] >= 0, queen_col[i] <= 8), True))
    # If queen is not active, we don't care about its position (but we'll ensure it doesn't dominate)
    # We'll handle this by only considering active queens in domination constraints

# Domination constraints: every square must be dominated by at least one queen
for row in range(9):
    for col in range(9):
        # A square is dominated if there exists an active queen that dominates it
        dominated = False
        for i in range(MAX_QUEENS):
            # Queen i dominates square (row, col) if:
            # 1. Queen i is active AND
            # 2. Same row OR same column OR same diagonal
            same_row = queen_row[i] == row
            same_col = queen_col[i] == col
            same_diag1 = queen_row[i] - queen_col[i] == row - col  # main diagonal
            same_diag2 = queen_row[i] + queen_col[i] == row + col  # anti diagonal
            
            queen_dominates = And(queen_active[i], 
                                 Or(same_row, same_col, same_diag1, same_diag2))
            
            if not dominated:
                dominated = queen_dominates
            else:
                dominated = Or(dominated, queen_dominates)
        
        # Each square must be dominated by at least one queen
        solver.add(dominated)

# Objective: minimize the number of active queens
num_queens = Sum([If(queen_active[i], 1, 0) for i in range(MAX_QUEENS)])
solver.minimize(num_queens)

# Check and print results
BENCHMARK_MODE = True
result = solver.check()

if result == sat:
    model = solver.model()
    print("STATUS: sat")
    
    # Count active queens and collect their positions
    active_queens = []
    for i in range(MAX_QUEENS):
        if is_true(model[queen_active[i]]):
            row_val = model[queen_row[i]]
            col_val = model[queen_col[i]]
            active_queens.append((int(row_val), int(col_val)))
    
    print(f"Minimum queens needed: {len(active_queens)}")
    print("Queen positions (row, col):")
    for pos in active_queens:
        print(f"  {pos}")
    
    # Verify all squares are dominated
    print("\nVerification:")
    all_dominated = True
    for row in range(9):
        for col in range(9):
            dominated = False
            for (q_row, q_col) in active_queens:
                if (q_row == row or q_col == col or 
                    q_row - q_col == row - col or 
                    q_row + q_col == row + col):
                    dominated = True
                    break
            if not dominated:
                print(f"  Square ({row}, {col}) NOT dominated!")
                all_dominated = False
    
    if all_dominated:
        print("  All squares are dominated ✓")
    
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")