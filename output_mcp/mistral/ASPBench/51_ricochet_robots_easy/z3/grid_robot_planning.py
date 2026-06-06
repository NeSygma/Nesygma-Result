from z3 import *

# BENCHMARK_MODE: ON (problem is guaranteed solvable)
BENCHMARK_MODE = True

# ====== PROBLEM SETUP ======
# Grid: 4x4 (rows 0-3, cols 0-3)
# Robots: A starts at (0,1), B starts at (1,1)
# Target: A must reach (2,1)
# Walls: Column 2 right side, rows 0-1 (cannot move from col 1 to col 2 in rows 0-1)

# ====== PLANNING HORIZON ======
# We will search for a solution with horizon up to 6 moves (expected min is 3)
MAX_HORIZON = 6

# ====== DECISION VARIABLES ======
# For each time step t in [0, MAX_HORIZON], we track:
# - rowA[t], colA[t] = position of Robot A
# - rowB[t], colB[t] = position of Robot B
# - move_robot[t] = which robot moves at step t (0 = none, 1 = A, 2 = B)

rowA = [Int(f'rowA_{t}') for t in range(MAX_HORIZON + 1)]
colA = [Int(f'colA_{t}') for t in range(MAX_HORIZON + 1)]
rowB = [Int(f'rowB_{t}') for t in range(MAX_HORIZON + 1)]
colB = [Int(f'colB_{t}') for t in range(MAX_HORIZON + 1)]

# Move decision variables: 0 = no move, 1 = A moves, 2 = B moves
move_robot = [Int(f'move_robot_{t}') for t in range(MAX_HORIZON)]

# For each move, we track from/to positions
move_fromA_row = [Int(f'move_fromA_row_{t}') for t in range(MAX_HORIZON)]
move_fromA_col = [Int(f'move_fromA_col_{t}') for t in range(MAX_HORIZON)]
move_toA_row = [Int(f'move_toA_row_{t}') for t in range(MAX_HORIZON)]
move_toA_col = [Int(f'move_toA_col_{t}') for t in range(MAX_HORIZON)]

move_fromB_row = [Int(f'move_fromB_row_{t}') for t in range(MAX_HORIZON)]
move_fromB_col = [Int(f'move_fromB_col_{t}') for t in range(MAX_HORIZON)]
move_toB_row = [Int(f'move_toB_row_{t}') for t in range(MAX_HORIZON)]
move_toB_col = [Int(f'move_toB_col_{t}') for t in range(MAX_HORIZON)]

# ====== SOLVER SETUP ======
opt = Optimize()

# ====== INITIAL STATE ======
# At t=0, A is at (0,1), B is at (1,1)
opt.add(rowA[0] == 0, colA[0] == 1)
opt.add(rowB[0] == 1, colB[0] == 1)

# ====== GOAL STATE ======
# At t=horizon, A must be at (2,1)

# ====== CONSTRAINTS ======
# For each time step t from 0 to MAX_HORIZON-1:
for t in range(MAX_HORIZON):
    # Only one robot can move at a time (or none)
    opt.add(move_robot[t] >= 0, move_robot[t] <= 2)
    
    # If A moves at t, then its position changes from move_fromA to move_toA
    opt.add(Implies(move_robot[t] == 1,
                   And(move_fromA_row[t] == rowA[t], move_fromA_col[t] == colA[t],
                       move_toA_row[t] == rowA[t+1], move_toA_col[t] == colA[t+1])))
    
    # If B moves at t, then its position changes from move_fromB to move_toB
    opt.add(Implies(move_robot[t] == 2,
                   And(move_fromB_row[t] == rowB[t], move_fromB_col[t] == colB[t],
                       move_toB_row[t] == rowB[t+1], move_toB_col[t] == colB[t+1])))
    
    # If no robot moves, positions stay the same
    opt.add(Implies(move_robot[t] == 0,
                   And(rowA[t+1] == rowA[t], colA[t+1] == colA[t],
                       rowB[t+1] == rowB[t], colB[t+1] == colB[t])))
    
    # Movement is exactly one step in a cardinal direction
    # For A
    opt.add(Implies(move_robot[t] == 1,
                   Or(
                       # Up
                       And(move_toA_row[t] == move_fromA_row[t] - 1, move_toA_col[t] == move_fromA_col[t]),
                       # Down
                       And(move_toA_row[t] == move_fromA_row[t] + 1, move_toA_col[t] == move_fromA_col[t]),
                       # Left
                       And(move_toA_row[t] == move_fromA_row[t], move_toA_col[t] == move_fromA_col[t] - 1),
                       # Right
                       And(move_toA_row[t] == move_fromA_row[t], move_toA_col[t] == move_fromA_col[t] + 1)
                   )))
    
    # For B
    opt.add(Implies(move_robot[t] == 2,
                   Or(
                       # Up
                       And(move_toB_row[t] == move_fromB_row[t] - 1, move_toB_col[t] == move_fromB_col[t]),
                       # Down
                       And(move_toB_row[t] == move_fromB_row[t] + 1, move_toB_col[t] == move_fromB_col[t]),
                       # Left
                       And(move_toB_row[t] == move_fromB_row[t], move_toB_col[t] == move_fromB_col[t] - 1),
                       # Right
                       And(move_toB_row[t] == move_fromB_row[t], move_toB_col[t] == move_fromB_col[t] + 1)
                   )))
    
    # No collisions: A and B cannot be at the same position at the same time
    opt.add(Not(And(rowA[t] == rowB[t], colA[t] == colB[t])))
    opt.add(Not(And(rowA[t+1] == rowB[t+1], colA[t+1] == colB[t+1])))
    
    # Wall blocking: Cannot move from (r,1) to (r,2) for r in {0,1}
    for r in [0, 1]:
        opt.add(Implies(And(move_robot[t] == 1,
                           move_fromA_row[t] == r, move_fromA_col[t] == 1,
                           move_toA_col[t] == 2),
                       False))
        opt.add(Implies(And(move_robot[t] == 2,
                           move_fromB_row[t] == r, move_fromB_col[t] == 1,
                           move_toB_col[t] == 2),
                       False))
    
    # Valid positions: must stay within grid bounds (0-3 for both row and column)
    opt.add(rowA[t] >= 0, rowA[t] <= 3, colA[t] >= 0, colA[t] <= 3)
    opt.add(rowB[t] >= 0, rowB[t] <= 3, colB[t] >= 0, colB[t] <= 3)
    opt.add(rowA[t+1] >= 0, rowA[t+1] <= 3, colA[t+1] >= 0, colA[t+1] <= 3)
    opt.add(rowB[t+1] >= 0, rowB[t+1] <= 3, colB[t+1] >= 0, colB[t+1] <= 3)

# ====== GOAL: A must be at (2,1) at the horizon ======
# We will try each horizon from 1 to MAX_HORIZON
solution_found = False
moves = -1
sequence = []
final_positions = {}

for horizon in range(1, MAX_HORIZON + 1):
    opt.push()
    opt.add(rowA[horizon] == 2, colA[horizon] == 1)
    
    # Check if a solution exists for this horizon
    result = opt.check()
    
    if result == sat:
        solution_found = True
        moves = horizon
        m = opt.model()
        
        # Extract final positions
        final_positions = {
            'A': [m.eval(rowA[horizon]).as_long(), m.eval(colA[horizon]).as_long()],
            'B': [m.eval(rowB[horizon]).as_long(), m.eval(colB[horizon]).as_long()]
        }
        
        # Extract move sequence
        sequence = []
        for t in range(horizon):
            robot = m.eval(move_robot[t]).as_long()
            if robot == 1:  # A moves
                from_pos = [m.eval(move_fromA_row[t]).as_long(), m.eval(move_fromA_col[t]).as_long()]
                to_pos = [m.eval(move_toA_row[t]).as_long(), m.eval(move_toA_col[t]).as_long()]
                sequence.append({'robot': 'A', 'from': from_pos, 'to': to_pos})
            elif robot == 2:  # B moves
                from_pos = [m.eval(move_fromB_row[t]).as_long(), m.eval(move_fromB_col[t]).as_long()]
                to_pos = [m.eval(move_toB_row[t]).as_long(), m.eval(move_toB_col[t]).as_long()]
                sequence.append({'robot': 'B', 'from': from_pos, 'to': to_pos})
            # else: no move
        
        # We found the minimal horizon, so break
        opt.pop()
        break
    else:
        opt.pop()

# ====== OUTPUT ======
if solution_found:
    print("STATUS: sat")
    print(f"solution_found = True")
    print(f"moves = {moves}")
    print(f"sequence = {sequence}")
    print(f"final_positions = {final_positions}")
else:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")