from z3 import *

# BENCHMARK_MODE: ON (model-finding mode)
BENCHMARK_MODE = True

# --- Problem Constants ---
blocks = ['A', 'B', 'C']
table = 0  # Represent table as 0
block_to_int = {'A': 1, 'B': 2, 'C': 3}
int_to_block = {1: 'A', 2: 'B', 3: 'C'}

# --- Solver Setup ---
# We will try T = 1, 2, 3, ... until a solution is found

for max_T in range(1, 5):
    s = Solver()

    # --- Decision Variables ---
    # pos[t][b]: position of block b at time t (0=table, 1=A, 2=B, 3=C)
    pos = [[Int(f'pos_{t}_{b}') for b in blocks] for t in range(max_T + 1)]

    # clear[t][b]: whether block b is clear at time t
    clear = [[Bool(f'clear_{t}_{b}') for b in blocks] for t in range(max_T + 1)]

    # holding[t]: block being held at time t (0=none, 1=A, 2=B, 3=C)
    holding = [Int(f'holding_{t}') for t in range(max_T + 1)]

    # action[t]: (block, from, to) or (None, None, None)
    action_block = [Int(f'action_block_{t}') for t in range(max_T)]
    action_from = [Int(f'action_from_{t}') for t in range(max_T)]
    action_to = [Int(f'action_to_{t}') for t in range(max_T)]

    # --- Helper Functions ---
    def is_table(x):
        return x == 0

    def is_block(x):
        return Or([x == block_to_int[b] for b in blocks])

    # --- Initial State ---
    # Initial positions
    s.add(pos[0][blocks.index('A')] == 0)  # A is on table
    s.add(pos[0][blocks.index('B')] == 0)  # B is on table
    s.add(pos[0][blocks.index('C')] == block_to_int['A'])  # C is on A

    # Initial clearness
    s.add(clear[0][blocks.index('A')] == True)  # A is clear
    s.add(clear[0][blocks.index('B')] == True)  # B is clear
    s.add(clear[0][blocks.index('C')] == False) # C is not clear

    # Initial holding
    s.add(holding[0] == 0)   # No block is held

    # --- Goal State ---
    goal_constraints = []
    goal_constraints.append(pos[max_T][blocks.index('A')] == block_to_int['B'])  # A is on B
    goal_constraints.append(pos[max_T][blocks.index('B')] == block_to_int['C'])  # B is on C
    goal_constraints.append(pos[max_T][blocks.index('C')] == 0)  # C is on table
    goal_constraints.append(clear[max_T][blocks.index('A')] == False) # A has B on top
    goal_constraints.append(clear[max_T][blocks.index('B')] == False) # B has C on top
    goal_constraints.append(clear[max_T][blocks.index('C')] == True)   # C is clear
    s.add(And(goal_constraints))

    # --- No self-placement ---
    for t in range(max_T + 1):
        for i, b in enumerate(blocks):
            s.add(pos[t][i] != block_to_int[b])

    # --- No cycles ---
    for t in range(max_T + 1):
        for i, b1 in enumerate(blocks):
            for j, b2 in enumerate(blocks):
                if i != j:
                    s.add(Implies(pos[t][i] == block_to_int[b2], pos[t][j] != block_to_int[b1]))

    # --- Action Semantics ---
    for t in range(max_T):
        # If an action is taken at time t, encode its effects
        for i, b in enumerate(blocks):
            # Action: move block b from 'from_pos' to 'to_pos'
            from_pos = pos[t][i]
            s.add(Implies(
                And(
                    action_block[t] == block_to_int[b],
                    action_from[t] == from_pos,
                    action_to[t] != from_pos,
                    clear[t][i],  # Block is clear
                    holding[t] == 0  # No block is currently held
                ),
                And(
                    pos[t+1][i] == action_to[t],
                    clear[t+1][i] == True,  # After moving, the block is clear
                    # Update 'from' position clearness if it's a block
                    If(
                        is_block(from_pos),
                        clear[t+1][blocks.index(int_to_block[from_pos])] == True,
                        True
                    ),
                    # Update 'to' position clearness
                    If(
                        is_block(action_to[t]),
                        clear[t+1][blocks.index(int_to_block[action_to[t]])] == False,
                        True
                    ),
                    holding[t+1] == 0  # No block is held after the move
                )
            ))
        # If no action is taken, state persists
        s.add(Implies(
            And(
                action_block[t] == 0,  # No-op
                holding[t] == 0
            ),
            And(
                pos[t+1][blocks.index('A')] == pos[t][blocks.index('A')],
                pos[t+1][blocks.index('B')] == pos[t][blocks.index('B')],
                pos[t+1][blocks.index('C')] == pos[t][blocks.index('C')],
                clear[t+1][blocks.index('A')] == clear[t][blocks.index('A')],
                clear[t+1][blocks.index('B')] == clear[t][blocks.index('B')],
                clear[t+1][blocks.index('C')] == clear[t][blocks.index('C')],
                holding[t+1] == 0
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
            if block.as_long() != 0:
                plan.append(f"move({int_to_block[block.as_long()]}, {int_to_block[from_pos.as_long()] if from_pos.as_long() != 0 else 'table'}, {int_to_block[to_pos.as_long()] if to_pos.as_long() != 0 else 'table'})")
        print("actions =", plan)
        break
else:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")