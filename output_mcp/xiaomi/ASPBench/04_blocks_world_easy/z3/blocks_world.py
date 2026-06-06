from z3 import *

# Blocks World Planning Problem
# Blocks: A=0, B=1, C=2, Table=3
BLOCKS = [0, 1, 2]
BLOCK_NAMES = {0: 'A', 1: 'B', 2: 'C', 3: 'table'}
TABLE = 3

# We'll try increasing plan lengths starting from 3
# on(b, t) = position of block b at time t (table=3 or another block)
# move(b, t) = True if block b is moved at time t
# moved_from(b, t) = where block b was before move at time t
# moved_to(b, t) = where block b goes at time t

MAX_STEPS = 5  # Upper bound

for plan_len in range(3, MAX_STEPS + 1):
    solver = Solver()
    T = plan_len  # number of time steps (states: 0..T)
    
    # State variables: on[b][t] = what block b is on at time t
    # Values: 0,1,2 = on that block; 3 = on table
    on = [[Int(f'on_{b}_{t}') for t in range(T+1)] for b in BLOCKS]
    
    # Action variables: move[b][t] = True if block b is moved at time t (t=1..T)
    move = [[Bool(f'move_{b}_{t}') for t in range(T+1)] for b in BLOCKS]
    
    # moved_to[b][t] = destination when block b is moved at time t
    moved_to = [[Int(f'moved_to_{b}_{t}') for t in range(T+1)] for b in BLOCKS]
    
    # Domain constraints: on[b][t] in {0,1,2,3}
    for b in BLOCKS:
        for t in range(T+1):
            solver.add(And(on[b][t] >= 0, on[b][t] <= 3))
            solver.add(And(moved_to[b][t] >= 0, moved_to[b][t] <= 3))
    
    # No block on itself
    for b in BLOCKS:
        for t in range(T+1):
            solver.add(on[b][t] != b)
    
    # At most one block on top of another (except table can hold multiple)
    for t in range(T+1):
        for x in BLOCKS:  # x is a block (not table)
            # At most one block is on x at time t
            solver.add(
                Sum([If(on[b][t] == x, 1, 0) for b in BLOCKS]) <= 1
            )
    
    # Initial state: A on table, B on table, C on A
    solver.add(on[0][0] == TABLE)  # A on table
    solver.add(on[1][0] == TABLE)  # B on table
    solver.add(on[2][0] == 0)      # C on A
    
    # Goal state: A on B, B on C, C on table
    solver.add(on[0][T] == 1)      # A on B
    solver.add(on[1][T] == 2)      # B on C
    solver.add(on[2][T] == TABLE)  # C on table
    
    # Clear predicate: block b is clear at time t if nothing is on top of it
    def is_clear(b, t):
        return And([on[other][t] != b for other in BLOCKS])
    
    # Action constraints for each time step
    for t in range(1, T+1):
        # Exactly one block is moved at each time step
        solver.add(Sum([If(move[b][t], 1, 0) for b in BLOCKS]) == 1)
        
        for b in BLOCKS:
            # If block b is moved at time t:
            # 1. b must be clear at time t-1
            solver.add(Implies(move[b][t], is_clear(b, t-1)))
            # 2. moved_to must be valid: either table or a clear block (not b itself)
            solver.add(Implies(move[b][t], And(
                moved_to[b][t] != b,
                Or(moved_to[b][t] == TABLE,
                   And(moved_to[b][t] >= 0, moved_to[b][t] <= 2,
                       is_clear(moved_to[b][t], t-1)))
            )))
            # 3. State update: if moved, on[b][t] = moved_to[b][t]
            solver.add(Implies(move[b][t], on[b][t] == moved_to[b][t]))
            # 4. Frame axiom: if not moved, position stays the same
            solver.add(Implies(Not(move[b][t]), on[b][t] == on[b][t-1]))
    
    result = solver.check()
    if result == sat:
        m = solver.model()
        print("STATUS: sat")
        print(f"plan_length: {plan_len}")
        print()
        
        actions = []
        for t in range(1, T+1):
            for b in BLOCKS:
                if is_true(m.evaluate(move[b][t])):
                    dest = m.evaluate(moved_to[b][t]).as_long()
                    src = m.evaluate(on[b][t-1]).as_long()
                    actions.append((t, BLOCK_NAMES[b], BLOCK_NAMES[src], BLOCK_NAMES[dest]))
        
        print("Actions:")
        for step, block, frm, to in actions:
            print(f"  Step {step}: move {block} from {frm} to {to}")
        
        # Print full state trace
        print()
        print("State trace:")
        for t in range(T+1):
            print(f"  Time {t}:")
            for b in BLOCKS:
                pos = m.evaluate(on[b][t]).as_long()
                print(f"    {BLOCK_NAMES[b]} on {BLOCK_NAMES[pos]}")
        
        break
    else:
        if plan_len == MAX_STEPS - 1:
            print("STATUS: unsat")
            print("No plan found within max steps")