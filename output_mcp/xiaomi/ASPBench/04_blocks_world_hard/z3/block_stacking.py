from z3 import *

# Constants
NUM_BLOCKS = 12
BLOCK_NAMES = ['A','B','C','D','E','F','G','H','I','J','K','L']
BLOCK_IDX = {name: i for i, name in enumerate(BLOCK_NAMES)}
WEIGHTS = [1,2,3,4,5,6,7,8,9,10,11,12]  # A=1, B=2, ..., L=12
TABLE = NUM_BLOCKS  # special value for "on table"

MAX_MOVES = 50
MAX_TIME = MAX_MOVES + 1  # states: 0..MAX_MOVES

# We'll try increasing plan lengths
for plan_len in range(1, MAX_MOVES + 1):
    print(f"Trying plan length {plan_len}...")
    solver = Solver()
    solver.set("timeout", 120000)  # 2 minute timeout per attempt

    T = plan_len
    N = NUM_BLOCKS

    # Position of each block at each time step
    # pos[b][t] = which block b is on at time t, or TABLE (N) for table
    pos = [[Int(f'pos_{b}_{t}') for t in range(T+1)] for b in range(N)]

    # Domain constraints: each position is 0..N (N = table)
    for b in range(N):
        for t in range(T+1):
            solver.add(pos[b][t] >= 0, pos[b][t] <= N)

    # A block cannot be on itself
    for b in range(N):
        for t in range(T+1):
            solver.add(pos[b][t] != b)

    # Initial configuration
    # Stack 1: D on table, C on D, B on C, A on B
    solver.add(pos[BLOCK_IDX['D']][0] == TABLE)
    solver.add(pos[BLOCK_IDX['C']][0] == BLOCK_IDX['D'])
    solver.add(pos[BLOCK_IDX['B']][0] == BLOCK_IDX['C'])
    solver.add(pos[BLOCK_IDX['A']][0] == BLOCK_IDX['B'])

    # Stack 2: H on table, G on H, F on G, E on F
    solver.add(pos[BLOCK_IDX['H']][0] == TABLE)
    solver.add(pos[BLOCK_IDX['G']][0] == BLOCK_IDX['H'])
    solver.add(pos[BLOCK_IDX['F']][0] == BLOCK_IDX['G'])
    solver.add(pos[BLOCK_IDX['E']][0] == BLOCK_IDX['F'])

    # Stack 3: L on table, K on L, J on K, I on J
    solver.add(pos[BLOCK_IDX['L']][0] == TABLE)
    solver.add(pos[BLOCK_IDX['K']][0] == BLOCK_IDX['L'])
    solver.add(pos[BLOCK_IDX['J']][0] == BLOCK_IDX['K'])
    solver.add(pos[BLOCK_IDX['I']][0] == BLOCK_IDX['J'])

    # Goal configuration
    # Tower 1: L on table, I on L, F on I, C on F
    solver.add(pos[BLOCK_IDX['L']][T] == TABLE)
    solver.add(pos[BLOCK_IDX['I']][T] == BLOCK_IDX['L'])
    solver.add(pos[BLOCK_IDX['F']][T] == BLOCK_IDX['I'])
    solver.add(pos[BLOCK_IDX['C']][T] == BLOCK_IDX['F'])

    # Tower 2: K on table, H on K, E on H, B on E
    solver.add(pos[BLOCK_IDX['K']][T] == TABLE)
    solver.add(pos[BLOCK_IDX['H']][T] == BLOCK_IDX['K'])
    solver.add(pos[BLOCK_IDX['E']][T] == BLOCK_IDX['H'])
    solver.add(pos[BLOCK_IDX['B']][T] == BLOCK_IDX['E'])

    # Tower 3: J on table, G on J, D on G, A on D
    solver.add(pos[BLOCK_IDX['J']][T] == TABLE)
    solver.add(pos[BLOCK_IDX['G']][T] == BLOCK_IDX['J'])
    solver.add(pos[BLOCK_IDX['D']][T] == BLOCK_IDX['G'])
    solver.add(pos[BLOCK_IDX['A']][T] == BLOCK_IDX['D'])

    # Action variables: at each time step, which block moves, from where, to where
    move_block = [Int(f'move_block_{t}') for t in range(T)]
    move_from = [Int(f'move_from_{t}') for t in range(T)]
    move_to = [Int(f'move_to_{t}') for t in range(T)]

    for t in range(T):
        # move_block is 0..N-1 (a valid block)
        solver.add(move_block[t] >= 0, move_block[t] < N)
        # move_from and move_to are 0..N (N = table)
        solver.add(move_from[t] >= 0, move_from[t] <= N)
        solver.add(move_to[t] >= 0, move_to[t] <= N)
        # Source and destination must differ
        solver.add(move_from[t] != move_to[t])
        # Block cannot be placed on itself (move_to != move_block)
        solver.add(move_to[t] != move_block[t])

    # Transition constraints for each time step
    for t in range(T):
        mb = move_block[t]
        mf = move_from[t]
        mt = move_to[t]

        for b in range(N):
            # If block b is the one being moved
            # pos[b][t+1] = move_to[t]
            solver.add(Implies(mb == b, pos[b][t+1] == mt))
            # Before move: pos[b][t] == move_from[t]
            solver.add(Implies(mb == b, pos[b][t] == mf))

            # If block b is NOT being moved, position stays the same
            solver.add(Implies(mb != b, pos[b][t+1] == pos[b][t]))

    # Clear block constraint: only clear blocks can be moved
    # A block b is clear at time t if no other block is on top of it
    # i.e., for all other blocks c, pos[c][t] != b
    for t in range(T):
        mb = move_block[t]
        for b in range(N):
            # If mb == b, then b must be clear: no block c has pos[c][t] == b
            solver.add(Implies(mb == b,
                And([pos[c][t] != b for c in range(N)])))

    # Weight constraint: when placing block X on block Y, weight(Y) >= weight(X)
    # move_to[t] is the destination. If it's a block (not table), weight constraint applies
    for t in range(T):
        mb = move_block[t]
        mt = move_to[t]
        for y in range(N):
            # If move_to == y (placing on block y), then weight(y) >= weight(mb)
            solver.add(Implies(mt == y,
                Sum([If(mb == x, WEIGHTS[y] - WEIGHTS[x], 0) for x in range(N)]) >= 0))

    # Table limit: at most 6 blocks on table at any time
    for t in range(T+1):
        solver.add(Sum([If(pos[b][t] == TABLE, 1, 0) for b in range(N)]) <= 6)

    # Height limit: no tower exceeds height 5
    # We need to compute tower heights. A block's height = 1 + height of block it's on
    # Use iterative approach: height[b][t] = 1 if on table, else 1 + height[parent][t]
    # But this creates circular dependencies. Instead, bound depth directly.
    # A block at depth d means it's d levels above table. Max depth = 5.
    # We can encode: no chain of length > 5 exists.
    # For efficiency, we'll use depth variables.
    depth = [[Int(f'depth_{b}_{t}') for t in range(T+1)] for b in range(N)]
    for b in range(N):
        for t in range(T+1):
            solver.add(depth[b][t] >= 1, depth[b][t] <= 5)
            # If on table, depth = 1
            solver.add(Implies(pos[b][t] == TABLE, depth[b][t] == 1))
            # If on another block c, depth[b] = depth[c] + 1
            for c in range(N):
                solver.add(Implies(pos[b][t] == c, depth[b][t] == depth[c][t] + 1))

    # Structural constraint: no cycles in the "on" relation
    # At any time, the "on" relation forms a forest (DAG with table as roots)
    # We already prevent self-loops. For longer cycles, we can use depth bounds.
    # Since depth is bounded 1-5 and depth[b] = depth[parent]+1, cycles are impossible
    # (they'd require depth[b] > depth[b], contradiction).

    result = solver.check()
    if result == sat:
        m = solver.model()
        print(f"STATUS: sat")
        print(f"plan_length: {plan_len}")

        # Extract the plan
        actions = []
        for t in range(T):
            block_idx = m.evaluate(move_block[t]).as_long()
            from_idx = m.evaluate(move_from[t]).as_long()
            to_idx = m.evaluate(move_to[t]).as_long()

            block_name = BLOCK_NAMES[block_idx]
            from_name = "table" if from_idx == TABLE else BLOCK_NAMES[from_idx]
            to_name = "table" if to_idx == TABLE else BLOCK_NAMES[to_idx]

            actions.append({
                "step": t + 1,
                "action": "move",
                "block": block_name,
                "from": from_name,
                "to": to_name
            })

        print("\nPlan:")
        for act in actions:
            print(f"  Step {act['step']}: move {act['block']} from {act['from']} to {act['to']}")

        # Verify final state
        print("\nFinal state verification:")
        for b in range(N):
            p = m.evaluate(pos[b][T]).as_long()
            loc = "table" if p == TABLE else BLOCK_NAMES[p]
            print(f"  {BLOCK_NAMES[b]} on {loc}")

        break
    elif result == unsat:
        print(f"  No plan of length {plan_len} found.")
    else:
        print(f"  Solver returned unknown for length {plan_len}")
        break
else:
    print("STATUS: unsat")
    print("No plan found within 50 moves")