from z3 import *

# BENCHMARK_MODE: ON (model-finding mode)
BENCHMARK_MODE = True

# Grid size
N = 5

# Robots
robots = ["A", "B", "C"]

# Initial positions
initial_positions = {
    "A": (0, 1),
    "B": (1, 1),
    "C": (3, 1),
}

# Target position for Robot A
target_position = (2, 3)

# Wall constraints: walls are on the right side of columns 0, 1, 2
# Openings: column 1 and 2 have openings at row 2
# A move is invalid if it crosses a wall

def is_valid_move(from_pos, to_pos):
    from_row, from_col = from_pos
    to_row, to_col = to_pos
    
    # Check if move is exactly one step in a cardinal direction
    if abs(from_row - to_row) + abs(from_col - to_col) != 1:
        return False
    
    # Check if move crosses a wall
    # Walls are on the right side of columns 0, 1, 2
    # So, moving from col c to c+1 is invalid if there is a wall between c and c+1
    if from_col < to_col:  # Moving right
        if from_col == 0 and to_col == 1:
            # Check if there is a wall between col 0 and 1 at this row
            # Walls on column 0 right side: rows 0-4 (always blocked)
            return False
        elif from_col == 1 and to_col == 2:
            # Walls on column 1 right side: rows 0-1 and 3-4 (blocked), row 2 (open)
            if from_row not in [2]:
                return False
        elif from_col == 2 and to_col == 3:
            # Walls on column 2 right side: rows 0-1 and 3-4 (blocked), row 2 (open)
            if from_row not in [2]:
                return False
    elif from_col > to_col:  # Moving left
        if from_col == 1 and to_col == 0:
            # Moving left from col 1 to 0: no wall on left side of col 1
            pass
        elif from_col == 2 and to_col == 1:
            # Moving left from col 2 to 1: no wall on left side of col 2
            pass
        elif from_col == 3 and to_col == 2:
            # Moving left from col 3 to 2: no wall on left side of col 3
            pass
    
    # Check grid bounds
    if to_row < 0 or to_row >= N or to_col < 0 or to_col >= N:
        return False
    
    return True

# We will try to find a solution with a bounded number of moves
# Start with the expected minimum (7) and increment if needed
max_moves = 7

# We will use Optimize to minimize the number of moves
opt = Optimize()

# Decision variables:
# pos[t][r] = (row, col) position of robot r at time t
# Use a dictionary of lists of tuples (row, col) for positions
pos = [{
    r: [Int(f"pos_{t}_{r}_row"), Int(f"pos_{t}_{r}_col")] for r in robots
} for t in range(max_moves + 1)]

# move[t][r] = whether robot r moves at time t
move = [[Bool(f"move_{t}_{r}") for r in robots] for t in range(max_moves)]

# direction[t][r] = direction of movement at time t (0: none, 1: up, 2: down, 3: left, 4: right)
direction = [[Int(f"dir_{t}_{r}") for r in robots] for t in range(max_moves)]

# Initial positions
for r in robots:
    from_row, from_col = initial_positions[r]
    opt.add(pos[0][r][0] == from_row)
    opt.add(pos[0][r][1] == from_col)

# Target position for Robot A at the final time step
opt.add(pos[max_moves]["A"][0] == target_position[0])
opt.add(pos[max_moves]["A"][1] == target_position[1])

# Constraints for each time step
for t in range(max_moves):
    for r in robots:
        # If robot r moves at time t, its position changes according to direction
        from_row, from_col = pos[t][r]
        to_row, to_col = pos[t+1][r]
        
        # If not moving, position remains the same
        opt.add(Implies(Not(move[t][r]), 
                        And(to_row == from_row, to_col == from_col)))
        
        # If moving, new position must be valid
        opt.add(Implies(move[t][r],
                        And(
                            # Direction is one of 1 (up), 2 (down), 3 (left), 4 (right)
                            Or(direction[t][r] == 1, direction[t][r] == 2, 
                               direction[t][r] == 3, direction[t][r] == 4),
                            # New position is one step in the chosen direction
                            Or(
                                And(direction[t][r] == 1, to_row == from_row - 1, to_col == from_col),
                                And(direction[t][r] == 2, to_row == from_row + 1, to_col == from_col),
                                And(direction[t][r] == 3, to_row == from_row, to_col == from_col - 1),
                                And(direction[t][r] == 4, to_row == from_row, to_col == from_col + 1)
                            ),
                            # Move must be valid (no walls, within bounds)
                            is_valid_move((from_row.as_long(), from_col.as_long()), 
                                          (to_row.as_long(), to_col.as_long()))
                        )))

# No collisions: all robots must be in distinct positions at each time step
for t in range(max_moves + 1):
    for i in range(len(robots)):
        for j in range(i + 1, len(robots)):
            r1 = robots[i]
            r2 = robots[j]
            opt.add(Not(And(pos[t][r1][0] == pos[t][r2][0], 
                            pos[t][r1][1] == pos[t][r2][1])))

# Only one robot can move at each time step (optional, but simplifies the problem)
# Alternatively, allow multiple moves but ensure no collisions
# Here, we allow only one robot to move at each time step
for t in range(max_moves):
    opt.add(Sum([If(move[t][r], 1, 0) for r in robots]) <= 1)

# Minimize the number of moves (time steps)
has_solution = Bool("has_solution")
opt.add(has_solution == And(pos[max_moves]["A"][0] == target_position[0], 
                            pos[max_moves]["A"][1] == target_position[1]))

# If a solution exists, minimize the number of moves
opt.minimize(Sum([If(move[t]["A"], 1, 0) for t in range(max_moves)]))

# Check if a solution exists
result = opt.check()

if result == sat:
    model = opt.model()
    # Extract the number of moves
    moves = 0
    for t in range(max_moves):
        if model.evaluate(Sum([If(move[t][r], 1, 0) for r in robots])) == 1:
            moves += 1
    
    # Extract the sequence of moves
    sequence = []
    for t in range(max_moves):
        for r in robots:
            if model.evaluate(move[t][r]):
                from_pos = (model.evaluate(pos[t][r][0]).as_long(), 
                            model.evaluate(pos[t][r][1]).as_long())
                to_pos = (model.evaluate(pos[t+1][r][0]).as_long(), 
                          model.evaluate(pos[t+1][r][1]).as_long())
                direction_val = model.evaluate(direction[t][r]).as_long()
                direction_str = {1: "up", 2: "down", 3: "left", 4: "right"}.get(direction_val, "none")
                sequence.append({
                    "robot": r,
                    "from": list(from_pos),
                    "to": list(to_pos),
                    "direction": direction_str
                })
    
    # Extract final positions
    final_positions = {}
    for r in robots:
        final_positions[r] = [
            model.evaluate(pos[max_moves][r][0]).as_long(),
            model.evaluate(pos[max_moves][r][1]).as_long()
        ]
    
    print("STATUS: sat")
    print(f"solution_found = True")
    print(f"moves = {moves}")
    print(f"sequence = {sequence}")
    print(f"final_positions = {final_positions}")
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")