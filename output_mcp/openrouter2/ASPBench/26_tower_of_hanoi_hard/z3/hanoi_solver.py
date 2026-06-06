from z3 import *

BENCHMARK_MODE = True
T = 20  # upper bound on moves

solver = Optimize()

# Disk positions: disk_peg[d-1][t] is peg index (0=A,1=B,2=C,3=D) of disk d at time t
# t ranges from 0 to T
# d ranges from 1 to 4

disk_peg = [[Int(f'disk_{d}_peg_{t}') for t in range(T+1)] for d in range(1,5)]

# Move variables for each step t=1..T
move_disk = [Int(f'move_disk_{t}') for t in range(1, T+1)]
from_peg = [Int(f'from_peg_{t}') for t in range(1, T+1)]
to_peg   = [Int(f'to_peg_{t}')   for t in range(1, T+1)]

# Total number of moves used
total_moves = Int('total_moves')

# Basic bounds on total_moves
solver.add(total_moves >= 0, total_moves <= T)

# Initial state: all disks on peg A (index 0)
for d in range(1,5):
    solver.add(disk_peg[d-1][0] == 0)

# Constraints for each step
for t in range(1, T+1):
    # Move disk bounds
    solver.add(Implies(t <= total_moves, And(move_disk[t-1] >= 1, move_disk[t-1] <= 4)))
    solver.add(Implies(t > total_moves, move_disk[t-1] == 0))

    # Peg bounds
    solver.add(Implies(t <= total_moves,
                       And(from_peg[t-1] >= 0, from_peg[t-1] <= 3,
                           to_peg[t-1]   >= 0, to_peg[t-1]   <= 3,
                           from_peg[t-1] != to_peg[t-1])))
    solver.add(Implies(t > total_moves, from_peg[t-1] == to_peg[t-1]))

    # Update disk positions
    for d in range(1,5):
        prev = disk_peg[d-1][t-1]
        curr = disk_peg[d-1][t]
        # Disk moves if it is the chosen disk
        solver.add(curr == If(move_disk[t-1] == d, to_peg[t-1], prev))
        # If moved, source peg matches
        solver.add(Implies(move_disk[t-1] == d, disk_peg[d-1][t-1] == from_peg[t-1]))
        # If moved, dest peg matches
        solver.add(Implies(move_disk[t-1] == d, disk_peg[d-1][t] == to_peg[t-1]))
        # Top disk constraint: no smaller disk on source before move
        smaller_src = [disk_peg[s-1][t-1] != from_peg[t-1] for s in range(1, d)]
        if smaller_src:
            solver.add(Implies(move_disk[t-1] == d, And(smaller_src)))
        # No smaller disk on dest after move
        smaller_dest = [disk_peg[s-1][t] != to_peg[t-1] for s in range(1, d)]
        if smaller_dest:
            solver.add(Implies(move_disk[t-1] == d, And(smaller_dest)))

    # After total_moves, positions stay the same
    for d in range(1,5):
        solver.add(Implies(t > total_moves, disk_peg[d-1][t] == disk_peg[d-1][t-1]))

# Final state: all disks on peg D (index 3) at time total_moves
for d in range(1,5):
    for t in range(T+1):
        solver.add(Implies(t == total_moves, disk_peg[d-1][t] == 3))

# Each disk must visit peg B (1) and peg C (2) at least once before or at total_moves
for d in range(1,5):
    # Visit B
    solver.add(Or([And(t <= total_moves, disk_peg[d-1][t] == 1) for t in range(T+1)]))
    # Visit C
    solver.add(Or([And(t <= total_moves, disk_peg[d-1][t] == 2) for t in range(T+1)]))

# Minimize total_moves
solver.minimize(total_moves)

# Solve
result = solver.check()
if result == sat:
    model = solver.model()
    print("STATUS: sat")
    tm = model[total_moves].as_long()
    print(f"total_moves = {tm}")
    peg_map = {0:'A',1:'B',2:'C',3:'D'}
    for t in range(1, tm+1):
        disk = model[move_disk[t-1]].as_long()
        fpeg = peg_map[model[from_peg[t-1]].as_long()]
        tpeg = peg_map[model[to_peg[t-1]].as_long()]
        print(f"step: {t}, disk: {disk}, from: {fpeg}, to: {tpeg}")
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")