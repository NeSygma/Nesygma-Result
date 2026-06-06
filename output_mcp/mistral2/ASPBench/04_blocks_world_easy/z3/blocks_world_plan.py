from z3 import *

# BENCHMARK_MODE: ON (model-finding mode)
BENCHMARK_MODE = True

# --- Problem Constants ---
blocks = ['A', 'B', 'C']
table = 'table'

# --- Solver Setup ---
# We will try T = 1, 2, 3, ... until a solution is found

for max_T in range(1, 5):
    s = Solver()

    # --- Decision Variables ---
    # on[t][block]: block or table below 'block' at time t
    on = [[String(f'on_{t}_{b}') for b in blocks] for t in range(max_T + 1)]

    # clear[t][block]: whether 'block' is clear at time t
    clear = [[Bool(f'clear_{t}_{b}') for b in blocks] for t in range(max_T + 1)]

    # holding[t]: block being held at time t (or table)
    holding = [String(f'holding_{t}') for t in range(max_T + 1)]

    # action[t]: (block, from, to) or (None, None, None)
    action_block = [String(f'action_block_{t}') for t in range(max_T)]
    action_from = [String(f'action_from_{t}') for t in range(max_T)]
    action_to = [String(f'action_to_{t}') for t in range(max_T)]

    # --- Helper Functions ---
    def is_table(x):
        return x == table

    def is_block(x):
        return Or([x == b for b in blocks])

    # --- Initial State ---
    # Initial on positions
    s.add(on[0][0] == table)  # A is on table
    s.add(on[0][1] == table)  # B is on table
    s.add(on[0][2] == 'A')    # C is on A

    # Initial clearness
    s.add(clear[0][0] == True)  # A is clear (nothing on top)
    s.add(clear[0][1] == True)  # B is clear
    s.add(clear[0][2] == False) # C is not clear (A is on it)

    # Initial holding
    s.add(holding[0] == table)   # No block is held

    # --- Goal State ---
    goal_constraints = []
    goal_constraints.append(on[max_T][0] == 'B')  # A is on B
    goal_constraints.append(on[max_T][1] == 'C')  # B is on C
    goal_constraints.append(on[max_T][2] == table) # C is on table
    goal_constraints.append(clear[max_T][0] == False) # A has B on top
    goal_constraints.append(clear[max_T][1] == False) # B has C on top
    goal_constraints.append(clear[max_T][2] == True)   # C is clear
    s.add(And(goal_constraints))

    # --- No self-placement ---
    for t in range(max_T + 1):
        for i, b in enumerate(blocks):
            s.add(on[t][i] != b)

    # --- No cycles ---
    for t in range(max_T + 1):
        for i, b1 in enumerate(blocks):
            for j, b2 in enumerate(blocks):
                if i != j:
                    s.add(Implies(on[t][i] == b2, on[t][j] != b1))

    # --- Action Semantics ---
    for t in range(max_T):
        # If an action is taken at time t, encode its effects
        for i, b in enumerate(blocks):
            # Action: move block b from 'from_pos' to 'to_pos'
            from_pos = on[t][i]
            s.add(Implies(
                And(
                    action_block[t] == b,
                    action_from[t] == from_pos,
                    action_to[t] != from_pos,
                    clear[t][i]  # Block is clear
                ),
                And(
                    on[t+1][i] == action_to[t],
                    clear[t+1][i] == True,  # After moving, the block is clear (nothing on top)
                    # Update 'from' position clearness if it's a block
                    If(
                        is_block(from_pos),
                        clear[t+1][blocks.index(from_pos)] == True,
                        True
                    ),
                    # Update 'to' position clearness
                    If(
                        is_block(action_to[t]),
                        clear[t+1][blocks.index(action_to[t])] == False,
                        True
                    ),
                    holding[t+1] == table  # No block is held after the move
                )
            ))
        # If no action is taken, state persists
        s.add(Implies(
            And(
                action_block[t] == table,  # No-op
                holding[t] == table
            ),
            And(
                on[t+1][0] == on[t][0],
                on[t+1][1] == on[t][1],
                on[t+1][2] == on[t][2],
                clear[t+1][0] == clear[t][0],
                clear[t+1][1] == clear[t][1],
                clear[t+1][2] == clear[t][2],
                holding[t+1] == table
            )
        ))

    # Check if a plan exists for this T
    if s.check() == sat:
        model = s.model()
        print("STATUS: sat")
        print(f"plan_length = {max_T}")

        # Extract the plan
        plan = []
        for t in range(max_T):
            block = model[action_block[t]]
            from_pos = model[action_from[t]]
            to_pos = model[action_to[t]]
            if block != table:
                plan.append(f"move({block}, {from_pos}, {to_pos})")
        print("actions =", plan)
        break
else:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")