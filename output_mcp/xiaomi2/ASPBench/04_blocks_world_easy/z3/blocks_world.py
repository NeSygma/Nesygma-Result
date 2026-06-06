from z3 import *

solver = Optimize()

N = 3  # blocks: A=0, B=1, C=2
T = 5  # max time steps (generous upper bound)
TABLE = 3

# State: on[b][t] = what block b is on at time t (block index or TABLE)
on = [[Int(f'on_{b}_{t}') for t in range(T+1)] for b in range(N)]

# Move indicator: did block b move at step t?
moved = [[Bool(f'moved_{b}_{t}') for t in range(T)] for b in range(N)]

# Height for acyclicity enforcement
height = [[Int(f'h_{b}_{t}') for t in range(T+1)] for b in range(N)]

# --- Domain constraints ---
for b in range(N):
    for t in range(T+1):
        solver.add(on[b][t] >= 0, on[b][t] <= TABLE)
        solver.add(on[b][t] != b)  # no block on itself
        solver.add(height[b][t] >= 0, height[b][t] <= N)

# --- Initial State ---
solver.add(on[0][0] == TABLE)  # A on table
solver.add(on[1][0] == TABLE)  # B on table
solver.add(on[2][0] == 0)      # C on A

# --- Goal State ---
solver.add(on[0][T] == 1)      # A on B
solver.add(on[1][T] == 2)      # B on C
solver.add(on[2][T] == TABLE)  # C on table

# --- Structural: at most one block on top of any block ---
for t in range(T+1):
    for b in range(N):
        solver.add(Sum([If(on[j][t] == b, 1, 0) for j in range(N)]) <= 1)

# --- Acyclicity via height ordering ---
for t in range(T+1):
    for b in range(N):
        solver.add(Implies(on[b][t] == TABLE, height[b][t] == 0))
        for c in range(N):
            solver.add(Implies(on[b][t] == c, height[b][t] == height[c][t] + 1))

# --- Transition constraints ---
for t in range(T):
    # At most one block moves per step
    solver.add(Sum([If(moved[b][t], 1, 0) for b in range(N)]) <= 1)

    for b in range(N):
        # moved[b][t] iff position changed
        solver.add(moved[b][t] == (on[b][t+1] != on[b][t]))

        # If moved, block must be clear (nothing on top of it at time t)
        solver.add(Implies(moved[b][t],
                          And([on[j][t] != b for j in range(N)])))

        # If moved to another block c, c must be clear at time t
        for c in range(N):
            solver.add(Implies(And(moved[b][t], on[b][t+1] == c),
                              And([on[j][t] != c for j in range(N)])))

        # If not moved, position stays the same
        solver.add(Implies(Not(moved[b][t]), on[b][t+1] == on[b][t]))

# --- Minimize total number of moves ---
total_moves = Sum([If(moved[b][t], 1, 0) for b in range(N) for t in range(T)])
solver.minimize(total_moves)

# --- Solve ---
result = solver.check()

if result == sat:
    m = solver.model()
    print("STATUS: sat")
    tm = m.evaluate(total_moves)
    print(f"plan_length: {tm}")

    block_names = ['A', 'B', 'C']
    step = 1
    for t in range(T):
        for b in range(N):
            if is_true(m.evaluate(moved[b][t])):
                from_val = m.evaluate(on[b][t]).as_long()
                to_val = m.evaluate(on[b][t+1]).as_long()
                from_name = 'table' if from_val == TABLE else block_names[from_val]
                to_name = 'table' if to_val == TABLE else block_names[to_val]
                print(f"step {step}: move {block_names[b]} from {from_name} to {to_name}")
                step += 1

    # Print full state trace for verification
    print("\n--- Full State Trace ---")
    for t in range(T+1):
        print(f"Time {t}:")
        for b in range(N):
            pos = m.evaluate(on[b][t]).as_long()
            pos_name = 'table' if pos == TABLE else block_names[pos]
            print(f"  {block_names[b]} is on {pos_name}")
else:
    print("STATUS: unsat")
    print("No valid plan found.")