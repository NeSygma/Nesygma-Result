from z3 import *

# ------------------------------------------------------------
# Config
# ------------------------------------------------------------
MAX_PLAN_LENGTH = 30   # Start smaller, will increase if needed
BENCHMARK_MODE = True

# ------------------------------------------------------------
# Problem data
# ------------------------------------------------------------
NUM_BLOCKS = 12
blocks = list(range(1, NUM_BLOCKS + 1))  # 1=A .. 12=L
weight = {b: b for b in blocks}
block_names = {1:'A', 2:'B', 3:'C', 4:'D', 5:'E', 6:'F',
               7:'G', 8:'H', 9:'I', 10:'J', 11:'K', 12:'L'}

T = MAX_PLAN_LENGTH

# ------------------------------------------------------------
# Variables
# ------------------------------------------------------------
# pos[b][t] = what b sits on (0=table, 1..12=block)
pos = [[Int(f"pos_{b}_{t}") for t in range(T+1)] for b in range(NUM_BLOCKS + 1)]
# depth[b][t] = distance from table (1..5)
depth = [[Int(f"d_{b}_{t}") for t in range(T+1)] for b in range(NUM_BLOCKS + 1)]
# moved[b][t] = true if b moves at step t->t+1
moved = [[Bool(f"m_{b}_{t}") for t in range(T)] for b in range(NUM_BLOCKS + 1)]
# target[b][t] = destination when moved
target = [[Int(f"tgt_{b}_{t}") for t in range(T)] for b in range(NUM_BLOCKS + 1)]

solver = Solver()

# ------------------------------------------------------------
# Domain constraints
# ------------------------------------------------------------
for b in blocks:
    for t in range(T+1):
        solver.add(pos[b][t] >= 0, pos[b][t] <= NUM_BLOCKS)
        solver.add(pos[b][t] != b)  # cannot be on self
        solver.add(depth[b][t] >= 1, depth[b][t] <= 5)
    for t in range(T):
        solver.add(target[b][t] >= 0, target[b][t] <= NUM_BLOCKS)
        solver.add(target[b][t] != b)

# ------------------------------------------------------------
# Initial state
# ------------------------------------------------------------
# Stack 1: D(4) on table, C(3) on D, B(2) on C, A(1) on B
solver.add(pos[4][0] == 0)  # D on table
solver.add(pos[3][0] == 4)  # C on D
solver.add(pos[2][0] == 3)  # B on C
solver.add(pos[1][0] == 2)  # A on B

# Stack 2: H(8) on table, G(7) on H, F(6) on G, E(5) on F
solver.add(pos[8][0] == 0)  # H on table
solver.add(pos[7][0] == 8)  # G on H
solver.add(pos[6][0] == 7)  # F on G
solver.add(pos[5][0] == 6)  # E on F

# Stack 3: L(12) on table, K(11) on L, J(10) on K, I(9) on J
solver.add(pos[12][0] == 0) # L on table
solver.add(pos[11][0] == 12) # K on L
solver.add(pos[10][0] == 11) # J on K
solver.add(pos[9][0] == 10)  # I on J

# Initial depths
solver.add(depth[4][0] == 1)  # D on table
solver.add(depth[3][0] == 2)  # C on D
solver.add(depth[2][0] == 3)  # B on C
solver.add(depth[1][0] == 4)  # A on B

solver.add(depth[8][0] == 1)  # H on table
solver.add(depth[7][0] == 2)  # G on H
solver.add(depth[6][0] == 3)  # F on G
solver.add(depth[5][0] == 4)  # E on F

solver.add(depth[12][0] == 1) # L on table
solver.add(depth[11][0] == 2) # K on L
solver.add(depth[10][0] == 3) # J on K
solver.add(depth[9][0] == 4)  # I on J

# ------------------------------------------------------------
# Goal state (at time T)
# ------------------------------------------------------------
# Tower 1: L(12) on table, I(9) on L, F(6) on I, C(3) on F
solver.add(pos[12][T] == 0)
solver.add(pos[9][T] == 12)
solver.add(pos[6][T] == 9)
solver.add(pos[3][T] == 6)

# Tower 2: K(11) on table, H(8) on K, E(5) on H, B(2) on E
solver.add(pos[11][T] == 0)
solver.add(pos[8][T] == 11)
solver.add(pos[5][T] == 8)
solver.add(pos[2][T] == 5)

# Tower 3: J(10) on table, G(7) on J, D(4) on G, A(1) on D
solver.add(pos[10][T] == 0)
solver.add(pos[7][T] == 10)
solver.add(pos[4][T] == 7)
solver.add(pos[1][T] == 4)

# ------------------------------------------------------------
# Consistency: at most one block can sit on any other block
# ------------------------------------------------------------
for t in range(T+1):
    for c in blocks:
        solver.add(Sum([If(pos[b][t] == c, 1, 0) for b in blocks]) <= 1)

# ------------------------------------------------------------
# Transition constraints for each step t (0 to T-1)
# ------------------------------------------------------------
for t in range(T):
    # ----- Exactly one block is moved at each step -----
    solver.add(Sum([If(moved[b][t], 1, 0) for b in blocks]) == 1)

    for b in blocks:
        # ----- Preconditions -----

        # b must be clear at time t
        solver.add(Implies(moved[b][t], And([pos[c][t] != b for c in blocks if c != b])))

        # If target is a block c, then c must be clear at time t
        for c in blocks:
            if c != b:
                solver.add(Implies(And(moved[b][t], target[b][t] == c),
                                  And([pos[d][t] != c for d in blocks if d != c])))

        # Weight constraint: heavier cannot be on lighter
        for c in blocks:
            if c != b:
                solver.add(Implies(And(moved[b][t], target[b][t] == c),
                                  weight[c] >= weight[b]))

        # ----- Effect: update position -----
        solver.add(Implies(moved[b][t], pos[b][t+1] == target[b][t]))

        # ----- Frame: position unchanged if not moved -----
        solver.add(Implies(Not(moved[b][t]), pos[b][t+1] == pos[b][t]))

    # ----- Depth consistency at t+1 -----
    for b in blocks:
        # If on table, depth = 1
        solver.add(Implies(pos[b][t+1] == 0, depth[b][t+1] == 1))
        # If on another block c, depth = depth[c][t+1] + 1
        for c in blocks:
            if c != b:
                solver.add(Implies(pos[b][t+1] == c,
                                  depth[b][t+1] == depth[c][t+1] + 1))

    # ----- Table limit at t+1 -----
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
    
    plan = []
    for t in range(T):
        moved_block = None
        for b in blocks:
            if m.eval(moved[b][t]):
                moved_block = b
                break
        if moved_block is None:
            break
        
        target_val = m.eval(target[moved_block][t]).as_long()
        from_val = m.eval(pos[moved_block][t]).as_long()
        
        from_name = "table" if from_val == 0 else block_names[from_val]
        to_name = "table" if target_val == 0 else block_names[target_val]
        
        plan.append({
            "step": t+1,
            "action": "move",
            "block": block_names[moved_block],
            "from": from_name,
            "to": to_name
        })
    
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
        print(f"RAW_RESULT: unsat (no plan found with T={T}; try larger T)")
    else:
        print("STATUS: unsat")
        print("No plan exists within the given bounds.")
else:
    print("STATUS: unknown")