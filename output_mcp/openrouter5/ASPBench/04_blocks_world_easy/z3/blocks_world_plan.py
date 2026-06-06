from z3 import *

# Blocks World Planning with Z3
# Blocks: A, B, C
# Find shortest plan (expected: 3 moves)

blocks = ["A", "B", "C"]
num_blocks = 3
TABLE = 0

T = 3  # horizon

solver = Solver()

# Variables: on[b][t] = position (0=table, 1=A, 2=B, 3=C)
on = [[Int(f"on_{b}_{t}") for t in range(T+1)] for b in range(num_blocks)]

# Action variables: move[b][t] = 1 if block b is moved at step t
move = [[Int(f"move_{b}_{t}") for t in range(T)] for b in range(num_blocks)]

# Domain constraints
for b in range(num_blocks):
    for t in range(T+1):
        solver.add(on[b][t] >= 0, on[b][t] <= num_blocks)

for b in range(num_blocks):
    for t in range(T):
        solver.add(Or(move[b][t] == 0, move[b][t] == 1))

# Initial state (t=0)
solver.add(on[0][0] == TABLE)  # A on table
solver.add(on[1][0] == TABLE)  # B on table
solver.add(on[2][0] == 1)      # C on A (position 1 = A)

# Goal state (t=T)
solver.add(on[0][T] == 2)  # A on B (position 2 = B)
solver.add(on[1][T] == 3)  # B on C (position 3 = C)
solver.add(on[2][T] == TABLE)  # C on table

# No block on itself
for b in range(num_blocks):
    for t in range(T+1):
        solver.add(on[b][t] != b + 1)

# At most one block on top of another block
for t in range(T+1):
    for pos in range(1, num_blocks+1):
        solver.add(Sum([If(on[b][t] == pos, 1, 0) for b in range(num_blocks)]) <= 1)

# Exactly one block moved per time step
for t in range(T):
    solver.add(Sum([move[b][t] for b in range(num_blocks)]) == 1)

# Frame: if not moved, position stays; if moved, position changes
for t in range(T):
    for b in range(num_blocks):
        solver.add(Implies(move[b][t] == 0, on[b][t+1] == on[b][t]))
        solver.add(Implies(move[b][t] == 1, on[b][t+1] != on[b][t]))

# Precondition: a moved block must be clear (nothing on top of it)
for t in range(T):
    for b in range(num_blocks):
        clear_cond = And([on[other][t] != (b + 1) for other in range(num_blocks) if other != b])
        solver.add(Implies(move[b][t] == 1, clear_cond))

# Precondition: if a block is on top of another, the lower block can't move
for t in range(T):
    for lower in range(num_blocks):
        for upper in range(num_blocks):
            if upper != lower:
                solver.add(Implies(on[upper][t] == lower + 1, move[lower][t] == 0))

# Postcondition: if moved to a position (not table), that position must be clear at time t
for t in range(T):
    for b in range(num_blocks):
        for pos in range(1, num_blocks+1):
            others_clear = And([on[other][t] != pos for other in range(num_blocks) if other != b])
            solver.add(Implies(And(move[b][t] == 1, on[b][t+1] == pos), 
                               And(others_clear, pos != b + 1)))

result = solver.check()

if result == sat:
    m = solver.model()
    print("STATUS: sat")
    print(f"Plan found with horizon T={T}")
    
    # Extract the plan
    for t in range(T):
        for b in range(num_blocks):
            if m.eval(move[b][t]).as_long() == 1:
                block_name = blocks[b]
                from_pos_val = m.eval(on[b][t]).as_long()
                to_pos_val = m.eval(on[b][t+1]).as_long()
                
                from_str = "table" if from_pos_val == 0 else blocks[from_pos_val - 1]
                to_str = "table" if to_pos_val == 0 else blocks[to_pos_val - 1]
                
                print(f"Step {t+1}: move {block_name} from {from_str} to {to_str}")
    
    # Print full state trace
    print("\nState trace:")
    for t in range(T+1):
        state_str = f"t={t}: "
        for b in range(num_blocks):
            pos_val = m.eval(on[b][t]).as_long()
            pos_str = "table" if pos_val == 0 else blocks[pos_val - 1]
            state_str += f"{blocks[b]} on {pos_str}, "
        print(state_str)
    
    print(f"\nplan_length: {T}")
    print("actions:")
    for t in range(T):
        for b in range(num_blocks):
            if m.eval(move[b][t]).as_long() == 1:
                block_name = blocks[b]
                from_pos_val = m.eval(on[b][t]).as_long()
                to_pos_val = m.eval(on[b][t+1]).as_long()
                from_str = "table" if from_pos_val == 0 else blocks[from_pos_val - 1]
                to_str = "table" if to_pos_val == 0 else blocks[to_pos_val - 1]
                print(f"  step: {t+1}, action: move, block: {block_name}, from: {from_str}, to: {to_str}")
else:
    print("STATUS: unsat")
    print("No plan found with horizon 3")