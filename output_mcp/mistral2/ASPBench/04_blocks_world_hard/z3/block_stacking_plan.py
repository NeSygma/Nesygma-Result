from z3 import *

# Block labels: A=0, B=1, ..., L=11
blocks = list(range(12))
block_names = [chr(ord('A') + i) for i in blocks]
block_weights = {i: i+1 for i in blocks}  # A=1, B=2, ..., L=12

# Initial and goal configurations as lists of stacks (each stack is a list of blocks from bottom to top)
# Initial Configuration:
# Stack 1: D on table, C on D, B on C, A on B  => [D, C, B, A]
# Stack 2: H on table, G on H, F on G, E on F  => [H, G, F, E]
# Stack 3: L on table, K on L, J on K, I on J  => [L, K, J, I]
initial_stacks = [
    [3, 2, 1, 0],  # D, C, B, A
    [7, 6, 5, 4],  # H, G, F, E
    [11, 10, 9, 8] # L, K, J, I
]

# Goal Configuration:
# Tower 1: L on table, I on L, F on I, C on F  => [L, I, F, C]
# Tower 2: K on table, H on K, E on H, B on E  => [K, H, E, B]
# Tower 3: J on table, G on J, D on G, A on D  => [J, G, D, A]
goal_stacks = [
    [11, 9, 6, 2],  # L, I, F, C
    [10, 7, 4, 1],  # K, H, E, B
    [9, 6, 3, 0]    # J, G, D, A
]

# Maximum plan length
MAX_PLAN_LENGTH = 50

# Helper: Is a block clear at a given time step?
# We'll represent the "on top of" relation as an array: on_top[t][block] = block_on_top or -1 if none
# We'll also represent the stack structure as an array: stack[t][block] = stack_index (0,1,2) or -1 if not on any stack

# We'll use a solver to search for a valid plan
solver = Solver()

# Decision variables:
# - plan_length: the actual number of moves (0 <= plan_length <= MAX_PLAN_LENGTH)
plan_length = Int('plan_length')
solver.add(plan_length >= 0, plan_length <= MAX_PLAN_LENGTH)

# For each time step t in [0, plan_length], we have:
# - on_top[t][block]: the block directly on top of 'block' at step t, or -1 if none
# - stack[t][block]: the stack index (0,1,2) that 'block' belongs to at step t, or -1 if not on any stack
# - clear[t][block]: whether 'block' is clear (nothing on top) at step t

# We'll represent these as arrays of arrays
on_top = [[Int(f'on_top_{t}_{b}') for b in blocks] for t in range(MAX_PLAN_LENGTH + 1)]
stack = [[Int(f'stack_{t}_{b}') for b in blocks] for t in range(MAX_PLAN_LENGTH + 1)]
clear = [[Bool(f'clear_{t}_{b}') for b in blocks] for t in range(MAX_PLAN_LENGTH + 1)]

# Action variables for each step t in [1, plan_length]:
# - move_block[t]: the block being moved (or -1 if no move)
# - move_from[t]: the source position: -1 for table, or a block index
# - move_to[t]: the target position: -1 for table, or a block index
move_block = [Int(f'move_block_{t}') for t in range(MAX_PLAN_LENGTH + 1)]
move_from = [Int(f'move_from_{t}') for t in range(MAX_PLAN_LENGTH + 1)]
move_to = [Int(f'move_to_{t}') for t in range(MAX_PLAN_LENGTH + 1)]

# Initialize step 0 to the initial configuration
for b in blocks:
    # Initial stack assignments
    for sidx in range(3):
        solver.add(Or([stack[0][b] == sidx] + [stack[0][b] == -1]))
    # Position in stack: index in the list
    for sidx, stack_b in enumerate(initial_stacks):
        if b in stack_b:
            solver.add(stack[0][b] == sidx)
            pos_in_stack = stack_b.index(b)
            # Blocks below: must have this block on top
            if pos_in_stack > 0:
                below = stack_b[pos_in_stack - 1]
                solver.add(on_top[0][below] == b)
            else:
                solver.add(on_top[0][b] == -1)  # bottom block
    # If not in any stack, assign to -1 (should not happen)
    solver.add(Or([stack[0][b] == sidx for sidx in range(3)] + [stack[0][b] == -1]))

# Clear at step 0: a block is clear if nothing is on top of it
for b in blocks:
    solver.add(clear[0][b] == (on_top[0][b] == -1))

# Goal configuration at step plan_length
for b in blocks:
    for sidx, goal_stack in enumerate(goal_stacks):
        if b in goal_stack:
            solver.add(stack[plan_length][b] == sidx)
            pos_in_stack = goal_stack.index(b)
            if pos_in_stack > 0:
                below = goal_stack[pos_in_stack - 1]
                solver.add(on_top[plan_length][below] == b)
            else:
                solver.add(on_top[plan_length][b] == -1)
    solver.add(Or([stack[plan_length][b] == sidx for sidx in range(3)] + [stack[plan_length][b] == -1]))

# Clear at goal step: same as above
for b in blocks:
    solver.add(clear[plan_length][b] == (on_top[plan_length][b] == -1))

# For each time step t from 1 to plan_length, define the action and state transition
for t in range(1, MAX_PLAN_LENGTH + 1):
    # If t > plan_length, no-op (but we will only enforce constraints up to plan_length)
    if t <= plan_length:
        # Action variables: move_block[t], move_from[t], move_to[t]
        # move_block[t] is the block being moved, or -1 if no move
        solver.add(Or(move_block[t] == -1, And(move_block[t] >= 0, move_block[t] < 12)))
        solver.add(Or(move_from[t] == -1, And(move_from[t] >= 0, move_from[t] < 12)))
        solver.add(Or(move_to[t] == -1, And(move_to[t] >= 0, move_to[t] < 12)))
        
        # Only one move per step: if move_block[t] != -1, then a move occurs
        # Constraints for the move:
        # 1. The block must be clear at step t-1
        solver.add(Implies(move_block[t] != -1, clear[t-1][move_block[t]]))
        
        # 2. The source must be correct: if move_from[t] != -1, then move_from[t] must be the block currently directly below move_block[t] at step t-1
        #    If move_from[t] == -1, then the block is on the table at step t-1
        for b in blocks:
            # If b is the block being moved, its source must match move_from[t]
            solver.add(Implies(
                And(move_block[t] == b, move_block[t] != -1),
                Or(
                    And(move_from[t] == -1, stack[t-1][b] == -1),  # on table
                    And(move_from[t] >= 0, on_top[t-1][move_from[t]] == b)
                )
            ))
        
        # 3. The target must be valid: if move_to[t] != -1, then move_to[t] must be clear at step t-1
        for b in blocks:
            solver.add(Implies(
                And(move_to[t] == b, move_to[t] != -1),
                clear[t-1][b]
            ))
        
        # 4. Weight constraint: if placing b on c (c != -1), then weight(c) >= weight(b)
        for b in blocks:
            for c in blocks:
                solver.add(Implies(
                    And(move_block[t] == b, move_to[t] == c, move_block[t] != -1, move_to[t] != -1),
                    block_weights[c] >= block_weights[b]
                ))
        
        # 5. Table limit: at most 6 blocks directly on the table at step t
        # Count the number of blocks with stack[t][b] == -1 (on table)
        table_blocks = [If(stack[t][b] == -1, 1, 0) for b in blocks]
        solver.add(Sum(table_blocks) <= 6)
        
        # 6. Height limit: no tower exceeds height 5
        # For each stack, count the number of blocks in it
        for sidx in range(3):
            stack_size = Sum([If(stack[t][b] == sidx, 1, 0) for b in blocks])
            solver.add(stack_size <= 5)
        
        # 7. Distinct positions: move_from[t] != move_to[t] if both are blocks
        solver.add(Not(And(move_from[t] != -1, move_to[t] != -1, move_from[t] == move_to[t])))
        
        # 8. Update state after the move
        # We need to update on_top, stack, and clear for step t based on the move
        # This is complex; we'll use the following approach:
        # - For the moved block, it is now on top of move_to[t] (or on table if move_to[t] == -1)
        # - The block that was on top of move_to[t] (if any) is no longer on top of it
        # - The moved block is no longer on top of its previous block (if any)
        # - The moved block is now in the stack of move_to[t] (or on table)
        # - Clear statuses are updated accordingly
        
        # We'll add these as constraints for the moved block and affected blocks
        for b in blocks:
            # If b is the moved block
            if b == move_block[t] and move_block[t] != -1:
                # After move, b is on top of move_to[t] (or on table)
                solver.add(Or(
                    And(move_to[t] == -1, stack[t][b] == -1, on_top[t][b] == -1),  # on table
                    And(move_to[t] != -1, on_top[t][move_to[t]] == b, stack[t][b] == stack[t][move_to[t]])
                ))
                # b is no longer on top of its previous block (if any)
                solver.add(Or(
                    And(move_from[t] == -1, on_top[t][b] == -1),  # was on table, now on target
                    And(move_from[t] != -1, on_top[t][move_from[t]] != b)
                ))
            else:
                # For other blocks, on_top and stack are the same as step t-1, unless they are affected by the move
                # If b is move_to[t], its on_top is updated to b (the moved block)
                solver.add(Implies(
                    b == move_to[t] and move_to[t] != -1 and move_block[t] != -1,
                    on_top[t][b] == move_block[t]
                ))
                # If b is move_from[t] and it's a block, its on_top is updated to whatever was on top of it before (if any)
                solver.add(Implies(
                    b == move_from[t] and move_from[t] != -1 and move_block[t] != -1,
                    on_top[t][b] == on_top[t-1][b]
                ))
                # For all other blocks, on_top and stack remain the same
                solver.add(Implies(
                    And(b != move_block[t], b != move_from[t], b != move_to[t]),
                    And(on_top[t][b] == on_top[t-1][b], stack[t][b] == stack[t-1][b])
                ))
        
        # Update stack assignments for the moved block
        for b in blocks:
            if b == move_block[t] and move_block[t] != -1:
                solver.add(Or(
                    And(move_to[t] == -1, stack[t][b] == -1),  # on table
                    And(move_to[t] != -1, stack[t][b] == stack[t][move_to[t]])
                ))
            else:
                solver.add(stack[t][b] == stack[t-1][b])
        
        # Update clear statuses
        for b in blocks:
            # The moved block is not clear after the move (unless it's on the table and nothing else is on it, but it's on top of something)
            solver.add(Implies(
                b == move_block[t] and move_block[t] != -1,
                Not(clear[t][b])
            ))
            # The block that was on top of move_to[t] (if any) is now clear
            solver.add(Implies(
                And(move_to[t] != -1, move_block[t] != -1, on_top[t-1][move_to[t]] != -1),
                clear[t][on_top[t-1][move_to[t]]]
            ))
            # The block that was below the moved block (if any) is now clear
            solver.add(Implies(
                And(move_from[t] != -1, move_block[t] != -1, on_top[t][move_from[t]] == move_block[t]),
                clear[t][move_from[t]]
            ))
            # For all other blocks, clear status is the same as step t-1
            solver.add(Implies(
                And(b != move_block[t], b != move_from[t], b != move_to[t]),
                clear[t][b] == clear[t-1][b]
            ))
    else:
        # For t > plan_length, state remains the same as step plan_length
        for b in blocks:
            solver.add(stack[t][b] == stack[plan_length][b])
            solver.add(on_top[t][b] == on_top[plan_length][b])
            solver.add(clear[t][b] == clear[plan_length][b])

# Optimize for a plan of minimal length (optional, but helps)
solver.push()
solver.add(plan_length < MAX_PLAN_LENGTH)
result = solver.check()
if result == sat:
    model = solver.model()
    actual_plan_length = model[plan_length].as_long()
    print("STATUS: sat")
    print(f"Plan length: {actual_plan_length}")
    
    # Extract the plan
    actions = []
    for t in range(1, actual_plan_length + 1):
        mb = model[move_block[t]]
        mf = model[move_from[t]]
        mt = model[move_to[t]]
        if mb is not None and mb.as_long() != -1:
            block = block_names[mb.as_long()]
            from_pos = "table" if mf is None or mf.as_long() == -1 else block_names[mf.as_long()]
            to_pos = "table" if mt is None or mt.as_long() == -1 else block_names[mt.as_long()]
            actions.append({
                "step": t,
                "action": "move",
                "block": block,
                "from": from_pos,
                "to": to_pos
            })
    print("actions:")
    for act in actions:
        print(act)
    solver.pop()
else:
    solver.pop()
    # Try with full MAX_PLAN_LENGTH
    result = solver.check()
    if result == sat:
        model = solver.model()
        actual_plan_length = model[plan_length].as_long()
        print("STATUS: sat")
        print(f"Plan length: {actual_plan_length}")
        
        # Extract the plan
        actions = []
        for t in range(1, actual_plan_length + 1):
            mb = model[move_block[t]]
            mf = model[move_from[t]]
            mt = model[move_to[t]]
            if mb is not None and mb.as_long() != -1:
                block = block_names[mb.as_long()]
                from_pos = "table" if mf is None or mf.as_long() == -1 else block_names[mf.as_long()]
                to_pos = "table" if mt is None or mt.as_long() == -1 else block_names[mt.as_long()]
                actions.append({
                    "step": t,
                    "action": "move",
                    "block": block,
                    "from": from_pos,
                    "to": to_pos
                })
        print("actions:")
        for act in actions:
            print(act)
    else:
        print("STATUS: unknown")
        if result == unsat:
            print("RAW_RESULT: unsat")
        else:
            print("RAW_RESULT: unknown")