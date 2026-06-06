from z3 import *

# Mapping indices: 0=table, 1=A, 2=B, 3=C
blocks = ['A','B','C']
idx = {'A':1,'B':2,'C':3}

H = 3  # horizon (number of steps)
solver = Solver()

# Location variables: loc[block][t]
loc = {b: [Int(f"loc_{b}_{t}") for t in range(H+1)] for b in blocks}

# Move variables per step
move_block = [Int(f"move_block_{t}") for t in range(1, H+1)]
dest = [Int(f"dest_{t}") for t in range(1, H+1)]

# Domain constraints for locations (0..3)
for b in blocks:
    for t in range(H+1):
        solver.add(loc[b][t] >= 0, loc[b][t] <= 3)
        # No block can be on itself
        solver.add(loc[b][t] != idx[b])

# Domain constraints for move variables
for t in range(1, H+1):
    solver.add(move_block[t-1] >= 1, move_block[t-1] <= 3)  # must move a block
    solver.add(dest[t-1] >= 0, dest[t-1] <= 3)
    # Cannot move a block onto itself
    solver.add(dest[t-1] != move_block[t-1])

# Initial state constraints
solver.add(loc['A'][0] == 0)  # A on table
solver.add(loc['B'][0] == 0)  # B on table
solver.add(loc['C'][0] == idx['A'])  # C on A

# Goal state constraints at time H
solver.add(loc['A'][H] == idx['B'])  # A on B
solver.add(loc['B'][H] == idx['C'])  # B on C
solver.add(loc['C'][H] == 0)          # C on table

# At each time step enforce at most one block on each non-table position
for t in range(H+1):
    for p in [1,2,3]:
        solver.add(Sum([If(loc[b][t] == p, 1, 0) for b in blocks]) <= 1)

# Define clear condition helper
def is_clear(block_name, time):
    # block is clear if no other block is on it at given time
    return And([loc[other][time] != idx[block_name] for other in blocks if other != block_name])

# Transition constraints for each step
for t in range(1, H+1):
    mb = move_block[t-1]
    d = dest[t-1]
    # The moved block must be clear before move
    # Encode: for each possible block, if mb == idx[block] then that block is clear at t-1
    clear_conditions = []
    for b in blocks:
        clear_conditions.append(Implies(mb == idx[b], is_clear(b, t-1)))
    solver.add(And(clear_conditions))
    # Destination must be clear (if not table)
    dest_clear = []
    for b in blocks:
        dest_clear.append(Implies(And(d == idx[b], d != 0), is_clear(b, t-1)))
    solver.add(And(dest_clear))
    # Update locations
    for b in blocks:
        # If this block is the moved one, its new location is dest
        solver.add(If(mb == idx[b], loc[b][t] == d, loc[b][t] == loc[b][t-1]))

# Ensure exactly one move per step (already enforced by move_block domain)
# Solve
result = solver.check()
if result == sat:
    m = solver.model()
    print("STATUS: sat")
    plan = []
    for t in range(1, H+1):
        mb_idx = m.eval(move_block[t-1]).as_long()
        d_idx = m.eval(dest[t-1]).as_long()
        # Find block name from index
        block_name = [b for b,i in idx.items() if i == mb_idx][0]
        # source location from previous time
        src_idx = m.eval(loc[block_name][t-1]).as_long()
        src = "table" if src_idx == 0 else [b for b,i in idx.items() if i == src_idx][0]
        to = "table" if d_idx == 0 else [b for b,i in idx.items() if i == d_idx][0]
        plan.append((t, block_name, src, to))
    print("plan_length =", H)
    for step, blk, src, to in plan:
        print(f"step:{step} action:move block:{blk} from:{src} to:{to}")
else:
    print("STATUS: unsat")