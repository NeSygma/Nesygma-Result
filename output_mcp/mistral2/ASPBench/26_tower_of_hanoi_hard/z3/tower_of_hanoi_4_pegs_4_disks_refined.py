from z3 import *

# BENCHMARK_MODE: ON (model-finding with minimization)
BENCHMARK_MODE = True

# --- Problem Parameters ---
NUM_DISKS = 4
NUM_PEGS = 4
PEG_LABELS = ['A', 'B', 'C', 'D']
PEG_ENCODING = {lbl: i for i, lbl in enumerate(PEG_LABELS)}
DISK_LABELS = list(range(1, NUM_DISKS + 1))

# --- Expected optimal moves ---
EXPECTED_MOVES = 19

# --- Solver Setup ---
solver = Solver()

# --- Decision Variables ---
# Sequence of moves: for each step t in [0, EXPECTED_MOVES-1],
# move[t] = (disk, from_peg, to_peg)
move_disk = [Int(f'move_disk_{t}') for t in range(EXPECTED_MOVES)]
move_from = [Int(f'move_from_{t}') for t in range(EXPECTED_MOVES)]
move_to   = [Int(f'move_to_{t}') for t in range(EXPECTED_MOVES)]

# --- State: For each peg and each time step, which disks are on it?
# on_peg[t][p][d] = True if disk d is on peg p at time t
on_peg = [[[Bool(f'on_peg_{t}_{p}_{d}') for d in range(NUM_DISKS)] for p in range(NUM_PEGS)] for t in range(EXPECTED_MOVES + 1)]

# --- Initial State (t=0) ---
# Peg A: disks 4,3,2,1 (bottom to top)
# Pegs B,C,D: empty
for d in range(NUM_DISKS):
    # Disk d+1 is on peg A at t=0
    solver.add(on_peg[0][PEG_ENCODING['A']][d] == True)
    for p in range(NUM_PEGS):
        if p != PEG_ENCODING['A']:
            solver.add(on_peg[0][p][d] == False)

# --- Goal State (t=EXPECTED_MOVES) ---
# Peg D: disks 4,3,2,1 (bottom to top)
# Pegs A,B,C: empty
for d in range(NUM_DISKS):
    solver.add(on_peg[EXPECTED_MOVES][PEG_ENCODING['D']][d] == True)
    for p in range(NUM_PEGS):
        if p != PEG_ENCODING['D']:
            solver.add(on_peg[EXPECTED_MOVES][p][d] == False)

# --- Move Constraints ---
for t in range(EXPECTED_MOVES):
    # Disk, from_peg, to_peg must be valid
    solver.add(move_disk[t] >= 1, move_disk[t] <= NUM_DISKS)
    solver.add(move_from[t] >= 0, move_from[t] < NUM_PEGS)
    solver.add(move_to[t] >= 0, move_to[t] < NUM_PEGS)
    solver.add(move_from[t] != move_to[t])

    d_idx = move_disk[t] - 1
    from_p = move_from[t]
    to_p = move_to[t]

    # The disk must be on the 'from' peg before the move and not on the 'to' peg before the move
    solver.add(on_peg[t][from_p][d_idx] == True)
    solver.add(on_peg[t][to_p][d_idx] == False)

    # After the move, the disk is on the 'to' peg and not on the 'from' peg
    solver.add(on_peg[t+1][from_p][d_idx] == False)
    solver.add(on_peg[t+1][to_p][d_idx] == True)

    # All other disks remain unchanged
    for p in range(NUM_PEGS):
        for d in range(NUM_DISKS):
            if not (p == from_p and d == d_idx) and not (p == to_p and d == d_idx):
                solver.add(on_peg[t+1][p][d] == on_peg[t][p][d])

# --- Standard Tower of Hanoi Constraints ---
# For each peg and each time step, the disks on it must be in decreasing order (larger at bottom)
for t in range(EXPECTED_MOVES + 1):
    for p in range(NUM_PEGS):
        # For each disk, if it is on the peg, all larger disks must also be on the peg
        for d in range(NUM_DISKS):
            # If disk d is on peg p at time t, then all larger disks must also be on peg p
            larger_disks = [on_peg[t][p][k] for k in range(d + 1, NUM_DISKS)]
            solver.add(Implies(on_peg[t][p][d], And(larger_disks)))

# --- Pilgrim's Journey Constraint ---
# For each disk, it must be moved to peg B at least once and to peg C at least once.
for d in range(NUM_DISKS):
    # Count number of times disk d+1 is moved to peg B
    count_B = Sum([If(And(move_disk[t] == d+1, move_to[t] == PEG_ENCODING['B']), 1, 0) for t in range(EXPECTED_MOVES)])
    # Count number of times disk d+1 is moved to peg C
    count_C = Sum([If(And(move_disk[t] == d+1, move_to[t] == PEG_ENCODING['C']), 1, 0) for t in range(EXPECTED_MOVES)])
    solver.add(count_B >= 1)
    solver.add(count_C >= 1)

# --- Check and print result ---
result = solver.check()

if result == sat:
    model = solver.model()
    print("STATUS: sat")
    
    # Print the sequence of moves
    print("Moves:")
    for t in range(EXPECTED_MOVES):
        disk_val = model[move_disk[t]]
        from_val = model[move_from[t]]
        to_val = model[move_to[t]]
        print(f"Step {t+1}: disk {disk_val} from {PEG_LABELS[from_val.as_long()]} to {PEG_LABELS[to_val.as_long()]}")
    
    # Verify final state
    print("\nFinal state verification:")
    for p in range(NUM_PEGS):
        peg_name = PEG_LABELS[p]
        disks_on_peg = []
        for d in range(NUM_DISKS):
            if model[on_peg[EXPECTED_MOVES][p][d]]:
                disks_on_peg.append(d+1)
        print(f"Peg {peg_name}: {sorted(disks_on_peg)}")
    
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")