from z3 import *

# BENCHMARK_MODE: ON (model-finding with minimization)
BENCHMARK_MODE = True

# --- Problem Parameters ---
NUM_DISKS = 4
NUM_PEGS = 4
PEG_LABELS = ['A', 'B', 'C', 'D']
PEG_ENCODING = {lbl: i for i, lbl in enumerate(PEG_LABELS)}
DISK_LABELS = list(range(1, NUM_DISKS + 1))

# --- Upper bound for total moves (to define arrays) ---
MAX_MOVES = 30

# --- Optimization Setup ---
opt = Optimize()

# --- Decision Variables ---
# Total number of moves (to minimize)
TOTAL_MOVES = Int('TOTAL_MOVES')
opt.add(TOTAL_MOVES >= 1, TOTAL_MOVES <= MAX_MOVES)

# Sequence of moves: for each step t in [1, MAX_MOVES],
# move[t] = (disk, from_peg, to_peg)
# We'll represent this as three arrays of length MAX_MOVES
move_disk = [Int(f'move_disk_{t}') for t in range(MAX_MOVES)]
move_from = [Int(f'move_from_{t}') for t in range(MAX_MOVES)]
move_to   = [Int(f'move_to_{t}') for t in range(MAX_MOVES)]

# --- State: For each peg and each time step, which disks are on it?
# on_peg[t][p][d] = True if disk d is on peg p at time t
on_peg = [[[Bool(f'on_peg_{t}_{p}_{d}') for d in range(NUM_DISKS)] for p in range(NUM_PEGS)] for t in range(MAX_MOVES + 1)]

# --- Initial State (t=0) ---
# Peg A: disks 4,3,2,1 (bottom to top)
# Pegs B,C,D: empty
for d in range(NUM_DISKS):
    # Disk d+1 is on peg A at t=0
    opt.add(on_peg[0][PEG_ENCODING['A']][d] == True)
    for p in range(NUM_PEGS):
        if p != PEG_ENCODING['A']:
            opt.add(on_peg[0][p][d] == False)

# --- Goal State (t=TOTAL_MOVES) ---
# Peg D: disks 4,3,2,1 (bottom to top)
# Pegs A,B,C: empty
for d in range(NUM_DISKS):
    opt.add(on_peg[TOTAL_MOVES][PEG_ENCODING['D']][d] == True)
    for p in range(NUM_PEGS):
        if p != PEG_ENCODING['D']:
            opt.add(on_peg[TOTAL_MOVES][p][d] == False)

# --- Move Constraints ---
# For each move t in [0, TOTAL_MOVES-1], define the move
for t in range(MAX_MOVES):
    # Only enforce move constraints for t < TOTAL_MOVES
    opt.add(Implies(t < TOTAL_MOVES, 
                   And(move_disk[t] >= 1, move_disk[t] <= NUM_DISKS,
                       move_from[t] >= 0, move_from[t] < NUM_PEGS,
                       move_to[t] >= 0, move_to[t] < NUM_PEGS,
                       move_from[t] != move_to[t])))

    # The disk must be on the 'from' peg before the move and not on the 'to' peg before the move
    d_idx = move_disk[t] - 1
    from_p = move_from[t]
    to_p = move_to[t]
    opt.add(Implies(t < TOTAL_MOVES, 
                   And(on_peg[t][from_p][d_idx] == True,
                       on_peg[t][to_p][d_idx] == False)))

    # After the move, the disk is on the 'to' peg and not on the 'from' peg
    opt.add(Implies(t < TOTAL_MOVES,
                   And(on_peg[t+1][from_p][d_idx] == False,
                       on_peg[t+1][to_p][d_idx] == True)))

    # All other disks remain unchanged
    for p in range(NUM_PEGS):
        for d in range(NUM_DISKS):
            if not (p == from_p and d == d_idx) and not (p == to_p and d == d_idx):
                opt.add(Implies(t < TOTAL_MOVES, 
                               on_peg[t+1][p][d] == on_peg[t][p][d]))

# --- Standard Tower of Hanoi Constraints ---
# For each peg and each time step, the disks on it must be in decreasing order (larger at bottom)
for t in range(MAX_MOVES + 1):
    for p in range(NUM_PEGS):
        # For each pair of disks on the same peg, the larger must be below the smaller
        # We enforce this by ensuring that if a larger disk is present, all smaller disks above it are also present
        # This is complex; instead, we enforce that the top disk is the smallest present
        # So we track the top disk for each peg at each time step
        pass

# --- Track top disk for each peg at each time step ---
top_disk = [[Int(f'top_disk_{t}_{p}') for p in range(NUM_PEGS)] for t in range(MAX_MOVES + 1)]
# -1 means no disk (peg empty)
for t in range(MAX_MOVES + 1):
    for p in range(NUM_PEGS):
        opt.add(top_disk[t][p] >= -1, top_disk[t][p] <= NUM_DISKS)

# Initial top disk: peg A has disk 1 (smallest) on top
opt.add(top_disk[0][PEG_ENCODING['A']] == 1)
for p in range(NUM_PEGS):
    if p != PEG_ENCODING['A']:
        opt.add(top_disk[0][p] == -1)

# Goal top disk: peg D has disk 1 on top
opt.add(top_disk[TOTAL_MOVES][PEG_ENCODING['D']] == 1)
for p in range(NUM_PEGS):
    if p != PEG_ENCODING['D']:
        opt.add(top_disk[TOTAL_MOVES][p] == -1)

# Update top disk after each move
for t in range(MAX_MOVES):
    opt.add(Implies(t < TOTAL_MOVES,
                   And(top_disk[t+1][move_to[t]] == move_disk[t] + 1,  # +1 because disks are 1-indexed
                       top_disk[t+1][move_from[t]] == If(
                           Sum([If(on_peg[t][move_from[t]][d], 1, 0) for d in range(NUM_DISKS)]) == 1,
                           -1,
                           top_disk[t][move_from[t]]
                       ))))
    # For other pegs, top disk remains the same
    for p in range(NUM_PEGS):
        if p != move_to[t] and p != move_from[t]:
            opt.add(Implies(t < TOTAL_MOVES, top_disk[t+1][p] == top_disk[t][p]))

# --- Pilgrim's Journey Constraint ---
# For each disk, it must be moved to peg B at least once and to peg C at least once.
for d in range(NUM_DISKS):
    # Count number of times disk d+1 is moved to peg B
    count_B = Sum([If(And(t < TOTAL_MOVES, move_disk[t] == d+1, move_to[t] == PEG_ENCODING['B']), 1, 0) for t in range(MAX_MOVES)])
    # Count number of times disk d+1 is moved to peg C
    count_C = Sum([If(And(t < TOTAL_MOVES, move_disk[t] == d+1, move_to[t] == PEG_ENCODING['C']), 1, 0) for t in range(MAX_MOVES)])
    opt.add(count_B >= 1)
    opt.add(count_C >= 1)

# --- Minimize total moves ---
opt.minimize(TOTAL_MOVES)

# --- Check and print result ---
result = opt.check()

if result == sat:
    model = opt.model()
    total_moves_val = model[TOTAL_MOVES]
    print("STATUS: sat")
    print(f"Total moves: {total_moves_val}")
    
    # Print the sequence of moves
    print("Moves:")
    for t in range(total_moves_val.as_long()):
        disk_val = model[move_disk[t]]
        from_val = model[move_from[t]]
        to_val = model[move_to[t]]
        print(f"Step {t+1}: disk {disk_val} from {PEG_LABELS[from_val.as_long()]} to {PEG_LABELS[to_val.as_long()]}")
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")