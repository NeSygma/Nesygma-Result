from z3 import *

# Grid size
N = 5  # 0-4 for rows and cols

# Robots
robots = ["A", "B", "C"]
robot_idx = {"A": 0, "B": 1, "C": 2}

# Starting positions
start_pos = {
    "A": (0, 1),
    "B": (1, 1),
    "C": (3, 1)
}

# Target: Robot A must reach (2, 3)
target = (2, 3)

# Walls: vertical barriers at column boundaries
# Wall at col c right side means you cannot move from (r, c) to (r, c+1) for blocked rows
# Column 0 right side: rows 0-4 (left boundary)
# Column 1 right side: rows 0-1 and 3-4 (bridge opening at row 2)
# Column 2 right side: rows 0-1 and 3-4 (bridge opening at row 2)

# wall_blocked[row][col] = True means there is a wall on the right side of (row, col)
# i.e., you cannot move from (row, col) to (row, col+1)
wall_right = [[False for _ in range(N)] for _ in range(N)]

# Column 0 right side: rows 0-4
for r in range(N):
    wall_right[r][0] = True

# Column 1 right side: rows 0-1 and 3-4
for r in range(N):
    if r != 2:
        wall_right[r][1] = True

# Column 2 right side: rows 0-1 and 3-4
for r in range(N):
    if r != 2:
        wall_right[r][2] = True

# We need to find the minimum number of moves.
# Let's try increasing move counts until we find a solution.
# Expected minimum is 7.

def can_move(r1, c1, r2, c2):
    """Check if a move from (r1,c1) to (r2,c2) is valid (single step, no wall, in bounds)"""
    # Must be within bounds
    if not (0 <= r1 < N and 0 <= c1 < N and 0 <= r2 < N and 0 <= c2 < N):
        return False
    # Must be Manhattan distance 1
    if abs(r1 - r2) + abs(c1 - c2) != 1:
        return False
    # Check walls
    if r1 == r2:
        # Horizontal move
        if c2 == c1 + 1:
            # Moving right: check wall on right side of (r1, c1)
            if wall_right[r1][c1]:
                return False
        elif c2 == c1 - 1:
            # Moving left: check wall on right side of (r1, c2) (the cell to the left)
            if wall_right[r1][c2]:
                return False
    # Vertical moves have no walls (only vertical walls exist)
    return True

# Precompute all valid moves
valid_moves = {}
for robot in robots:
    moves = []
    for r1 in range(N):
        for c1 in range(N):
            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                r2, c2 = r1 + dr, c1 + dc
                if can_move(r1, c1, r2, c2):
                    moves.append(((r1, c1), (r2, c2)))
    valid_moves[robot] = moves

print(f"Total valid moves per robot: {len(valid_moves['A'])}")

# Try increasing move counts
BENCHMARK_MODE = True

for max_moves in range(1, 15):
    solver = Solver()
    
    # Variables: for each time step t (0 to max_moves), we have positions of all robots
    # pos[t][robot_idx] = (row, col)
    pos = [[Int(f"pos_{t}_{r}_row"), Int(f"pos_{t}_{r}_col")] for t in range(max_moves + 1) for r in range(3)]
    # Reshape to [t][robot][coord]
    pos_grid = [[[Int(f"pos_{t}_{r}_row"), Int(f"pos_{t}_{r}_col")] for r in range(3)] for t in range(max_moves + 1)]
    
    # Actually let's use a simpler structure
    # pos[t][r] = (row, col) as two Ints
    pos_rows = [[Int(f"r_{t}_{r}") for r in range(3)] for t in range(max_moves + 1)]
    pos_cols = [[Int(f"c_{t}_{r}") for r in range(3)] for t in range(max_moves + 1)]
    
    # Initial positions
    for r_idx, robot in enumerate(robots):
        sr, sc = start_pos[robot]
        solver.add(pos_rows[0][r_idx] == sr)
        solver.add(pos_cols[0][r_idx] == sc)
    
    # Bounds
    for t in range(max_moves + 1):
        for r_idx in range(3):
            solver.add(pos_rows[t][r_idx] >= 0)
            solver.add(pos_rows[t][r_idx] < N)
            solver.add(pos_cols[t][r_idx] >= 0)
            solver.add(pos_cols[t][r_idx] < N)
    
    # No collisions: no two robots at same position at same time
    for t in range(max_moves + 1):
        for r1 in range(3):
            for r2 in range(r1 + 1, 3):
                solver.add(Not(And(pos_rows[t][r1] == pos_rows[t][r2], pos_cols[t][r1] == pos_cols[t][r2])))
    
    # Move constraints: at each step, exactly one robot moves one step
    # We'll use an action variable: which robot moves at step t (0,1,2 for A,B,C, or -1 for no move)
    # But we need exactly one move per step for the first max_moves steps
    # Actually, we want to find a sequence of exactly max_moves moves.
    # At each step t (0 to max_moves-1), exactly one robot moves.
    
    for t in range(max_moves):
        # Which robot moves at step t
        move_robot = Int(f"move_{t}")
        solver.add(move_robot >= 0)
        solver.add(move_robot < 3)
        
        # For each possible robot that could move
        move_possible = []
        for r_idx in range(3):
            # This robot moves from its position at time t to a new position at time t+1
            # The move must be a valid single step
            # We need to encode: if move_robot == r_idx, then:
            #   - pos_rows[t+1][r_idx] != pos_rows[t][r_idx] OR pos_cols[t+1][r_idx] != pos_cols[t][r_idx]
            #   - Manhattan distance = 1
            #   - No wall violation
            #   - Other robots stay in place
            
            # Other robots stay in place
            for r2 in range(3):
                if r2 != r_idx:
                    solver.add(Implies(move_robot == r_idx, pos_rows[t+1][r2] == pos_rows[t][r2]))
                    solver.add(Implies(move_robot == r_idx, pos_cols[t+1][r2] == pos_cols[t][r2]))
            
            # The moving robot changes position by exactly one step
            dr = pos_rows[t+1][r_idx] - pos_rows[t][r_idx]
            dc = pos_cols[t+1][r_idx] - pos_cols[t][r_idx]
            
            # Manhattan distance = 1
            solver.add(Implies(move_robot == r_idx, 
                Or(And(dr == 1, dc == 0), And(dr == -1, dc == 0), 
                   And(dr == 0, dc == 1), And(dr == 0, dc == -1))))
            
            # Wall constraints
            # Moving right: dr=0, dc=1 -> check wall_right at (row, col)
            solver.add(Implies(And(move_robot == r_idx, dr == 0, dc == 1),
                Not(wall_right[pos_rows[t][r_idx].as_long() if isinstance(pos_rows[t][r_idx], IntNumRef) else 0][pos_cols[t][r_idx].as_long() if isinstance(pos_cols[t][r_idx], IntNumRef) else 0])))
            # Hmm, we can't use as_long() on symbolic expressions.
            # We need a different approach for wall constraints.
    
    # Let me rethink - the wall constraints need to be encoded symbolically.
    # Let's use a different approach with precomputed valid moves.

print("--- Approach 2: Using move variables ---")

# For each time step, we select a robot and a valid move for that robot.
# Let's encode moves as: at step t, robot r moves from (r1,c1) to (r2,c2)
# where ((r1,c1),(r2,c2)) is a valid move.

# Precompute all valid moves as tuples
all_moves = []
for r1 in range(N):
    for c1 in range(N):
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            r2, c2 = r1 + dr, c1 + dc
            if can_move(r1, c1, r2, c2):
                all_moves.append(((r1, c1), (r2, c2)))

print(f"Total valid moves: {len(all_moves)}")

# Map each move to an index
move_list = all_moves
M = len(move_list)

for max_moves in range(1, 12):
    solver = Solver()
    
    # Position variables
    pos_rows = [[Int(f"r_{t}_{r}") for r in range(3)] for t in range(max_moves + 1)]
    pos_cols = [[Int(f"c_{t}_{r}") for r in range(3)] for t in range(max_moves + 1)]
    
    # Initial positions
    for r_idx, robot in enumerate(robots):
        sr, sc = start_pos[robot]
        solver.add(pos_rows[0][r_idx] == sr)
        solver.add(pos_cols[0][r_idx] == sc)
    
    # Bounds
    for t in range(max_moves + 1):
        for r_idx in range(3):
            solver.add(pos_rows[t][r_idx] >= 0)
            solver.add(pos_rows[t][r_idx] < N)
            solver.add(pos_cols[t][r_idx] >= 0)
            solver.add(pos_cols[t][r_idx] < N)
    
    # No collisions
    for t in range(max_moves + 1):
        for r1 in range(3):
            for r2 in range(r1 + 1, 3):
                solver.add(Not(And(pos_rows[t][r1] == pos_rows[t][r2], pos_cols[t][r1] == pos_cols[t][r2])))
    
    # At each step, select a robot and a valid move
    for t in range(max_moves):
        # Select which robot moves
        move_robot = Int(f"move_robot_{t}")
        solver.add(move_robot >= 0)
        solver.add(move_robot < 3)
        
        # Select which move (index into move_list)
        move_idx = Int(f"move_idx_{t}")
        solver.add(move_idx >= 0)
        solver.add(move_idx < M)
        
        # The move must start from the robot's current position
        # and end at the robot's next position
        # move_list[move_idx] = ((r1,c1), (r2,c2))
        # We need: pos_rows[t][move_robot] == r1 AND pos_cols[t][move_robot] == c1
        # AND pos_rows[t+1][move_robot] == r2 AND pos_cols[t+1][move_robot] == c2
        
        # For each possible move index, encode the implication
        for mi, ((r1, c1), (r2, c2)) in enumerate(move_list):
            # If this move is selected, then the robot's position changes accordingly
            # and the robot must be at (r1,c1) at time t
            solver.add(Implies(And(move_idx == mi, move_robot == 0),
                And(pos_rows[t][0] == r1, pos_cols[t][0] == c1,
                    pos_rows[t+1][0] == r2, pos_cols[t+1][0] == c2)))
            solver.add(Implies(And(move_idx == mi, move_robot == 1),
                And(pos_rows[t][1] == r1, pos_cols[t][1] == c1,
                    pos_rows[t+1][1] == r2, pos_cols[t+1][1] == c2)))
            solver.add(Implies(And(move_idx == mi, move_robot == 2),
                And(pos_rows[t][2] == r1, pos_cols[t][2] == c1,
                    pos_rows[t+1][2] == r2, pos_cols[t+1][2] == c2)))
        
        # Other robots stay in place
        for r_idx in range(3):
            for r2_idx in range(3):
                if r2_idx != r_idx:
                    solver.add(Implies(move_robot == r_idx,
                        And(pos_rows[t+1][r2_idx] == pos_rows[t][r2_idx],
                            pos_cols[t+1][r2_idx] == pos_cols[t][r2_idx])))
    
    # Goal: Robot A at target at the final time step
    solver.add(pos_rows[max_moves][0] == target[0])
    solver.add(pos_cols[max_moves][0] == target[1])
    
    print(f"Trying max_moves = {max_moves}...")
    result = solver.check()
    
    if result == sat:
        m = solver.model()
        print(f"STATUS: sat")
        print(f"Solution found with {max_moves} moves!")
        
        # Extract the sequence
        print(f"moves: {max_moves}")
        print(f"solution_found: True")
        
        # Print final positions
        print("final_positions:")
        for r_idx, robot in enumerate(robots):
            fr = m.eval(pos_rows[max_moves][r_idx])
            fc = m.eval(pos_cols[max_moves][r_idx])
            print(f"  {robot}: [{fr}, {fc}]")
        
        # Print sequence
        print("sequence:")
        for t in range(max_moves):
            mr = m.eval(Int(f"move_robot_{t}"))
            mi = m.eval(Int(f"move_idx_{t}"))
            ((r1, c1), (r2, c2)) = move_list[mi.as_long()]
            robot_name = robots[mr.as_long()]
            print(f"  Step {t+1}: Robot {robot_name} from [{r1},{c1}] to [{r2},{c2}]")
        
        break
    elif result == unsat:
        print(f"  No solution with {max_moves} moves")
    else:
        print(f"  Unknown")