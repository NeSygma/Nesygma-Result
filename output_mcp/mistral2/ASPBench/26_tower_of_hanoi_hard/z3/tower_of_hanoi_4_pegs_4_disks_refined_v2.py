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
# We model the state as a 2D array: state[t][p] is a Z3 Array from disk to Bool (True if disk is on peg p at time t)
state = [[Array(f'state_{t}_{p}', IntSort(), BoolSort()) for p in range(NUM_PEGS)] for t in range(EXPECTED_MOVES + 1)]

# --- Helper: Disk d is on peg p at time t ---
def disk_on(t, p, d):
    return state[t][p][d]

# --- Initial State (t=0) ---
# Peg A: disks 4,3,2,1 (bottom to top)
# Pegs B,C,D: empty
for d in range(1, NUM_DISKS + 1):
    solver.add(disk_on(0, PEG_ENCODING['A'], d) == True)
    for p in range(NUM_PEGS):
        if p != PEG_ENCODING['A']:
            solver.add(disk_on(0, p, d) == False)

# --- Goal State (t=EXPECTED_MOVES) ---
# Peg D: disks 4,3,2,1 (bottom to top)
# Pegs A,B,C: empty
for d in range(1, NUM_DISKS + 1):
    solver.add(disk_on(EXPECTED_MOVES, PEG_ENCODING['D'], d) == True)
    for p in range(NUM_PEGS):
        if p != PEG_ENCODING['D']:
            solver.add(disk_on(EXPECTED_MOVES, p, d) == False)

# --- Move Constraints ---
for t in range(EXPECTED_MOVES):
    # Disk, from_peg, to_peg must be valid
    solver.add(move_disk[t] >= 1, move_disk[t] <= NUM_DISKS)
    solver.add(move_from[t] >= 0, move_from[t] < NUM_PEGS)
    solver.add(move_to[t] >= 0, move_to[t] < NUM_PEGS)
    solver.add(move_from[t] != move_to[t])

    d = move_disk[t]
    from_p = move_from[t]
    to_p = move_to[t]

    # The disk must be on the 'from' peg before the move and not on the 'to' peg before the move
    solver.add(disk_on(t, from_p, d) == True)
    solver.add(disk_on(t, to_p, d) == False)

    # After the move, the disk is on the 'to' peg and not on the 'from' peg
    # For all disks except d, state remains the same
    for other_d in range(1, NUM_DISKS + 1):
        if other_d != d:
            solver.add(state[t+1][from_p][other_d] == state[t][from_p][other_d])
            solver.add(state[t+1][to_p][other_d] == state[t][to_p][other_d])
    # For disk d: update state
    solver.add(state[t+1][from_p][d] == False)
    solver.add(state[t+1][to_p][d] == True)
    # For all other pegs, state remains the same
    for p in range(NUM_PEGS):
        if p != from_p and p != to_p:
            for other_d in range(1, NUM_DISKS + 1):
                solver.add(state[t+1][p][other_d] == state[t][p][other_d])

# --- Standard Tower of Hanoi Constraints ---
# For each peg and each time step, the disks on it must be in decreasing order (larger at bottom)
for t in range(EXPECTED_MOVES + 1):
    for p in range(NUM_PEGS):
        # For each disk, if it is on the peg, all larger disks must also be on the peg
        for d in range(1, NUM_DISKS + 1):
            # If disk d is on peg p at time t, then all larger disks must also be on peg p
            larger_disks = [state[t][p][k] for k in range(d + 1, NUM_DISKS + 1)]
            solver.add(Implies(state[t][p][d], And(larger_disks)))

# --- Pilgrim's Journey Constraint ---
# For each disk, it must be moved to peg B at least once and to peg C at least once.
for d in range(1, NUM_DISKS + 1):
    # Count number of times disk d is moved to peg B
    count_B = Sum([If(And(move_disk[t] == d, move_to[t] == PEG_ENCODING['B']), 1, 0) for t in range(EXPECTED_MOVES)])
    # Count number of times disk d is moved to peg C
    count_C = Sum([If(And(move_disk[t] == d, move_to[t] == PEG_ENCODING['C']), 1, 0) for t in range(EXPECTED_MOVES)])
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
        for d in range(1, NUM_DISKS + 1):
            if model.evaluate(disk_on(EXPECTED_MOVES, p, d), model_completion=True):
                disks_on_peg.append(d)
        print(f"Peg {peg_name}: {sorted(disks_on_peg)}")
    
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")