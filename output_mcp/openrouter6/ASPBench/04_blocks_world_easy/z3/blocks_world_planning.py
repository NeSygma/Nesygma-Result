from z3 import *

# Blocks: A=0, B=1, C=2
# Positions: 0=table, 1=A, 2=B, 3=C
blocks = [0, 1, 2]
block_names = ['A', 'B', 'C']
position_names = ['table', 'A', 'B', 'C']

# We'll try increasing time horizons until we find a solution
for T in range(0, 10):  # Try up to 10 time steps
    solver = Solver()
    
    # State variables: on[block][time] = position (0-3)
    on = [[Int(f'on_{b}_{t}') for t in range(T+1)] for b in blocks]
    
    # Move variables for each time step
    moved_block = [Int(f'moved_{t}') for t in range(T)]
    target_pos = [Int(f'target_{t}') for t in range(T)]
    
    # Domain constraints for state variables
    for b in blocks:
        for t in range(T+1):
            solver.add(And(on[b][t] >= 0, on[b][t] <= 3))
    
    # Domain constraints for move variables
    for t in range(T):
        solver.add(And(moved_block[t] >= 0, moved_block[t] <= 2))  # Block indices
        solver.add(And(target_pos[t] >= 0, target_pos[t] <= 3))    # Position indices
    
    # Initial state constraints
    solver.add(on[0][0] == 0)  # A on table
    solver.add(on[1][0] == 0)  # B on table
    solver.add(on[2][0] == 1)  # C on A (position 1 = A)
    
    # Goal state constraints
    if T > 0:  # Only add goal constraints if we have time steps
        solver.add(on[0][T] == 2)  # A on B
        solver.add(on[1][T] == 3)  # B on C
        solver.add(on[2][T] == 0)  # C on table
    
    # Global constraints for each time step
    for t in range(T+1):
        # No block can be on itself
        for b in blocks:
            solver.add(on[b][t] != b + 1)  # b+1 is the position index for block b
        
        # At most one block can be on top of another block
        for pos in range(1, 4):  # Positions 1,2,3 correspond to blocks A,B,C
            # Count how many blocks are on this position
            count = Sum([If(on[b][t] == pos, 1, 0) for b in blocks])
            solver.add(count <= 1)
    
    # Transition constraints for each move
    for t in range(T):
        b = moved_block[t]
        dst = target_pos[t]
        
        # The block being moved must be clear at time t
        # Clear means no other block is on top of it
        for other in blocks:
            if other != b:
                solver.add(on[other][t] != b + 1)
        
        # Target position must be clear (if moving to a block)
        # Table (position 0) is always clear
        solver.add(Or(
            dst == 0,  # Moving to table is always allowed
            And([on[other][t] != dst for other in blocks])  # Moving to a block requires it to be clear
        ))
        
        # Cannot move to itself
        solver.add(dst != b + 1)
        
        # State transition: moved block goes to target position
        solver.add(on[b][t+1] == dst)
        
        # Other blocks stay in place
        for other in blocks:
            if other != b:
                solver.add(on[other][t+1] == on[other][t])
    
    # Check satisfiability
    result = solver.check()
    
    if result == sat:
        print("STATUS: sat")
        print(f"plan_length: {T}")
        print("actions:")
        
        model = solver.model()
        actions = []
        
        for t in range(T):
            b_idx = model[moved_block[t]].as_long()
            dst_idx = model[target_pos[t]].as_long()
            
            # Get source position from state at time t
            src_idx = model[on[b_idx][t]].as_long()
            
            action = {
                "step": t + 1,
                "action": "move",
                "block": block_names[b_idx],
                "from": position_names[src_idx],
                "to": position_names[dst_idx]
            }
            actions.append(action)
            
            print(f"  Step {t+1}: move {block_names[b_idx]} from {position_names[src_idx]} to {position_names[dst_idx]}")
        
        # Also print in the required format
        print(f"actions_list: {actions}")
        break
    elif result == unsat:
        if T == 0:
            print("STATUS: unsat")
            print("Initial state does not match goal state")
        # Continue to next T
    else:
        print("STATUS: unknown")
        break
else:
    print("STATUS: unsat")
    print("No solution found within 10 time steps")