from z3 import *

# ------------------------------------------------------------
# Configurable parameters
# ------------------------------------------------------------
MAX_PLAN_LENGTH = 50   # Maximum moves allowed
BENCHMARK_MODE = True   # In benchmark mode, unsat triggers refinement

# ------------------------------------------------------------
# Problem data
# ------------------------------------------------------------
NUM_BLOCKS = 12
blocks = list(range(1, NUM_BLOCKS + 1))  # 1=A, 2=B, ..., 12=L

# Weights: block ID equals weight (A=1, ..., L=12)
weight = {b: b for b in blocks}

# Block names for output
block_names = {1:'A', 2:'B', 3:'C', 4:'D', 5:'E', 6:'F',
               7:'G', 8:'H', 9:'I', 10:'J', 11:'K', 12:'L'}

T = MAX_PLAN_LENGTH

# ------------------------------------------------------------
# Z3 variables
# ------------------------------------------------------------
# pos[b][t] = what block b sits on at time t (0 = table, 1..12 = block)
pos = [[Int(f"pos_{b}_{t}") for t in range(T+1)] for b in range(NUM_BLOCKS + 1)]

# depth[b][t] = distance from table (1 = on table, 2 = on block on table, ...)
depth = [[Int(f"depth_{b}_{t}") for t in range(T+1)] for b in range(NUM_BLOCKS + 1)]

# moved[b][t] = whether block b is moved at step t+1 (t from 0 to T-1)
moved = [[Bool(f"moved_{b}_{t}") for t in range(T)] for b in range(NUM_BLOCKS + 1)]

# target[b][t] = where block b is placed when moved at step t+1 (0=table, 1..12=block)
target = [[Int(f"target_{b}_{t}") for t in range(T)] for b in range(NUM_BLOCKS + 1)]

solver = Solver()

# ------------------------------------------------------------
# Domain constraints
# ------------------------------------------------------------
for b in blocks:
    for t in range(T+1):
        solver.add(pos[b][t] >= 0, pos[b][t] <= NUM_BLOCKS)
        solver.add(pos[b][t] != b)                      # no self-support
        solver.add(depth[b][t] >= 1, depth[b][t] <= 5)  # height limit (max 5)
    for t in range(T):
        solver.add(target[b][t] >= 0, target[b][t] <= NUM_BLOCKS)
        solver.add(target[b][t] != b)                   # can't place on self

# ------------------------------------------------------------
# Initial state (time 0)
# ------------------------------------------------------------
# Stack 1: D(4) on table, C(3) on D(4), B(2) on C(3), A(1) on B(2)
solver.add(pos[4][0] == 0)
solver.add(pos[3][0] == 4)
solver.add(pos[2][0] == 3)
solver.add(pos[1][0] == 2)

# Stack 2: H(8) on table, G(7) on H(8), F(6) on G(7), E(5) on F(6)
solver.add(pos[8][0] == 0)
solver.add(pos[7][0] == 8)
solver.add(pos[6][0] == 7)
solver.add(pos[5][0] == 6)

# Stack 3: L(12) on table, K(11) on L(12), J(10) on K(11), I(9) on J(10)
solver.add(pos[12][0] == 0)
solver.add(pos[11][0] == 12)
solver.add(pos[10][0] == 11)
solver.add(pos[9][0] == 10)

# ------------------------------------------------------------
# Goal state (time T)
# ------------------------------------------------------------
# Tower 1: L(12) on table, I(9) on L(12), F(6) on I(9), C(3) on F(6)
solver.add(pos[12][T] == 0)
solver.add(pos[9][T] == 12)
solver.add(pos[6][T] == 9)
solver.add(pos[3][T] == 6)

# Tower 2: K(11) on table, H(8) on K(11), E(5) on H(8), B(2) on E(5)
solver.add(pos[11][T] == 0)
solver.add(pos[8][T] == 11)
solver.add(pos[5][T] == 8)
solver.add(pos[2][T] == 5)

# Tower 3: J(10) on table, G(7) on J(10), D(4) on G(7), A(1) on D(4)
solver.add(pos[10][T] == 0)
solver.add(pos[7][T] == 10)
solver.add(pos[4][T] == 7)
solver.add(pos[1][T] == 4)

# ------------------------------------------------------------
# Consistency constraints (apply at all times)
# ------------------------------------------------------------
# At most one block can sit on any other block
for t in range(T+1):
    for c in blocks:
        solver.add(Sum([If(pos[b][t] == c, 1, 0) for b in blocks]) <= 1)

# ------------------------------------------------------------
# Initial depth constraints (time 0)
# ------------------------------------------------------------
for b in blocks:
    solver.add(Or([And(pos[b][0] == 0, depth[b][0] == 1)] + 
                  [And(pos[b][0] == c, depth[b][0] == depth[c][0] + 1) 
                   for c in blocks if c != b]))

# ------------------------------------------------------------
# Transition constraints for each step t (0 to T-1)
# ------------------------------------------------------------
for t in range(T):
    # ---- 1. Exactly one block is moved at each step ----
    solver.add(Sum([If(moved[b][t], 1, 0) for b in blocks]) == 1)

    for b in blocks:
        # ---- 2. Preconditions for moving block b ----
        
        # b must be clear (no block sits on b) at time t
        clear_b = And([pos[c][t] != b for c in blocks if c != b])
        solver.add(Implies(moved[b][t], clear_b))

        # If target is a block (not table), it must be clear at time t
        # For each possible target c, if target == c, then c must be clear
        for c in blocks:
            if c != b:
                # target == c implies that c is clear (no block sits on c)
                clear_c = And([pos[d][t] != c for d in blocks if d != c])
                solver.add(Implies(And(moved[b][t], target[b][t] == c), clear_c))

        # ---- 3. Weight constraint ----
        # Heavier block cannot be placed on lighter block
        # weight(target) >= weight(b) required
        for c in blocks:
            if c != b:
                solver.add(Implies(And(moved[b][t], target[b][t] == c),
                                  weight[c] >= weight[b]))

        # ---- 4. Effect: new position at t+1 ----
        solver.add(Implies(moved[b][t], pos[b][t+1] == target[b][t]))

        # ---- 5. Frame axiom: position unchanged if not moved ----
        solver.add(Implies(Not(moved[b][t]), pos[b][t+1] == pos[b][t]))

    # ---- 6. Depth constraints at t+1 ----
    for b in blocks:
        solver.add(Or([And(pos[b][t+1] == 0, depth[b][t+1] == 1)] + 
                      [And(pos[b][t+1] == c, depth[b][t+1] == depth[c][t+1] + 1) 
                       for c in blocks if c != b]))

    # ---- 7. Table limit at t+1 ----
    solver.add(Sum([If(pos[b][t+1] == 0, 1, 0) for b in blocks]) <= 6)

# ------------------------------------------------------------
# Solve
# ------------------------------------------------------------
print(f"Solving with plan length limit T={T}...")
result = solver.check()

if result == sat:
    m = solver.model()
    print("STATUS: sat")
    print(f"Plan found with up to {T} moves.")
    
    # Extract the plan
    plan = []
    for t in range(T):
        # Find which block was moved at step t
        moved_block = None
        for b in blocks:
            if m.eval(moved[b][t]):
                moved_block = b
                break
        if moved_block is None:
            break
        
        target_val = m.eval(target[moved_block][t]).as_long()
        
        # Find from-position (where block was at time t)
        from_val = m.eval(pos[moved_block][t]).as_long()
        
        # Determine from and to names
        from_name = "table" if from_val == 0 else block_names[from_val]
        to_name = "table" if target_val == 0 else block_names[target_val]
        
        plan.append({
            "step": t+1,
            "action": "move",
            "block": block_names[moved_block],
            "from": from_name,
            "to": to_name
        })
    
    # Print the plan
    print(f"plan_length: {len(plan)}")
    print("actions:")
    for action in plan:
        print(f"  - step: {action['step']}")
        print(f"    action: {action['action']}")
        print(f"    block: {action['block']}")
        print(f"    from: {action['from']}")
        print(f"    to: {action['to']}")

elif result == unsat:
    if BENCHMARK_MODE:
        print("STATUS: unsat")
        print("RAW_RESULT: unsat (no plan found within T=50; refinement may be needed)")
    else:
        print("STATUS: unsat")
        print("No plan exists within the given bounds.")
else:
    print("STATUS: unknown")