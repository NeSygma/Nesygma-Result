from z3 import *

# Parameters
N = 12  # number of blocks
max_steps = 20  # search up to 20 moves (should be enough)

# Mapping block letters to indices (A=1,...,L=12)
block_names = ['A','B','C','D','E','F','G','H','I','J','K','L']
name_to_idx = {name: i+1 for i, name in enumerate(block_names)}
idx_to_name = {i+1: name for i, name in enumerate(block_names)}

# Weight mapping: weight = index (since A=1,...L=12)
weights = {i+1: i+1 for i in range(N)}

# Helper to get weight as Z3 IntVal
weight = lambda idx: IntVal(weights[idx])

# Initial configuration locations (0 = table)
init_loc = {}
# Stack1: D on table, C on D, B on C, A on B
init_loc[name_to_idx['D']] = 0
init_loc[name_to_idx['C']] = name_to_idx['D']
init_loc[name_to_idx['B']] = name_to_idx['C']
init_loc[name_to_idx['A']] = name_to_idx['B']
# Stack2: H on table, G on H, F on G, E on F
init_loc[name_to_idx['H']] = 0
init_loc[name_to_idx['G']] = name_to_idx['H']
init_loc[name_to_idx['F']] = name_to_idx['G']
init_loc[name_to_idx['E']] = name_to_idx['F']
# Stack3: L on table, K on L, J on K, I on J
init_loc[name_to_idx['L']] = 0
init_loc[name_to_idx['K']] = name_to_idx['L']
init_loc[name_to_idx['J']] = name_to_idx['K']
init_loc[name_to_idx['I']] = name_to_idx['J']

# Goal configuration locations
goal_loc = {}
# Tower1: L on table, I on L, F on I, C on F
goal_loc[name_to_idx['L']] = 0
goal_loc[name_to_idx['I']] = name_to_idx['L']
goal_loc[name_to_idx['F']] = name_to_idx['I']
goal_loc[name_to_idx['C']] = name_to_idx['F']
# Tower2: K on table, H on K, E on H, B on E
goal_loc[name_to_idx['K']] = 0
goal_loc[name_to_idx['H']] = name_to_idx['K']
goal_loc[name_to_idx['E']] = name_to_idx['H']
goal_loc[name_to_idx['B']] = name_to_idx['E']
# Tower3: J on table, G on J, D on G, A on D
goal_loc[name_to_idx['J']] = 0
goal_loc[name_to_idx['G']] = name_to_idx['J']
goal_loc[name_to_idx['D']] = name_to_idx['G']
goal_loc[name_to_idx['A']] = name_to_idx['D']

# Declare location variables: loc[step][block]
loc = [[Int(f"loc_{s}_{b}") for b in range(1, N+1)] for s in range(max_steps+1)]

solver = Solver()

# Initial state constraints
for b in range(1, N+1):
    solver.add(loc[0][b-1] == init_loc.get(b, -1))  # all blocks should be defined
    # sanity: location must be 0..N
    solver.add(And(loc[0][b-1] >= 0, loc[0][b-1] <= N))

# Declare move variables for each step
block_s = [Int(f"block_{s}") for s in range(1, max_steps+1)]
from_s = [Int(f"from_{s}") for s in range(1, max_steps+1)]
to_s = [Int(f"to_{s}") for s in range(1, max_steps+1)]

for s in range(1, max_steps+1):
    # block index 0 means idle step
    solver.add(And(block_s[s-1] >= 0, block_s[s-1] <= N))
    solver.add(And(from_s[s-1] >= 0, from_s[s-1] <= N))
    solver.add(And(to_s[s-1] >= 0, to_s[s-1] <= N))

    # Transition constraints
    # For each block b, define its location at step s
    for b in range(1, N+1):
        # default: stays the same
        stay = loc[s][b-1] == loc[s-1][b-1]
        move = And(block_s[s-1] == b,
                    from_s[s-1] == loc[s-1][b-1],
                    to_s[s-1] != from_s[s-1],
                    to_s[s-1] != b,
                    # source block must be clear before move
                    # no other block on b at previous step
                    ForAll([Int('c')], Implies(And(Int('c') != b, loc[s-1][Int('c')-1] == b), False)),
                    # destination must be clear if not table
                    If(to_s[s-1] == 0,
                       True,
                       ForAll([Int('c2')], Implies(And(Int('c2') != b, loc[s-1][Int('c2')-1] == to_s[s-1]), False)),
                    # weight constraint if placed on another block
                    If(to_s[s-1] == 0,
                       True,
                       weight(to_s[s-1]) >= weight(b)),
                    loc[s][b-1] == to_s[s-1])
        # If idle step (block_s == 0) then all stay
        solver.add(If(block_s[s-1] == 0, stay, Or(stay, move)))
    # Ensure that if block_s != 0 then exactly one block moves (already enforced by construction)
    # No additional constraints needed

# Goal state at final step
for b in range(1, N+1):
    solver.add(loc[max_steps][b-1] == goal_loc.get(b, -1))

# Solve
result = solver.check()
if result == sat:
    m = solver.model()
    print("STATUS: sat")
    # Extract moves
    moves = []
    for s in range(1, max_steps+1):
        blk = m.eval(block_s[s-1]).as_long()
        if blk != 0:
            frm = m.eval(from_s[s-1]).as_long()
            to = m.eval(to_s[s-1]).as_long()
            moves.append((s, idx_to_name[blk], "table" if frm==0 else idx_to_name[frm], "table" if to==0 else idx_to_name[to]))
    print("plan_length =", len(moves))
    for step, blk, frm, to in moves:
        print(f"{{'step': {step}, 'action': 'move', 'block': '{blk}', 'from': '{frm}', 'to': '{to}'}}")
else:
    print("STATUS: unsat")