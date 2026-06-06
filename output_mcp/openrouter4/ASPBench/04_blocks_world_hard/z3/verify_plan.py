from z3 import *

# ------------------------------------------------------------
# Verify a hand-crafted plan using Z3
# ------------------------------------------------------------
NUM_BLOCKS = 12
blocks = list(range(1, NUM_BLOCKS + 1))
weight = {b: b for b in blocks}
block_names = {1:'A', 2:'B', 3:'C', 4:'D', 5:'E', 6:'F',
               7:'G', 8:'H', 9:'I', 10:'J', 11:'K', 12:'L'}
name_to_block = {v: k for k, v in block_names.items()}

# Hand-crafted plan
plan_moves = [
    ("A", "B", "table"),
    ("B", "C", "table"),
    ("C", "D", "table"),
    ("A", "table", "D"),
    ("B", "table", "C"),
    ("E", "F", "table"),
    ("F", "G", "table"),
    ("F", "table", "G"),
    ("I", "J", "table"),
    ("E", "table", "G"),
    ("J", "K", "table"),
    ("K", "L", "table"),
    ("I", "table", "L"),
    ("F", "G", "I"),
    ("B", "C", "table"),
    ("C", "table", "F"),
    ("G", "H", "J"),
    ("H", "table", "K"),
    ("E", "table", "H"),
    ("B", "table", "E"),
    ("D", "table", "G"),
    ("A", "D", "table"),
    ("A", "table", "D")
]

T = len(plan_moves)
print(f"Plan length: {T}")

# Variables
pos = [[Int(f"pos_{b}_{t}") for t in range(T+1)] for b in range(NUM_BLOCKS + 1)]

solver = Solver()

# Domain
for b in blocks:
    for t in range(T+1):
        solver.add(pos[b][t] >= 0, pos[b][t] <= NUM_BLOCKS)
        solver.add(pos[b][t] != b)

# Initial state
# Stack 1: D(4) on table, C(3) on D, B(2) on C, A(1) on B
solver.add(pos[4][0] == 0)
solver.add(pos[3][0] == 4)
solver.add(pos[2][0] == 3)
solver.add(pos[1][0] == 2)

# Stack 2: H(8) on table, G(7) on H, F(6) on G, E(5) on F
solver.add(pos[8][0] == 0)
solver.add(pos[7][0] == 8)
solver.add(pos[6][0] == 7)
solver.add(pos[5][0] == 6)

# Stack 3: L(12) on table, K(11) on L, J(10) on K, I(9) on J
solver.add(pos[12][0] == 0)
solver.add(pos[11][0] == 12)
solver.add(pos[10][0] == 11)
solver.add(pos[9][0] == 10)

# Goal state at time T
solver.add(pos[12][T] == 0)  # L on table
solver.add(pos[9][T] == 12)  # I on L
solver.add(pos[6][T] == 9)   # F on I
solver.add(pos[3][T] == 6)   # C on F

solver.add(pos[11][T] == 0)  # K on table
solver.add(pos[8][T] == 11)  # H on K
solver.add(pos[5][T] == 8)   # E on H
solver.add(pos[2][T] == 5)   # B on E

solver.add(pos[10][T] == 0)  # J on table
solver.add(pos[7][T] == 10)  # G on J
solver.add(pos[4][T] == 7)   # D on G
solver.add(pos[1][T] == 4)   # A on D

# Encode each move
for step_idx, (block_name, from_name, to_name) in enumerate(plan_moves):
    t = step_idx
    b = name_to_block[block_name]
    from_val = 0 if from_name == "table" else name_to_block[from_name]
    to_val = 0 if to_name == "table" else name_to_block[to_name]
    
    # Constraint: block b must be at from_val at time t
    solver.add(pos[b][t] == from_val)
    
    # Constraint: b is clear (nothing on top)
    for other in blocks:
        if other != b:
            solver.add(pos[other][t] != b)
    
    # If moving to a block c, c must be clear
    if to_val != 0:
        for other in blocks:
            if other != b:
                solver.add(pos[other][t] != to_val)
        # Weight constraint
        solver.add(weight[to_val] >= weight[b])
    
    # Update position
    solver.add(pos[b][t+1] == to_val)
    
    # Frame: all other blocks stay where they are
    for other in blocks:
        if other != b:
            solver.add(pos[other][t+1] == pos[other][t])

# Table limit for each time step
for t in range(T+1):
    solver.add(Sum([If(pos[b][t] == 0, 1, 0) for b in blocks]) <= 6)

# Height limit: max 5 blocks in any stack
# Encode by checking that for each block b, there's no chain of 5 others above it
# Simplification: check that depth (computed via chain) never exceeds 5
# We'll use a different approach: for each b at each t, 
# there cannot be 5 blocks above it in a chain

# Let me use depth variables for the height check
depth = [[Int(f"d_{b}_{t}") for t in range(T+1)] for b in range(NUM_BLOCKS + 1)]
for b in blocks:
    for t in range(T+1):
        solver.add(depth[b][t] >= 1)
        solver.add(depth[b][t] <= 5)

for t in range(T+1):
    for b in blocks:
        solver.add(Implies(pos[b][t] == 0, depth[b][t] == 1))
        for c in blocks:
            if c != b:
                solver.add(Implies(pos[b][t] == c, depth[b][t] == depth[c][t] + 1))

# Also enforce: at most one block on any other block
for t in range(T+1):
    for c in blocks:
        solver.add(Sum([If(pos[b][t] == c, 1, 0) for b in blocks if b != c]) <= 1)

print("Checking plan validity...")
result = solver.check()
print(f"Result: {result}")

if result == sat:
    print("STATUS: sat")
    print("Plan is VALID!")
    m = solver.model()
    print("\nFinal state verification:")
    for b in blocks:
        p = m.eval(pos[b][T]).as_long()
        d = m.eval(depth[b][T]).as_long()
        pos_name = "table" if p == 0 else block_names[p]
        print(f"  {block_names[b]}: on {pos_name}, depth {d}")
elif result == unsat:
    print("STATUS: unsat")
    print("Plan is INVALID!")
    # Let's find which step fails
    # Check each step individually
    for step_idx, (block_name, from_name, to_name) in enumerate(plan_moves):
        step_solver = Solver()
        b = name_to_block[block_name]
        from_val = 0 if from_name == "table" else name_to_block[from_name]
        to_val = 0 if to_name == "table" else name_to_block[to_name]
        
        # Add state constraints up to this step
        step_solver.add(pos[4][0] == 0)
        step_solver.add(pos[3][0] == 4)
        step_solver.add(pos[2][0] == 3)
        step_solver.add(pos[1][0] == 2)
        step_solver.add(pos[8][0] == 0)
        step_solver.add(pos[7][0] == 8)
        step_solver.add(pos[6][0] == 7)
        step_solver.add(pos[5][0] == 6)
        step_solver.add(pos[12][0] == 0)
        step_solver.add(pos[11][0] == 12)
        step_solver.add(pos[10][0] == 11)
        step_solver.add(pos[9][0] == 10)
        
        for s in range(step_idx + 1):
            sb = name_to_block[plan_moves[s][0]]
            sfrom = 0 if plan_moves[s][1] == "table" else name_to_block[plan_moves[s][1]]
            sto = 0 if plan_moves[s][2] == "table" else name_to_block[plan_moves[s][2]]
            
            step_solver.add(pos[sb][s] == sfrom)
            for other in blocks:
                if other != sb:
                    step_solver.add(pos[other][s] != sb)
            if sto != 0:
                for other in blocks:
                    if other != sb:
                        step_solver.add(pos[other][s] != sto)
                step_solver.add(weight[sto] >= weight[sb])
            step_solver.add(pos[sb][s+1] == sto)
            for other in blocks:
                if other != sb:
                    step_solver.add(pos[other][s+1] == pos[other][s])
        
        # Table limit
        for s in range(step_idx + 2):
            step_solver.add(Sum([If(pos[bb][s] == 0, 1, 0) for bb in blocks]) <= 6)
        
        # One-block-per-support constraint
        for s in range(step_idx + 2):
            for c in blocks:
                step_solver.add(Sum([If(pos[bb][s] == c, 1, 0) for bb in blocks if bb != c]) <= 1)
        
        step_res = step_solver.check()
        if step_res == unsat:
            print(f"  Step {step_idx+1}: {block_name} from {from_name} to {to_name} FAILS")
        else:
            print(f"  Step {step_idx+1}: {block_name} from {from_name} to {to_name} OK")
else:
    print("STATUS: unknown")