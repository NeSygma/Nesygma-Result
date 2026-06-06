from z3 import *

# Define blocks as integers 0-11 for simplicity
blocks = list(range(12))  # A=0, B=1, ..., L=11
weights = {i: i+1 for i in blocks}  # A=1, B=2, ..., L=12

# Maximum plan length
MAX_STEPS = 50

# Create solver
solver = Solver()

# State[t][b] = position of block b at time t
# We'll use a list of arrays: state[t] is an array of integers: state[t][b] = block under b, or -1 if b is on table or clear
state = [Array(f'state_{t}', IntSort(), IntSort()) for t in range(MAX_STEPS + 1)]

# Actions: for each step t (1..MAX_STEPS)
action_block = [Int(f'action_block_{t}') for t in range(1, MAX_STEPS + 1)]
action_from = [Int(f'action_from_{t}') for t in range(1, MAX_STEPS + 1)]  # -1 for table, otherwise block id
action_to = [Int(f'action_to_{t}') for t in range(1, MAX_STEPS + 1)]  # -1 for table, otherwise block id

# Initial state constraints
init_state = state[0]
# Stack 1: D on table, C on D, B on C, A on B
solver.add(init_state[0] == 1)  # A on B
solver.add(init_state[1] == 2)  # B on C
solver.add(init_state[2] == 3)  # C on D
solver.add(init_state[3] == -1)  # D on table
# Stack 2: H on table, G on H, F on G, E on F
solver.add(init_state[4] == 5)  # E on F
solver.add(init_state[5] == 6)  # F on G
solver.add(init_state[6] == 7)  # G on H
solver.add(init_state[7] == -1)  # H on table
# Stack 3: L on table, K on L, J on K, I on J
solver.add(init_state[8] == 9)  # I on J
solver.add(init_state[9] == 10)  # J on K
solver.add(init_state[10] == 11)  # K on L
solver.add(init_state[11] == -1)  # L on table

# Goal state constraints
goal_state = state[MAX_STEPS]
# Tower 1: L on table, I on L, F on I, C on F
solver.add(goal_state[2] == 5)  # C on F
solver.add(goal_state[5] == 8)  # F on I
solver.add(goal_state[8] == 11)  # I on L
solver.add(goal_state[11] == -1)  # L on table
# Tower 2: K on table, H on K, E on H, B on E
solver.add(goal_state[1] == 4)  # B on E
solver.add(goal_state[4] == 7)  # E on H
solver.add(goal_state[7] == 10)  # H on K
solver.add(goal_state[10] == -1)  # K on table
# Tower 3: J on table, G on J, D on G, A on D
solver.add(goal_state[0] == 3)  # A on D
solver.add(goal_state[3] == 6)  # D on G
solver.add(goal_state[6] == 9)  # G on J
solver.add(goal_state[9] == -1)  # J on table

# Transition constraints for each step t from 1 to MAX_STEPS
for t in range(1, MAX_STEPS + 1):
    prev_state = state[t-1]
    curr_state = state[t]
    
    # The block being moved must be at the 'from' position in the previous state
    solver.add(prev_state[action_block[t]] == action_from[t])
    
    # All other blocks remain in the same position
    for b in blocks:
        if b != action_block[t]:
            solver.add(curr_state[b] == prev_state[b])
    
    # The block being moved must be clear in the previous state
    # A block is clear if no other block has it as the block under it
    clear_constraints = []
    for b2 in blocks:
        if b2 != action_block[t]:
            clear_constraints.append(prev_state[b2] != action_block[t])
    solver.add(And(clear_constraints))
    
    # The target position must be clear (if it's not table)
    # If action_to[t] != -1, then no other block can have action_to[t] as the block under it
    if action_to[t] != -1:
        target_clear_constraints = []
        for b2 in blocks:
            if b2 != action_to[t]:
                target_clear_constraints.append(prev_state[b2] != action_to[t])
        solver.add(And(target_clear_constraints))
    
    # Weight constraint: if target is not table, then weight(block) <= weight(target)
    if action_to[t] != -1:
        solver.add(weights[action_block[t]] <= weights[action_to[t]])
    
    # Table limit: at most 6 blocks on table in current state
    # A block is on table if its state is -1
    on_table_count = Sum([If(state[t][b] == -1, 1, 0) for b in blocks])
    solver.add(on_table_count <= 6)
    
    # Height limit: no tower may exceed height 5
    # We'll enforce this by ensuring no chain of 5 blocks exists
    for b in blocks:
        # Unroll the chain: b -> state[t][b] -> state[t][state[t][b]] -> ...
        # If any chain reaches length 5, it's invalid
        # We'll check for chains of length 5
        b1 = state[t][b]
        b2 = state[t][b1]
        b3 = state[t][b2]
        b4 = state[t][b3]
        b5 = state[t][b4]
        # If b is not -1 and b1 is not -1 and b2 is not -1 and b3 is not -1 and b4 is not -1 and b5 is not -1, then invalid
        solver.add(Not(And(
            b != -1, b1 != -1, b2 != -1, b3 != -1, b4 != -1, b5 != -1
        )))

# Distinct positions: from != to
for t in range(1, MAX_STEPS + 1):
    solver.add(action_from[t] != action_to[t])

# Check if a solution exists
BENCHMARK_MODE = True
result = solver.check()

if result == sat:
    model = solver.model()
    print("STATUS: sat")
    print("A valid plan exists within 50 moves.")
    # Extract and print the plan
    print("\nPlan (first 20 moves shown):")
    for t in range(1, min(21, MAX_STEPS + 1)):
        block = model[action_block[t]]
        from_pos = model[action_from[t]]
        to_pos = model[action_to[t]]
        # Convert to human-readable format
        block_name = chr(ord('A') + block.as_long())
        from_name = "table" if from_pos.as_long() == -1 else chr(ord('A') + from_pos.as_long())
        to_name = "table" if to_pos.as_long() == -1 else chr(ord('A') + to_pos.as_long())
        print(f"Step {t}: move {block_name} from {from_name} to {to_name}")
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")