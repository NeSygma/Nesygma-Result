from z3 import *

# Parameters
rows, cols = 5, 5
robots = ['A','B','C']
robot_index = {r:i for i,r in enumerate(robots)}
# Initial positions
init_pos = {
    'A': (0,1),
    'B': (1,1),
    'C': (3,1)
}
# Target for A
target = (2,3)
# Max steps
max_steps = 8

# Precompute allowed moves between cells
allowed = {}
for r1 in range(rows):
    for c1 in range(cols):
        for dr,dc in [(1,0),(-1,0),(0,1),(0,-1)]:
            r2, c2 = r1+dr, c1+dc
            if 0 <= r2 < rows and 0 <= c2 < cols:
                # Check wall between (r1,c1) and (r2,c2)
                blocked = False
                # vertical walls
                if c1 == c2:
                    # horizontal adjacency, no walls
                    blocked = False
                else:
                    # vertical adjacency
                    if c1 == 0 and c2 == 1:
                        blocked = True
                    elif c1 == 1 and c2 == 0:
                        blocked = True
                    elif c1 == 1 and c2 == 2:
                        if r1 in {0,1,3,4}:
                            blocked = True
                    elif c1 == 2 and c2 == 1:
                        if r1 in {0,1,3,4}:
                            blocked = True
                    elif c1 == 2 and c2 == 3:
                        if r1 in {0,1,3,4}:
                            blocked = True
                    elif c1 == 3 and c2 == 2:
                        if r1 in {0,1,3,4}:
                            blocked = True
                if not blocked:
                    allowed[(r1,c1,r2,c2)] = True

# Solver
opt = Optimize()
# Position variables: pos_row[t][i], pos_col[t][i]
pos_row = [[Int(f'row_{t}_{i}') for i in range(len(robots))] for t in range(max_steps+1)]
pos_col = [[Int(f'col_{t}_{i}') for i in range(len(robots))] for t in range(max_steps+1)]
# Moved flags
moved = [[Bool(f'moved_{t}_{i}') for i in range(len(robots))] for t in range(max_steps)]

# Initial positions
for i,r in enumerate(robots):
    opt.add(pos_row[0][i] == init_pos[r][0])
    opt.add(pos_col[0][i] == init_pos[r][1])

# Constraints for each step
for t in range(max_steps):
    # At most one robot moves
    opt.add(Sum([If(moved[t][i],1,0) for i in range(len(robots))]) <= 1)
    for i in range(len(robots)):
        # If moved, must move to an allowed adjacent cell
        # Build list of allowed moves from current position
        # Use implication for each possible target
        # We need to ensure that if moved, then pos[t+1] equals one of allowed
        # We'll add a disjunction of possibilities
        move_options = []
        for (r1,c1,r2,c2) in allowed:
            if r1 == 0 and c1 == 0:  # placeholder to avoid unused variable
                pass
        # Instead, we will add implications for each allowed move
        for (r1,c1,r2,c2) in allowed:
            opt.add(Implies(And(pos_row[t][i]==r1, pos_col[t][i]==c1, moved[t][i]), And(pos_row[t+1][i]==r2, pos_col[t+1][i]==c2)))
        # If not moved, stay in place
        opt.add(Implies(Not(moved[t][i]), And(pos_row[t+1][i]==pos_row[t][i], pos_col[t+1][i]==pos_col[t][i])))
    # Collision avoidance at next step
    for i in range(len(robots)):
        for j in range(i+1, len(robots)):
            opt.add(Or(pos_row[t+1][i] != pos_row[t+1][j], pos_col[t+1][i] != pos_col[t+1][j]))

# Goal: A at target at final step
opt.add(pos_row[max_steps][robot_index['A']] == target[0])
opt.add(pos_col[max_steps][robot_index['A']] == target[1])

# Objective: minimize total moves
total_moves = Sum([If(moved[t][i],1,0) for t in range(max_steps) for i in range(len(robots))])
opt.minimize(total_moves)

# Check
result = opt.check()
print("STATUS: ", result)
if result == sat:
    m = opt.model()
    # Compute moves count
    moves_count = 0
    for t in range(max_steps):
        for i in range(len(robots)):
            if is_true(m.evaluate(moved[t][i])):
                moves_count += 1
    # Build sequence
    sequence = []
    for t in range(max_steps):
        for i in range(len(robots)):
            if is_true(m.evaluate(moved[t][i])):
                r_from = m.evaluate(pos_row[t][i]).as_long()
                c_from = m.evaluate(pos_col[t][i]).as_long()
                r_to = m.evaluate(pos_row[t+1][i]).as_long()
                c_to = m.evaluate(pos_col[t+1][i]).as_long()
                sequence.append({"robot": robots[i], "from": [r_from, c_from], "to": [r_to, c_to]})
    # Final positions
    final_positions = {}
    for i,r in enumerate(robots):
        final_positions[r] = [m.evaluate(pos_row[max_steps][i]).as_long(), m.evaluate(pos_col[max_steps][i]).as_long()]
    # Output
    print("solution_found: true")
    print("moves:", moves_count)
    print("sequence:", sequence)
    print("final_positions:", final_positions)
else:
    print("solution_found: false")
    print("moves: 0")
    print("sequence: []")
    print("final_positions: {}")