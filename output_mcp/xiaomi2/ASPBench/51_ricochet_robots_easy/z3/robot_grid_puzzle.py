from z3 import *

solver = Optimize()

MAX_MOVES = 10

# State at each time step (0..MAX_MOVES)
row_A = [Int(f'row_A_{t}') for t in range(MAX_MOVES + 1)]
col_A = [Int(f'col_A_{t}') for t in range(MAX_MOVES + 1)]
row_B = [Int(f'row_B_{t}') for t in range(MAX_MOVES + 1)]
col_B = [Int(f'col_B_{t}') for t in range(MAX_MOVES + 1)]

# Move descriptors for each step
mover = [Int(f'mover_{t}') for t in range(MAX_MOVES)]      # 0=A, 1=B
direction = [Int(f'dir_{t}') for t in range(MAX_MOVES)]     # 0=up,1=down,2=left,3=right

# Active move flags
active = [Bool(f'active_{t}') for t in range(MAX_MOVES)]

# --- Initial positions ---
solver.add(row_A[0] == 0, col_A[0] == 1)
solver.add(row_B[0] == 1, col_B[0] == 1)

# --- Grid bounds (0-3 for both row and col) ---
for t in range(MAX_MOVES + 1):
    solver.add(row_A[t] >= 0, row_A[t] <= 3)
    solver.add(col_A[t] >= 0, col_A[t] <= 3)
    solver.add(row_B[t] >= 0, row_B[t] <= 3)
    solver.add(col_B[t] >= 0, col_B[t] <= 3)

# --- No collision: robots cannot share a cell ---
for t in range(MAX_MOVES + 1):
    solver.add(Not(And(row_A[t] == row_B[t], col_A[t] == col_B[t])))

# --- Active moves must be contiguous (no gaps) ---
for t in range(1, MAX_MOVES):
    solver.add(Implies(active[t], active[t - 1]))

# --- Transition constraints ---
# Direction deltas: up=(-1,0), down=(1,0), left=(0,-1), right=(0,1)
deltas = [(-1, 0), (1, 0), (0, -1), (0, 1)]

for t in range(MAX_MOVES):
    # If not active, positions stay the same
    solver.add(Implies(Not(active[t]), And(
        row_A[t + 1] == row_A[t], col_A[t + 1] == col_A[t],
        row_B[t + 1] == row_B[t], col_B[t + 1] == col_B[t]
    )))

    # If active, mover in {0,1}, direction in {0,1,2,3}
    solver.add(Implies(active[t], And(
        mover[t] >= 0, mover[t] <= 1,
        direction[t] >= 0, direction[t] <= 3
    )))

    # Movement effects for each robot and direction
    for m_val in [0, 1]:  # 0=A, 1=B
        for d_val, (dr, dc) in enumerate(deltas):
            if m_val == 0:
                solver.add(Implies(
                    And(active[t], mover[t] == 0, direction[t] == d_val),
                    And(
                        row_A[t + 1] == row_A[t] + dr,
                        col_A[t + 1] == col_A[t] + dc,
                        row_B[t + 1] == row_B[t],
                        col_B[t + 1] == col_B[t]
                    )
                ))
            else:
                solver.add(Implies(
                    And(active[t], mover[t] == 1, direction[t] == d_val),
                    And(
                        row_B[t + 1] == row_B[t] + dr,
                        col_B[t + 1] == col_B[t] + dc,
                        row_A[t + 1] == row_A[t],
                        col_A[t + 1] == col_A[t]
                    )
                ))

# --- Wall constraints ---
# Wall between column 1 and column 2 at rows 0 and 1
# Blocks: (r,1) <-> (r,2) for r in {0, 1}
for t in range(MAX_MOVES):
    for r in [0, 1]:
        for m_val in [0, 1]:
            pos_r = row_A if m_val == 0 else row_B
            pos_c = col_A if m_val == 0 else col_B
            # Can't move right from (r,1) to (r,2)
            solver.add(Implies(
                And(active[t], mover[t] == m_val),
                Not(And(pos_r[t] == r, pos_c[t] == 1, direction[t] == 3))
            ))
            # Can't move left from (r,2) to (r,1)
            solver.add(Implies(
                And(active[t], mover[t] == m_val),
                Not(And(pos_r[t] == r, pos_c[t] == 2, direction[t] == 2))
            ))

# --- Goal: Robot A must reach (2,1) at some time step ---
goal_t = [Bool(f'goal_{t}') for t in range(MAX_MOVES + 1)]
for t in range(MAX_MOVES + 1):
    solver.add(goal_t[t] == And(row_A[t] == 2, col_A[t] == 1))

solver.add(Or([goal_t[t] for t in range(MAX_MOVES + 1)]))

# --- Minimize total number of moves ---
num_active = Sum([If(active[t], 1, 0) for t in range(MAX_MOVES)])
solver.minimize(num_active)

# --- Solve ---
result = solver.check()

if result == sat:
    m = solver.model()
    n = m.eval(num_active).as_long()

    print("STATUS: sat")
    print(f"solution_found: True")
    print(f"moves: {n}")

    # Extract the move sequence
    print("sequence:")
    for t in range(n):
        mover_val = m.eval(mover[t]).as_long()
        robot = "A" if mover_val == 0 else "B"

        if mover_val == 0:
            r_from = m.eval(row_A[t]).as_long()
            c_from = m.eval(col_A[t]).as_long()
            r_to = m.eval(row_A[t + 1]).as_long()
            c_to = m.eval(col_A[t + 1]).as_long()
        else:
            r_from = m.eval(row_B[t]).as_long()
            c_from = m.eval(col_B[t]).as_long()
            r_to = m.eval(row_B[t + 1]).as_long()
            c_to = m.eval(col_B[t + 1]).as_long()

        print(f"  Step {t + 1}: Robot {robot} from [{r_from},{c_from}] to [{r_to},{c_to}]")

    # Final positions after all moves
    final_A_r = m.eval(row_A[n]).as_long()
    final_A_c = m.eval(col_A[n]).as_long()
    final_B_r = m.eval(row_B[n]).as_long()
    final_B_c = m.eval(col_B[n]).as_long()

    print(f"final_positions:")
    print(f"  A: [{final_A_r}, {final_A_c}]")
    print(f"  B: [{final_B_r}, {final_B_c}]")

    # Validation: verify goal is met
    goal_met = any(
        m.eval(And(row_A[t] == 2, col_A[t] == 1)) == True
        for t in range(n + 1)
    )
    print(f"goal_reached: {goal_met}")

elif result == unsat:
    print("STATUS: unsat")
    print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")