from z3 import *

# Parameters
MAX_STEPS = 5  # upper bound on steps to consider
GRID_SIZE = 4

# Helper to check adjacency (Manhattan distance = 1)

def adjacent(r1, c1, r2, c2):
    return Or(
        And(r1 == r2, Abs(c1 - c2) == 1),
        And(c1 == c2, Abs(r1 - r2) == 1)
    )

solver = Optimize()

# Position variables for each time step 0..MAX_STEPS
posA_r = [Int(f"A_r_{t}") for t in range(MAX_STEPS+1)]
posA_c = [Int(f"A_c_{t}") for t in range(MAX_STEPS+1)]
posB_r = [Int(f"B_r_{t}") for t in range(MAX_STEPS+1)]
posB_c = [Int(f"B_c_{t}") for t in range(MAX_STEPS+1)]

# Move indicator for each step
move = [Bool(f"move_{t}") for t in range(MAX_STEPS)]
# Which robot moves at step t (if any)
moveA = [Bool(f"moveA_{t}") for t in range(MAX_STEPS)]
moveB = [Bool(f"moveB_{t}") for t in range(MAX_STEPS)]

# Initial positions
solver.add(posA_r[0] == 0, posA_c[0] == 1)
solver.add(posB_r[0] == 1, posB_c[0] == 1)

# Domain constraints for all positions (within grid)
for t in range(MAX_STEPS+1):
    for var in (posA_r[t], posA_c[t], posB_r[t], posB_c[t]):
        solver.add(var >= 0, var < GRID_SIZE)

# No collision at any time step
for t in range(MAX_STEPS+1):
    solver.add(Or(posA_r[t] != posB_r[t], posA_c[t] != posB_c[t]))

# Wall constraints: cannot cross between col 2 and 3 at rows 0 or 1
def wall_block(r_from, c_from, r_to, c_to):
    return Or(
        And(r_from == 0, c_from == 2, r_to == 0, c_to == 3),
        And(r_from == 0, c_from == 3, r_to == 0, c_to == 2),
        And(r_from == 1, c_from == 2, r_to == 1, c_to == 3),
        And(r_from == 1, c_from == 3, r_to == 1, c_to == 2)
    )

# Transition constraints
for t in range(MAX_STEPS):
    # Exactly one robot moves iff ...
    solver.add(Implies(move[t], Xor(moveA[t], moveB[t])))
    solver.add(Implies(Not(move[t]), And(Not(moveA[t]), Not(moveB[t]))))
    # Define next positions using If expressions and fresh variables
    nextA_r = If(moveA[t], Int(f"A_r_next_{t}"), posA_r[t])
    nextA_c = If(moveA[t], Int(f"A_c_next_{t}"), posA_c[t])
    nextB_r = If(moveB[t], Int(f"B_r_next_{t}"), posB_r[t])
    nextB_c = If(moveB[t], Int(f"B_c_next_{t}"), posB_c[t])
    # Link to position variables at t+1
    solver.add(posA_r[t+1] == nextA_r)
    solver.add(posA_c[t+1] == nextA_c)
    solver.add(posB_r[t+1] == nextB_r)
    solver.add(posB_c[t+1] == nextB_c)
    # Movement constraints for A
    solver.add(Implies(moveA[t], And(
        adjacent(posA_r[t], posA_c[t], nextA_r, nextA_c),
        Not(wall_block(posA_r[t], posA_c[t], nextA_r, nextA_c))
    )))
    # Movement constraints for B
    solver.add(Implies(moveB[t], And(
        adjacent(posB_r[t], posB_c[t], nextB_r, nextB_c),
        Not(wall_block(posB_r[t], posB_c[t], nextB_r, nextB_c))
    )))
    # Prevent moving into the other robot's current cell
    solver.add(Implies(moveA[t], Or(nextA_r != posB_r[t], nextA_c != posB_c[t])))
    solver.add(Implies(moveB[t], Or(nextB_r != posA_r[t], nextB_c != posA_c[t])))

# Goal: Robot A at target (2,1) at final step
solver.add(posA_r[MAX_STEPS] == 2, posA_c[MAX_STEPS] == 1)

# Objective: minimize total moves
total_moves = Sum([If(move[t], 1, 0) for t in range(MAX_STEPS)])
solver.minimize(total_moves)

# Solve
if solver.check() == sat:
    m = solver.model()
    moves_count = m.eval(total_moves).as_long()
    sequence = []
    for t in range(MAX_STEPS):
        if is_true(m.eval(move[t])):
            if is_true(m.eval(moveA[t])):
                robot = "A"
                from_r = m.eval(posA_r[t]).as_long()
                from_c = m.eval(posA_c[t]).as_long()
                to_r = m.eval(posA_r[t+1]).as_long()
                to_c = m.eval(posA_c[t+1]).as_long()
            else:
                robot = "B"
                from_r = m.eval(posB_r[t]).as_long()
                from_c = m.eval(posB_c[t]).as_long()
                to_r = m.eval(posB_r[t+1]).as_long()
                to_c = m.eval(posB_c[t+1]).as_long()
            sequence.append((robot, [from_r, from_c], [to_r, to_c]))
    final_positions = {
        "A": [m.eval(posA_r[MAX_STEPS]).as_long(), m.eval(posA_c[MAX_STEPS]).as_long()],
        "B": [m.eval(posB_r[MAX_STEPS]).as_long(), m.eval(posB_c[MAX_STEPS]).as_long()]
    }
    print("STATUS: sat")
    print("solution_found = True")
    print(f"moves = {moves_count}")
    print("sequence = [")
    for robot, frm, to in sequence:
        print(f"  {{'robot': '{robot}', 'from': {frm}, 'to': {to}}},")
    print("]")
    print(f"final_positions = {final_positions}")
else:
    print("STATUS: unsat")
    print("solution_found = False")