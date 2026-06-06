from z3 import *

BENCHMARK_MODE = True
robots = ['A', 'B', 'C']
n_robots = 3

# Wall definitions (vertical barriers between columns):
# Between col 0 and col 1: ALL rows (0-4)
# Between col 1 and col 2: rows 0,1,3,4 (bridge at row 2)
# Between col 2 and col 3: rows 0,1,3,4 (bridge at row 2)

wall_rows_col01 = [0, 1, 2, 3, 4]  # all rows
wall_rows_col12 = [0, 1, 3, 4]      # bridge at row 2
wall_rows_col23 = [0, 1, 3, 4]      # bridge at row 2

for T in range(1, 11):
    solver = Solver()
    solver.set("timeout", 30000)

    # Position variables for each robot at each time step
    row = [[Int(f'row_{r}_{t}') for t in range(T+1)] for r in range(n_robots)]
    col = [[Int(f'col_{r}_{t}') for t in range(T+1)] for r in range(n_robots)]

    # Which robot moves and in what direction at each step
    moved = [Int(f'moved_{t}') for t in range(T)]
    direction = [Int(f'dir_{t}') for t in range(T)]  # 0=up, 1=down, 2=left, 3=right

    # Initial positions
    solver.add(row[0][0] == 0, col[0][0] == 1)  # A at (0,1)
    solver.add(row[1][0] == 1, col[1][0] == 1)  # B at (1,1)
    solver.add(row[2][0] == 3, col[2][0] == 1)  # C at (3,1)

    # Grid bounds for all positions at all times
    for t in range(T+1):
        for r in range(n_robots):
            solver.add(row[r][t] >= 0, row[r][t] <= 4)
            solver.add(col[r][t] >= 0, col[r][t] <= 4)

    for t in range(T):
        # Valid robot and direction indices
        solver.add(moved[t] >= 0, moved[t] <= 2)
        solver.add(direction[t] >= 0, direction[t] <= 3)

        for r in range(n_robots):
            is_mover = (moved[t] == r)

            # Movement effects: up (row-1), down (row+1), left (col-1), right (col+1)
            solver.add(Implies(And(is_mover, direction[t] == 0),
                              And(row[r][t+1] == row[r][t] - 1, col[r][t+1] == col[r][t])))
            solver.add(Implies(And(is_mover, direction[t] == 1),
                              And(row[r][t+1] == row[r][t] + 1, col[r][t+1] == col[r][t])))
            solver.add(Implies(And(is_mover, direction[t] == 2),
                              And(row[r][t+1] == row[r][t], col[r][t+1] == col[r][t] - 1)))
            solver.add(Implies(And(is_mover, direction[t] == 3),
                              And(row[r][t+1] == row[r][t], col[r][t+1] == col[r][t] + 1)))

            # Non-moving robot stays in place
            solver.add(Implies(moved[t] != r,
                              And(row[r][t+1] == row[r][t], col[r][t+1] == col[r][t])))

            # Grid boundary constraints
            solver.add(Implies(And(is_mover, direction[t] == 0), row[r][t] > 0))
            solver.add(Implies(And(is_mover, direction[t] == 1), row[r][t] < 4))
            solver.add(Implies(And(is_mover, direction[t] == 2), col[r][t] > 0))
            solver.add(Implies(And(is_mover, direction[t] == 3), col[r][t] < 4))

            # Wall: between col 0 and col 1 (all rows) - blocks right from col 0 and left from col 1
            solver.add(Not(And(is_mover, direction[t] == 3, col[r][t] == 0)))
            solver.add(Not(And(is_mover, direction[t] == 2, col[r][t] == 1)))

            # Wall: between col 1 and col 2 (rows 0,1,3,4) - bridge at row 2
            for wr in wall_rows_col12:
                solver.add(Not(And(is_mover, direction[t] == 3, col[r][t] == 1, row[r][t] == wr)))
                solver.add(Not(And(is_mover, direction[t] == 2, col[r][t] == 2, row[r][t] == wr)))

            # Wall: between col 2 and col 3 (rows 0,1,3,4) - bridge at row 2
            for wr in wall_rows_col23:
                solver.add(Not(And(is_mover, direction[t] == 3, col[r][t] == 2, row[r][t] == wr)))
                solver.add(Not(And(is_mover, direction[t] == 2, col[r][t] == 3, row[r][t] == wr)))

        # No collisions: all robots at distinct positions after each move
        for i in range(n_robots):
            for j in range(i+1, n_robots):
                solver.add(Or(row[i][t+1] != row[j][t+1], col[i][t+1] != col[j][t+1]))

    # Goal: Robot A must be at (2, 3) after all T moves
    solver.add(row[0][T] == 2, col[0][T] == 3)

    result = solver.check()
    if result == sat:
        m = solver.model()
        print("STATUS: sat")
        print(f"solution_found: True")
        print(f"moves: {T}")

        print("sequence:")
        for t in range(T):
            r_idx = m.evaluate(moved[t]).as_long()
            d = m.evaluate(direction[t]).as_long()
            robot_name = robots[r_idx]
            fr = m.evaluate(row[r_idx][t]).as_long()
            fc = m.evaluate(col[r_idx][t]).as_long()
            tr = m.evaluate(row[r_idx][t+1]).as_long()
            tc = m.evaluate(col[r_idx][t+1]).as_long()
            dir_name = ['up', 'down', 'left', 'right'][d]
            print(f"  Step {t+1}: {robot_name} moves {dir_name} from ({fr},{fc}) to ({tr},{tc})")

        print("final_positions:")
        for r in range(n_robots):
            fr = m.evaluate(row[r][T]).as_long()
            fc = m.evaluate(col[r][T]).as_long()
            print(f"  {robots[r]}: [{fr}, {fc}]")
        break
    elif result == unknown:
        print(f"T={T}: unknown (timeout)")
        continue
    else:
        print(f"T={T}: unsat")
        continue
else:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (no solution found up to T=10)")