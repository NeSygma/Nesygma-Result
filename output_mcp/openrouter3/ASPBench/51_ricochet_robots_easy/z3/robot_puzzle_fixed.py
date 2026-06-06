from z3 import *

# Problem parameters
GRID_SIZE = 4
MAX_MOVES = 10  # Upper bound for planning horizon

# Wall positions (blocked cells)
WALLS = [(0, 2), (1, 2)]  # Vertical barrier at column 2, rows 0-1

# Start and target positions
START_A = (0, 1)
START_B = (1, 1)
TARGET_A = (2, 1)

# Create solver
solver = Solver()

# State variables: position of each robot at each time step
# Time steps: 0 to MAX_MOVES (inclusive)
pos_A_row = [Int(f'pos_A_row_{t}') for t in range(MAX_MOVES + 1)]
pos_A_col = [Int(f'pos_A_col_{t}') for t in range(MAX_MOVES + 1)]
pos_B_row = [Int(f'pos_B_row_{t}') for t in range(MAX_MOVES + 1)]
pos_B_col = [Int(f'pos_B_col_{t}') for t in range(MAX_MOVES + 1)]

# Move variables: which robot moves at each step (0 = none, 1 = A, 2 = B)
move_robot = [Int(f'move_robot_{t}') for t in range(MAX_MOVES)]

# Direction variables for each move (0-3: up, down, left, right)
move_dir = [Int(f'move_dir_{t}') for t in range(MAX_MOVES)]

# Initial positions
solver.add(pos_A_row[0] == START_A[0])
solver.add(pos_A_col[0] == START_A[1])
solver.add(pos_B_row[0] == START_B[0])
solver.add(pos_B_col[0] == START_B[1])

# Grid bounds constraints for all positions
for t in range(MAX_MOVES + 1):
    solver.add(pos_A_row[t] >= 0, pos_A_row[t] < GRID_SIZE)
    solver.add(pos_A_col[t] >= 0, pos_A_col[t] < GRID_SIZE)
    solver.add(pos_B_row[t] >= 0, pos_B_row[t] < GRID_SIZE)
    solver.add(pos_B_col[t] >= 0, pos_B_col[t] < GRID_SIZE)

# Wall constraints: robots cannot be in wall positions
for t in range(MAX_MOVES + 1):
    for wall in WALLS:
        # Use Z3 Or instead of Python or
        solver.add(Or(
            pos_A_row[t] != wall[0],
            pos_A_col[t] != wall[1]
        ))
        solver.add(Or(
            pos_B_row[t] != wall[0],
            pos_B_col[t] != wall[1]
        ))

# No collision constraint: robots cannot be in same cell at same time
for t in range(MAX_MOVES + 1):
    solver.add(Or(
        pos_A_row[t] != pos_B_row[t],
        pos_A_col[t] != pos_B_col[t]
    ))

# Movement constraints for each time step
for t in range(MAX_MOVES):
    # Default: positions stay the same (no move)
    solver.add(pos_A_row[t+1] == pos_A_row[t])
    solver.add(pos_A_col[t+1] == pos_A_col[t])
    solver.add(pos_B_row[t+1] == pos_B_row[t])
    solver.add(pos_B_col[t+1] == pos_B_col[t])
    
    # If robot A moves at step t
    solver.add(Implies(
        move_robot[t] == 1,
        And(
            # Move exactly one step in cardinal direction
            Or(
                # Up
                And(pos_A_row[t+1] == pos_A_row[t] - 1, pos_A_col[t+1] == pos_A_col[t]),
                # Down
                And(pos_A_row[t+1] == pos_A_row[t] + 1, pos_A_col[t+1] == pos_A_col[t]),
                # Left
                And(pos_A_row[t+1] == pos_A_row[t], pos_A_col[t+1] == pos_A_col[t] - 1),
                # Right
                And(pos_A_row[t+1] == pos_A_row[t], pos_A_col[t+1] == pos_A_col[t] + 1)
            ),
            # B stays in place
            pos_B_row[t+1] == pos_B_row[t],
            pos_B_col[t+1] == pos_B_col[t]
        )
    ))
    
    # If robot B moves at step t
    solver.add(Implies(
        move_robot[t] == 2,
        And(
            # Move exactly one step in cardinal direction
            Or(
                # Up
                And(pos_B_row[t+1] == pos_B_row[t] - 1, pos_B_col[t+1] == pos_B_col[t]),
                # Down
                And(pos_B_row[t+1] == pos_B_row[t] + 1, pos_B_col[t+1] == pos_B_col[t]),
                # Left
                And(pos_B_row[t+1] == pos_B_row[t], pos_B_col[t+1] == pos_B_col[t] - 1),
                # Right
                And(pos_B_row[t+1] == pos_B_row[t], pos_B_col[t+1] == pos_B_col[t] + 1)
            ),
            # A stays in place
            pos_A_row[t+1] == pos_A_row[t],
            pos_A_col[t+1] == pos_A_col[t]
        )
    ))
    
    # If no robot moves at step t (move_robot[t] == 0)
    solver.add(Implies(
        move_robot[t] == 0,
        And(
            pos_A_row[t+1] == pos_A_row[t],
            pos_A_col[t+1] == pos_A_col[t],
            pos_B_row[t+1] == pos_B_row[t],
            pos_B_col[t+1] == pos_B_col[t]
        )
    ))
    
    # Move robot must be 0, 1, or 2
    solver.add(Or(
        move_robot[t] == 0,
        move_robot[t] == 1,
        move_robot[t] == 2
    ))

# Goal: Robot A must reach target position (2, 1) at some time step
# We'll check at the final time step
solver.add(pos_A_row[MAX_MOVES] == TARGET_A[0])
solver.add(pos_A_col[MAX_MOVES] == TARGET_A[1])

# Optimization: minimize the number of moves (non-zero move_robot entries)
# We'll use a soft constraint approach by checking different move counts
# First, let's find the minimum number of moves

print("Searching for minimum moves solution...")

# Try different move counts from 0 to MAX_MOVES
for num_moves in range(MAX_MOVES + 1):
    solver.push()
    
    # Add constraint that exactly num_moves are non-zero
    move_count = Sum([If(move_robot[t] != 0, 1, 0) for t in range(MAX_MOVES)])
    solver.add(move_count == num_moves)
    
    result = solver.check()
    
    if result == sat:
        model = solver.model()
        print(f"STATUS: sat")
        print(f"Minimum moves found: {num_moves}")
        
        # Extract solution
        moves = []
        for t in range(num_moves):
            robot_val = model.eval(move_robot[t])
            if robot_val == 1:
                robot = "A"
                from_pos = [int(model.eval(pos_A_row[t])), int(model.eval(pos_A_col[t]))]
                to_pos = [int(model.eval(pos_A_row[t+1])), int(model.eval(pos_A_col[t+1]))]
            elif robot_val == 2:
                robot = "B"
                from_pos = [int(model.eval(pos_B_row[t])), int(model.eval(pos_B_col[t]))]
                to_pos = [int(model.eval(pos_B_row[t+1])), int(model.eval(pos_B_col[t+1]))]
            else:
                continue  # No move
            
            moves.append({
                "robot": robot,
                "from": from_pos,
                "to": to_pos
            })
        
        final_positions = {
            "A": [int(model.eval(pos_A_row[MAX_MOVES])), int(model.eval(pos_A_col[MAX_MOVES]))],
            "B": [int(model.eval(pos_B_row[MAX_MOVES])), int(model.eval(pos_B_col[MAX_MOVES]))]
        }
        
        print(f"solution_found: True")
        print(f"moves: {num_moves}")
        print(f"sequence: {moves}")
        print(f"final_positions: {final_positions}")
        
        solver.pop()
        break
    else:
        solver.pop()
        if num_moves == MAX_MOVES:
            print("STATUS: unsat")
            print("No solution found within the move limit")
        else:
            print(f"Trying {num_moves + 1} moves...")