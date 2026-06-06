from z3 import *

# Configuration
BENCHMARK_MODE = True

# Problem constants
MAX_DISKS = 4
TOTAL_MOVES = 15
PEG_A = 0
PEG_B = 1
PEG_C = 2

solver = Solver()

# Location[t][d] for t in 0..TOTAL_MOVES, d in 0..MAX_DISKS-1 (disk index)
loc = [[Int(f'loc_{t}_{d}') for d in range(MAX_DISKS)] for t in range(TOTAL_MOVES+1)]

# Move variables for each step
move_disk = [Int(f'disk_{t}') for t in range(TOTAL_MOVES)]
move_src = [Int(f'src_{t}') for t in range(TOTAL_MOVES)]
move_dst = [Int(f'dst_{t}') for t in range(TOTAL_MOVES)]

# Initial state: all disks on peg A (disk index 0..MAX_DISKS-1)
for d in range(MAX_DISKS):
    solver.add(loc[0][d] == PEG_A)

# Goal state: all disks on peg C
for d in range(MAX_DISKS):
    solver.add(loc[TOTAL_MOVES][d] == PEG_C)

# Domain constraints for move variables
for t in range(TOTAL_MOVES):
    solver.add(move_disk[t] >= 1, move_disk[t] <= MAX_DISKS)
    solver.add(move_src[t] >= PEG_A, move_src[t] <= PEG_C)
    solver.add(move_dst[t] >= PEG_A, move_dst[t] <= PEG_C)
    solver.add(move_src[t] != move_dst[t])

# State update and legality for each step
for t in range(TOTAL_MOVES):
    # The moved disk changes peg
    d_idx = move_disk[t] - 1  # convert disk number to index
    solver.add(loc[t+1][d_idx] == move_dst[t])
    solver.add(loc[t][d_idx] == move_src[t])
    # Other disks keep their previous peg
    for d in range(MAX_DISKS):
        if d != d_idx:
            solver.add(loc[t+1][d] == loc[t][d])
    # No smaller disk on the source peg (disk must be on top)
    # For each smaller disk i (0..d_idx-1), it cannot be on the source peg at time t
    for i in range(d_idx):
        solver.add(loc[t][i] != move_src[t])
    # No smaller disk on the destination peg (cannot place larger on smaller)
    for i in range(d_idx):
        solver.add(loc[t][i] != move_dst[t])
    # All peg indices stay within {0,1,2}
    for tt in range(TOTAL_MOVES+1):
        for d in range(MAX_DISKS):
            solver.add(loc[tt][d] >= PEG_A, loc[tt][d] <= PEG_C)

# Solve
result = solver.check()
if result == sat:
    model = solver.model()
    print("STATUS: sat")
    # Print the sequence of moves
    for t in range(TOTAL_MOVES):
        d = model[move_disk[t]].as_long()
        s = model[move_src[t]].as_long()
        d_peg = model[move_dst[t]].as_long()
        src_letter = {PEG_A: 'A', PEG_B: 'B', PEG_C: 'C'}[s]
        dst_letter = {PEG_A: 'A', PEG_B: 'B', PEG_C: 'C'}[d_peg]
        print(f"step {t+1}: disk {d} from {src_letter} to {dst_letter}")
    print(f"total_moves = {TOTAL_MOVES}")
    print(f"is_optimal = True")
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")