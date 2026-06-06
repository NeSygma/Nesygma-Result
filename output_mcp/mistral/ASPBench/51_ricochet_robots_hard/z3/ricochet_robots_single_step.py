from z3 import *

# Parameters
max_moves = 10  # Upper bound on the number of moves
robots = ['A', 'B', 'C']
initial_positions = {'A': (0, 1), 'B': (1, 1), 'C': (3, 1)}
target = (2, 3)

# Wall constraints: walls are between (r,c) and (r,c+1) if there is a wall on the right side of column c in row r.
# From the problem:
# - Column 0 right side: walls in all rows (0-4)
# - Column 1 right side: walls in rows 0-1 and 3-4, no wall in row 2
# - Column 2 right side: walls in rows 0-1 and 3-4, no wall in row 2
# So, horizontal movement from (r,0) to (r,1) is blocked for all r.
# Horizontal movement from (r,1) to (r,2) is blocked for r in {0,1,3,4}, allowed for r=2.
# Horizontal movement from (r,2) to (r,3) is blocked for r in {0,1,3,4}, allowed for r=2.

def can_move_horizontally(r, c_from, c_to):
    # c_to = c_from + 1 or c_from - 1
    if c_to == c_from + 1:
        # Moving right
        if c_from == 0:
            return False  # wall between 0 and 1 in all rows
        elif c_from == 1:
            return r == 2  # only allowed in row 2
        elif c_from == 2:
            return r == 2  # only allowed in row 2
        else:
            return True  # no wall specified, assume allowed
    elif c_to == c_from - 1:
        # Moving left
        if c_from == 1:
            return False  # wall between 0 and 1 in all rows
        elif c_from == 2:
            return r == 2  # only allowed in row 2
        elif c_from == 3:
            return r == 2  # only allowed in row 2
        else:
            return True  # no wall specified, assume allowed
    else:
        return False

def can_move_vertically(r_from, c, r_to):
    # Vertical movement is never blocked by walls (only by grid bounds)
    return True

# Create solver
opt = Optimize()

# Decision variables: for each move t and robot, position (r, c)
# We'll use arrays for positions over time
positions = {}
for robot in robots:
    positions[robot] = [(Int(f"{robot}_r_{t}"), Int(f"{robot}_c_{t}")) for t in range(max_moves)]

# Initial positions
for robot in robots:
    r0, c0 = initial_positions[robot]
    opt.add(positions[robot][0][0] == r0)
    opt.add(positions[robot][0][1] == c0)

# Movement constraints and collision avoidance
for t in range(max_moves - 1):
    for robot in robots:
        r_t, c_t = positions[robot][t]
        r_t1, c_t1 = positions[robot][t+1]
        # Robot can move to adjacent cell or stay (but staying is not useful for minimization)
        # Movement options: up, down, left, right, or stay
        opt.add(Or(
            # Up
            And(r_t1 == r_t - 1, c_t1 == c_t, r_t1 >= 0),
            # Down
            And(r_t1 == r_t + 1, c_t1 == c_t, r_t1 <= 4),
            # Left
            And(r_t1 == r_t, c_t1 == c_t - 1, c_t1 >= 0),
            # Right
            And(r_t1 == r_t, c_t1 == c_t + 1, c_t1 <= 4),
            # Stay
            And(r_t1 == r_t, c_t1 == c_t)
        ))
        # Wall constraints for horizontal movement
        # If moving horizontally, check wall
        opt.add(Implies(
            And(r_t1 == r_t, Or(c_t1 == c_t + 1, c_t1 == c_t - 1)),
            can_move_horizontally(r_t, c_t, c_t1)
        ))
        # Vertical movement is always allowed (no walls)
        opt.add(Implies(
            And(c_t1 == c_t, Or(r_t1 == r_t + 1, r_t1 == r_t - 1)),
            can_move_vertically(r_t, c_t, r_t1)
        ))

# Collision avoidance: all robots must be in distinct cells at each time step
for t in range(max_moves):
    cells_at_t = [positions[robot][t] for robot in robots]
    # Flatten the list of tuples into a list of Z3 expressions
    distinct_exprs = []
    for (r, c) in cells_at_t:
        distinct_exprs.append(r)
        distinct_exprs.append(c)
    opt.add(Distinct(distinct_exprs))

# Goal: Robot A must reach (2,3) at some time step
# We will find the minimal t where this happens
moves_used = Int('moves_used')
opt.add(moves_used >= 0)
opt.add(moves_used < max_moves)

# Ensure the goal is reached at or before moves_used
for t in range(max_moves):
    opt.add(Implies(t <= moves_used, Or(
        positions['A'][t][0] == 2,
        positions['A'][t][1] == 3
    )))
    # Actually, we need both conditions to be true simultaneously
    opt.add(Implies(t <= moves_used, And(
        positions['A'][t][0] == 2,
        positions['A'][t][1] == 3
    )))

opt.minimize(moves_used)

# Check
result = opt.check()
if result == sat:
    model = opt.model()
    print("STATUS: sat")
    # Extract solution
    moves_count = model[moves_used].as_long()
    print(f"Minimum moves: {moves_count}")
    # Extract sequence
    sequence = []
    for t in range(moves_count):
        for robot in robots:
            r_prev = model[positions[robot][t][0]].as_long()
            c_prev = model[positions[robot][t][1]].as_long()
            r_curr = model[positions[robot][t+1][0]].as_long()
            c_curr = model[positions[robot][t+1][1]].as_long()
            if (r_prev, c_prev) != (r_curr, c_curr):
                sequence.append({
                    'robot': robot,
                    'from': [r_prev, c_prev],
                    'to': [r_curr, c_curr]
                })
    print("sequence =", sequence)
    # Final positions
    final_positions = {robot: [model[positions[robot][moves_count][0]].as_long(), model[positions[robot][moves_count][1]].as_long()] for robot in robots}
    print("final_positions =", final_positions)
elif result == unsat:
    print("STATUS: unsat")
else:
    print("STATUS: unknown")