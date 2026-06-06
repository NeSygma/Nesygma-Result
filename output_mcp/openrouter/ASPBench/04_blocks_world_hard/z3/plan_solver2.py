from z3 import *

# Parameters
N = 12  # number of blocks (A=1,...,L=12)
max_steps = 15  # allow up to 15 moves (should be enough)

# Mapping names to indices
names = ['A','B','C','D','E','F','G','H','I','J','K','L']
name_to_idx = {n:i+1 for i,n in enumerate(names)}
idx_to_name = {i+1:n for i,n in enumerate(names)}

# Weight = index (A=1,...L=12)
weights = {i+1:i+1 for i in range(N)}
weight = lambda idx: IntVal(weights[idx])

# Initial locations (0 = table)
init = {}
# Stack1: D on table, C on D, B on C, A on B
init[name_to_idx['D']] = 0
init[name_to_idx['C']] = name_to_idx['D']
init[name_to_idx['B']] = name_to_idx['C']
init[name_to_idx['A']] = name_to_idx['B']
# Stack2: H on table, G on H, F on G, E on F
init[name_to_idx['H']] = 0
init[name_to_idx['G']] = name_to_idx['H']
init[name_to_idx['F']] = name_to_idx['G']
init[name_to_idx['E']] = name_to_idx['F']
# Stack3: L on table, K on L, J on K, I on J
init[name_to_idx['L']] = 0
init[name_to_idx['K']] = name_to_idx['L']
init[name_to_idx['J']] = name_to_idx['K']
init[name_to_idx['I']] = name_to_idx['J']

# Goal locations
goal = {}
# Tower1: L on table, I on L, F on I, C on F
goal[name_to_idx['L']] = 0
goal[name_to_idx['I']] = name_to_idx['L']
goal[name_to_idx['F']] = name_to_idx['I']
goal[name_to_idx['C']] = name_to_idx['F']
# Tower2: K on table, H on K, E on H, B on E
goal[name_to_idx['K']] = 0
goal[name_to_idx['H']] = name_to_idx['K']
goal[name_to_idx['E']] = name_to_idx['H']
goal[name_to_idx['B']] = name_to_idx['E']
# Tower3: J on table, G on J, D on G, A on D
goal[name_to_idx['J']] = 0
goal[name_to_idx['G']] = name_to_idx['J']
goal[name_to_idx['D']] = name_to_idx['G']
goal[name_to_idx['A']] = name_to_idx['D']

# Location variables per step
loc = [[Int(f"loc_{s}_{b}") for b in range(1,N+1)] for s in range(max_steps+1)]
solver = Solver()

# Domain constraints and initial state
for b in range(1,N+1):
    solver.add(And(loc[0][b-1] >= 0, loc[0][b-1] <= N))
    solver.add(loc[0][b-1] == init.get(b, -1))

# Move variables per step (0 means no move)
move_block = [Int(f"mb_{s}") for s in range(1,max_steps+1)]
move_from = [Int(f"mf_{s}") for s in range(1,max_steps+1)]
move_to   = [Int(f"mt_{s}") for s in range(1,max_steps+1)]

for s in range(1,max_steps+1):
    solver.add(And(move_block[s-1] >= 0, move_block[s-1] <= N))
    solver.add(And(move_from[s-1] >= 0, move_from[s-1] <= N))
    solver.add(And(move_to[s-1]   >= 0, move_to[s-1]   <= N))

    # Transition constraints
    for b in range(1,N+1):
        # default stay same
        stay = loc[s][b-1] == loc[s-1][b-1]
        # if this block is moved
        moved = And(move_block[s-1] == b,
                    move_from[s-1] == loc[s-1][b-1],
                    move_to[s-1] != move_from[s-1],
                    move_to[s-1] != b,
                    # source must be clear: no other block on it
                    Sum([If(loc[s-1][c-1] == b, 1, 0) for c in range(1,N+1)]) == 0,
                    # destination clear if not table
                    If(move_to[s-1] == 0,
                       True,
                       Sum([If(loc[s-1][c-1] == move_to[s-1], 1, 0) for c in range(1,N+1)]) == 0,
                    # weight constraint if placed on block
                    If(move_to[s-1] == 0,
                       True,
                       weight(move_to[s-1]) >= weight(b)),
                    loc[s][b-1] == move_to[s-1])
        # If no move this step, all blocks stay
        solver.add(If(move_block[s-1] == 0, stay, Or(stay, moved)))
    # Table limit at each step
    solver.add(Sum([If(loc[s][b-1] == 0, 1, 0) for b in range(1,N+1)]) <= 6)

# Goal at final step
for b in range(1,N+1):
    solver.add(loc[max_steps][b-1] == goal.get(b, -1))

# Solve
res = solver.check()
if res == sat:
    m = solver.model()
    print("STATUS: sat")
    moves = []
    for s in range(1, max_steps+1):
        blk = m.eval(move_block[s-1]).as_long()
        if blk != 0:
            frm = m.eval(move_from[s-1]).as_long()
            to = m.eval(move_to[s-1]).as_long()
            moves.append((s, idx_to_name[blk], "table" if frm==0 else idx_to_name[frm], "table" if to==0 else idx_to_name[to]))
    print("plan_length =", len(moves))
    for step, blk, frm, to in moves:
        print(f"{{'step': {step}, 'action': 'move', 'block': '{blk}', 'from': '{frm}', 'to': '{to}'}}")
else:
    print("STATUS: unsat")