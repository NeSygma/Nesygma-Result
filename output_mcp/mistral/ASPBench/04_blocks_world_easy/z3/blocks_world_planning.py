from z3 import *

# BENCHMARK_MODE: ON (problem is guaranteed solvable)
BENCHMARK_MODE = True

# Blocks
blocks = ['A', 'B', 'C']

# Time horizon (start with expected optimal length)
T = 3

# Create solver
solver = Optimize()

# State variables:
# on[t][b] = block or "table" that block b is on at time t
# We will use a list of dictionaries for clarity
on = [{} for _ in range(T+1)]

# Initialize state variables for each time step and block
for t in range(T+1):
    for b in blocks:
        on[t][b] = String(f"on_{t}_{b}")
        solver.add(Or(
            on[t][b] == StringVal("table"),
            Or([on[t][b] == StringVal(block) for block in blocks])
        ))

# Action variables:
# action[t] = action at time t (always "move" in this problem)
action = [String(f"action_{t}") for t in range(T)]

# action_block[t] = block being moved at time t
action_block = [String(f"action_block_{t}") for t in range(T)]

# action_from[t] = source position at time t
action_from = [String(f"action_from_{t}") for t in range(T)]

# action_to[t] = target position at time t
action_to = [String(f"action_to_{t}") for t in range(T)]

# Initial state constraints (t=0)
# Block A is on the table
solver.add(on[0]["A"] == StringVal("table"))
# Block B is on the table
solver.add(on[0]["B"] == StringVal("table"))
# Block C is on top of block A
solver.add(on[0]["C"] == StringVal("A"))

# Ensure no block is on itself at any time
for t in range(T+1):
    for b in blocks:
        solver.add(on[t][b] != StringVal(b))

# Ensure at most one block is on another block (except table)
for t in range(T+1):
    for b in blocks:
        # Count how many blocks are on b
        count_on_b = Sum([If(on[t][b2] == StringVal(b), 1, 0) for b2 in blocks])
        solver.add(count_on_b <= 1)

# Action constraints
for t in range(T):
    # Action is always "move"
    solver.add(action[t] == StringVal("move"))
    
    # Block being moved must be clear at time t
    # A block is clear if nothing is on top of it
    for b in blocks:
        solver.add(Implies(
            action_block[t] == StringVal(b),
            And([on[t][b2] != StringVal(b) for b2 in blocks])
        ))
    
    # Source position must be where the block currently is
    for b in blocks:
        solver.add(Implies(
            action_block[t] == StringVal(b),
            action_from[t] == on[t][b]
        ))
    
    # Target position must be either "table" or a clear block
    solver.add(
        Or(
            action_to[t] == StringVal("table"),
            And(
                Or([action_to[t] == StringVal(b) for b in blocks]),
                And([on[t][b] != StringVal(action_to[t].__str__().split('_')[-1].strip('"')) for b in blocks])
            )
        )
    )
    
    # Update state after action
    # For the moved block, its new position is action_to[t]
    for b in blocks:
        solver.add(Implies(
            action_block[t] == StringVal(b),
            on[t+1][b] == action_to[t]
        ))
    
    # For other blocks, their position remains the same
    for b in blocks:
        solver.add(Implies(
            Not(Or([action_block[t] == StringVal(b2) for b2 in blocks])),
            on[t+1][b] == on[t][b]
        ))

# Goal state constraints (t=T)
# Block A is on top of block B
solver.add(on[T]["A"] == StringVal("B"))
# Block B is on top of block C
solver.add(on[T]["B"] == StringVal("C"))
# Block C is on the table
solver.add(on[T]["C"] == StringVal("table"))

# Ensure no block is on itself at goal state (redundant but safe)
for b in blocks:
    solver.add(on[T][b] != StringVal(b))

# Check if a plan of length T exists
result = solver.check()

if result == sat:
    model = solver.model()
    print("STATUS: sat")
    print(f"Optimal plan length: {T}")
    
    # Extract and print the plan
    actions_list = []
    for t in range(T):
        step = t + 1
        block = model[action_block[t]]
        from_pos = model[action_from[t]]
        to_pos = model[action_to[t]]
        actions_list.append({
            "step": step,
            "action": "move",
            "block": str(block),
            "from": str(from_pos),
            "to": str(to_pos)
        })
    
    print("plan_length:", T)
    print("actions:", actions_list)
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")