from z3 import *

# Configuration
GRID_SIZE = 5
MAX_MOVES = 20  # Upper bound for search

# Define wall constraints
# Walls are vertical barriers between columns
# wall_right[col][row] = True means there's a wall on the right side of column col at row row
wall_right = [[False for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

# Column 0 right side: rows 0-4 (left boundary)
for row in range(GRID_SIZE):
    wall_right[0][row] = True

# Column 1 right side: rows 0-1 and 3-4 (bridge opening at row 2)
for row in [0, 1, 3, 4]:
    wall_right[1][row] = True

# Column 2 right side: rows 0-1 and 3-4 (bridge opening at row 2)
for row in [0, 1, 3, 4]:
    wall_right[2][row] = True

# Create solver
solver = Solver()

# Robots: A, B, C
robots = ['A', 'B', 'C']
robot_ids = {robot: i for i, robot in enumerate(robots)}

# Initial positions
initial_positions = {
    'A': (0, 1),
    'B': (1, 1),
    'C': (3, 1)
}

# Target position for Robot A
target_A = (2, 3)

# Decision variables: positions of each robot at each time step
# time_steps: 0 to MAX_MOVES (inclusive)
positions = {}
for robot in robots:
    positions[robot] = {}
    for t in range(MAX_MOVES + 1):
        positions[robot][t] = {}
        positions[robot][t]['row'] = Int(f'{robot}_row_{t}')
        positions[robot][t]['col'] = Int(f'{robot}_col_{t}')
        
        # Initial positions at time 0
        if t == 0:
            solver.add(positions[robot][t]['row'] == initial_positions[robot][0])
            solver.add(positions[robot][t]['col'] == initial_positions[robot][1])
        
        # Bounds for all positions
        solver.add(positions[robot][t]['row'] >= 0)
        solver.add(positions[robot][t]['row'] < GRID_SIZE)
        solver.add(positions[robot][t]['col'] >= 0)
        solver.add(positions[robot][t]['col'] < GRID_SIZE)

# Movement constraints: single-step movements
for t in range(MAX_MOVES):
    for robot in robots:
        r1 = positions[robot][t]['row']
        c1 = positions[robot][t]['col']
        r2 = positions[robot][t+1]['row']
        c2 = positions[robot][t+1]['col']
        
        # Manhattan distance = 1
        solver.add(Or(
            And(r2 == r1, c2 == c1 + 1),  # right
            And(r2 == r1, c2 == c1 - 1),  # left
            And(r2 == r1 + 1, c2 == c1),  # down
            And(r2 == r1 - 1, c2 == c1)   # up
        ))

# Wall constraints: cannot move through walls
for t in range(MAX_MOVES):
    for robot in robots:
        r1 = positions[robot][t]['row']
        c1 = positions[robot][t]['col']
        r2 = positions[robot][t+1]['row']
        c2 = positions[robot][t+1]['col']
        
        # Check if moving right crosses a wall
        # If c2 == c1 + 1, then we're moving from column c1 to c1+1
        # Check if there's a wall at column c1, row r1 (right side of column c1)
        # Use Or-Loop pattern to avoid indexing with Z3 variables
        wall_constraints = []
        for col in range(GRID_SIZE):
            for row in range(GRID_SIZE):
                if wall_right[col][row]:
                    # If moving right from (row, col) to (row, col+1)
                    wall_constraints.append(And(
                        c2 == c1 + 1,
                        r1 == row,
                        c1 == col
                    ))
        if wall_constraints:
            solver.add(Not(Or(wall_constraints)))
        
        # Check if moving left crosses a wall
        # If c2 == c1 - 1, then we're moving from column c1 to c1-1
        # Check if there's a wall at column c1-1, row r1 (right side of column c1-1)
        wall_constraints_left = []
        for col in range(GRID_SIZE):
            for row in range(GRID_SIZE):
                if wall_right[col][row]:
                    # If moving left from (row, col+1) to (row, col)
                    wall_constraints_left.append(And(
                        c2 == c1 - 1,
                        r1 == row,
                        c1 == col + 1
                    ))
        if wall_constraints_left:
            solver.add(Not(Or(wall_constraints_left)))

# No collisions: robots cannot occupy the same cell at the same time
for t in range(MAX_MOVES + 1):
    for i in range(len(robots)):
        for j in range(i + 1, len(robots)):
            robot1 = robots[i]
            robot2 = robots[j]
            solver.add(Or(
                positions[robot1][t]['row'] != positions[robot2][t]['row'],
                positions[robot1][t]['col'] != positions[robot2][t]['col']
            ))

# Goal: Robot A must reach (2, 3) at some time step
# We'll add a boolean variable for each time step indicating if goal is reached
goal_reached = [Bool(f'goal_reached_{t}') for t in range(MAX_MOVES + 1)]
for t in range(MAX_MOVES + 1):
    solver.add(goal_reached[t] == And(
        positions['A'][t]['row'] == target_A[0],
        positions['A'][t]['col'] == target_A[1]
    ))

# At least one goal must be reached
solver.add(Or(goal_reached))

# Minimize the number of moves (time steps until goal is reached)
# We'll use a soft constraint approach: minimize the first time step where goal is reached
# Create a variable for the time when goal is first reached
time_to_goal = Int('time_to_goal')
solver.add(time_to_goal >= 0)
solver.add(time_to_goal <= MAX_MOVES)

# time_to_goal is the smallest t where goal_reached[t] is true
for t in range(MAX_MOVES + 1):
    if t == 0:
        solver.add(Implies(goal_reached[t], time_to_goal == t))
    else:
        # If goal is reached at time t, then time_to_goal <= t
        solver.add(Implies(goal_reached[t], time_to_goal <= t))
        # If goal is not reached at time t, then time_to_goal > t
        solver.add(Implies(Not(goal_reached[t]), time_to_goal > t))

# Also ensure that if goal is reached at time t, it wasn't reached earlier
for t in range(1, MAX_MOVES + 1):
    solver.add(Implies(goal_reached[t], Or([Not(goal_reached[s]) for s in range(t)])))

# Optimize for minimum time_to_goal
opt = Optimize()
opt.add(solver.assertions())
opt.minimize(time_to_goal)

# Check and print results
BENCHMARK_MODE = True
result = opt.check()

if result == sat:
    model = opt.model()
    print("STATUS: sat")
    
    # Find the actual number of moves (time_to_goal)
    moves = model.eval(time_to_goal).as_long()
    print(f"moves = {moves}")
    
    # Extract the sequence of moves
    sequence = []
    for t in range(moves):
        move = {}
        for robot in robots:
            from_pos = [model.eval(positions[robot][t]['row']).as_long(),
                       model.eval(positions[robot][t]['col']).as_long()]
            to_pos = [model.eval(positions[robot][t+1]['row']).as_long(),
                     model.eval(positions[robot][t+1]['col']).as_long()]
            
            # Check if this robot moved
            if from_pos != to_pos:
                move['robot'] = robot
                move['from'] = from_pos
                move['to'] = to_pos
                break  # Only one robot moves per time step
        
        if move:
            sequence.append(move)
    
    print(f"sequence = {sequence}")
    
    # Final positions
    final_positions = {}
    for robot in robots:
        final_row = model.eval(positions[robot][moves]['row']).as_long()
        final_col = model.eval(positions[robot][moves]['col']).as_long()
        final_positions[robot] = [final_row, final_col]
    
    print(f"final_positions = {final_positions}")
    print(f"solution_found = True")
    
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")