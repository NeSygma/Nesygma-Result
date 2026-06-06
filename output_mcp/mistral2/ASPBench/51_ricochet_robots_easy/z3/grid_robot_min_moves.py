from z3 import *

# BENCHMARK_MODE: ON (model-finding with guaranteed solution)
BENCHMARK_MODE = True

# ====== PROBLEM DATA ======
GRID_SIZE = 4  # 0..3 for rows and columns
ROBOTS = {"A": (0, 1), "B": (1, 1)}
TARGET = (2, 1)

# Walls: vertical barriers between columns at specific rows
# Represented as (row, col, direction) where direction is 'right' or 'left'
# Here: column 2 right side: rows 0-1 => blocks moving from col=1 to col=2 at rows 0,1
WALLS = [(0, 1, 'right'), (1, 1, 'right')]  # (row, col, side) where side='right' means blocks (row,col) -> (row,col+1)

# ====== SOLVER SETUP ======
opt = Optimize()

# ====== VARIABLES ======
# Time horizon: we will search for a solution with at most MAX_T moves
# We don't know the minimal T, so we will incrementally increase MAX_T until a solution is found
# For now, set a reasonable upper bound (e.g., 10)
MAX_T = 10

# For each time step t in 0..MAX_T, track robot positions
# Use a dictionary: robot -> array of positions over time
robot_pos = {r: [Array(f"pos_{r}_{t}", IntSort(), IntSort()) for t in range(MAX_T + 1)] for r in ROBOTS.keys()}

# For each time step t in 0..MAX_T, track which robot moves (optional, but useful for sequence)
# We'll instead derive moves from position changes

# Decision variables: whether a robot moves at time t (optional, but helps with constraints)
moved = [[Bool(f"moved_{r}_{t}") for t in range(MAX_T)] for r in ROBOTS.keys()]

# For each time step t in 0..MAX_T, track the move direction (optional)
# We'll instead derive direction from position change

# ====== INITIAL STATE ======
for r in ROBOTS.keys():
    opt.add(Select(robot_pos[r][0], 0) == ROBOTS[r][0])  # row
    opt.add(Select(robot_pos[r][0], 1) == ROBOTS[r][1])  # col

# ====== GOAL STATE ======
# At some time T <= MAX_T, Robot A must be at TARGET
opt.add(Or([Select(robot_pos["A"][t], 0) == TARGET[0] and Select(robot_pos["A"][t], 1) == TARGET[1] for t in range(MAX_T + 1)]))

# ====== MOVEMENT CONSTRAINTS ======
# For each time step t from 0 to MAX_T-1, and for each robot r
for t in range(MAX_T):
    for r in ROBOTS.keys():
        # Current and next position
        curr_row = Select(robot_pos[r][t], 0)
        curr_col = Select(robot_pos[r][t], 1)
        next_row = Select(robot_pos[r][t + 1], 0)
        next_col = Select(robot_pos[r][t + 1], 1)

        # Movement is either staying or moving one step in a cardinal direction
        # We allow staying in place (optional, but useful for synchronization)
        opt.add(Or(
            # Stay
            And(next_row == curr_row, next_col == curr_col),
            # Move up
            And(next_row == curr_row - 1, next_col == curr_col, curr_row - 1 >= 0),
            # Move down
            And(next_row == curr_row + 1, next_col == curr_col, curr_row + 1 < GRID_SIZE),
            # Move left
            And(next_row == curr_row, next_col == curr_col - 1, curr_col - 1 >= 0),
            # Move right
            And(next_row == curr_row, next_col == curr_col + 1, curr_col + 1 < GRID_SIZE)
        ))

        # If the robot moves, it must not cross a wall
        # Check if the move is rightward from col=1 to col=2 at rows 0 or 1
        for (wr, wc, side) in WALLS:
            if side == 'right':
                # Blocked if moving from (wr, wc) to (wr, wc+1)
                opt.add(Not(And(
                    curr_row == wr, curr_col == wc,
                    next_row == wr, next_col == wc + 1,
                    moved[r][t]
                )))

# ====== NO COLLISIONS ======
# At each time step, no two robots can occupy the same cell
for t in range(MAX_T + 1):
    for r1 in ROBOTS.keys():
        for r2 in ROBOTS.keys():
            if r1 < r2:  # avoid duplicate pairs
                opt.add(Not(And(
                    Select(robot_pos[r1][t], 0) == Select(robot_pos[r2][t], 0),
                    Select(robot_pos[r1][t], 1) == Select(robot_pos[r2][t], 1)
                )))

# ====== MINIMIZE NUMBER OF MOVES ======
# We want to minimize the total number of moves across all robots
# But we only care about the first time Robot A reaches the target
# So we will minimize the time T when Robot A reaches the target
# We'll use a variable T_goal to represent the time when Robot A reaches the target
T_goal = Int("T_goal")
opt.add(T_goal >= 0, T_goal <= MAX_T)
opt.add(Select(robot_pos["A"][T_goal], 0) == TARGET[0])
opt.add(Select(robot_pos["A"][T_goal], 1) == TARGET[1])

# Minimize T_goal
opt.minimize(T_goal)

# ====== SOLVE ======
result = opt.check()

# ====== OUTPUT ======
if result == sat:
    model = opt.model()
    T_goal_val = model[T_goal]
    
    # Reconstruct the sequence of moves up to T_goal_val
    sequence = []
    for t in range(int(T_goal_val.as_long())):
        for r in ROBOTS.keys():
            curr_row = model.eval(Select(robot_pos[r][t], 0), model_completion=True)
            curr_col = model.eval(Select(robot_pos[r][t], 1), model_completion=True)
            next_row = model.eval(Select(robot_pos[r][t + 1], 0), model_completion=True)
            next_col = model.eval(Select(robot_pos[r][t + 1], 1), model_completion=True)
            
            if curr_row != next_row or curr_col != next_col:
                # A move happened
                from_pos = [int(str(curr_row)), int(str(curr_col))]
                to_pos = [int(str(next_row)), int(str(next_col))]
                sequence.append({
                    "robot": r,
                    "from": from_pos,
                    "to": to_pos
                })
    
    # Final positions
    final_positions = {}
    for r in ROBOTS.keys():
        final_row = model.eval(Select(robot_pos[r][int(T_goal_val.as_long())], 0), model_completion=True)
        final_col = model.eval(Select(robot_pos[r][int(T_goal_val.as_long())], 1), model_completion=True)
        final_positions[r] = [int(str(final_row)), int(str(final_col))]
    
    print("STATUS: sat")
    print(f"solution_found = True")
    print(f"moves = {len(sequence)}")
    print("sequence =")
    for move in sequence:
        print(f"  - robot: {move['robot']}, from: {move['from']}, to: {move['to']}")
    print("final_positions =")
    for r, pos in final_positions.items():
        print(f"  {r}: {pos}")
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")