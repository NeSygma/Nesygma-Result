from z3 import *

# Tower of Hanoi with 4 disks, 4 pegs, mandatory B and C visits
# Peg encoding: 0=A, 1=B, 2=C, 3=D
# Disks: 0 (smallest, disk 1) to 3 (largest, disk 4)

NUM_DISKS = 4
NUM_PEGS = 4
PEG_A, PEG_B, PEG_C, PEG_D = 0, 1, 2, 3

def solve_hanoi(T):
    solver = Solver()
    
    # State: peg[t][d] = peg where disk d is at time t
    peg = [[Int(f"peg_{t}_{d}") for d in range(NUM_DISKS)] for t in range(T+1)]
    
    # moved[t] = which disk moves at step t (0 to NUM_DISKS-1)
    moved = [Int(f"moved_{t}") for t in range(T)]
    
    # Domains
    for t in range(T+1):
        for d in range(NUM_DISKS):
            solver.add(peg[t][d] >= 0, peg[t][d] <= 3)
    
    for t in range(T):
        solver.add(moved[t] >= 0, moved[t] <= 3)
    
    # Initial: all on peg A
    for d in range(NUM_DISKS):
        solver.add(peg[0][d] == PEG_A)
    
    # Goal: all on peg D
    for d in range(NUM_DISKS):
        solver.add(peg[T][d] == PEG_D)
    
    # For each step t:
    for t in range(T):
        # Exactly one disk moves: the moved disk changes peg, all others stay
        for d in range(NUM_DISKS):
            # If d is the moved disk, its peg can change
            # If d is NOT the moved disk, its peg stays the same
            solver.add(Implies(moved[t] != d, peg[t+1][d] == peg[t][d]))
        
        # The moved disk must actually change peg
        # Use Or-loop pattern since moved[t] is symbolic
        for d in range(NUM_DISKS):
            solver.add(Implies(moved[t] == d, peg[t+1][d] != peg[t][d]))
        
        # Top disk constraint: if disk d moves at step t, then no smaller disk
        # is on the same source peg at time t
        for d in range(NUM_DISKS):
            for s in range(d):  # s is smaller than d
                # If d moves, then smaller s is NOT on peg[t][d]
                solver.add(Implies(moved[t] == d, peg[t][s] != peg[t][d]))
        
        # Top disk constraint at destination: if disk d moves to a peg,
        # no smaller disk is already there at time t+1
        for d in range(NUM_DISKS):
            for s in range(d):
                solver.add(Implies(moved[t] == d, peg[t+1][s] != peg[t+1][d]))
    
    # Pilgrim's Journey: every disk must land on B at least once and C at least once
    for d in range(NUM_DISKS):
        visited_B = [And(moved[t] == d, peg[t+1][d] == PEG_B) for t in range(T)]
        solver.add(Or(visited_B))
        
        visited_C = [And(moved[t] == d, peg[t+1][d] == PEG_C) for t in range(T)]
        solver.add(Or(visited_C))
    
    result = solver.check()
    if result == sat:
        return solver.model(), peg, moved, T
    else:
        return None, None, None, T

# Try increasing T
for T in range(15, 30):
    print(f"Trying T = {T}...")
    m, peg, moved, steps = solve_hanoi(T)
    if m is not None:
        print(f"Found solution with T = {T}")
        print("STATUS: sat")
        print(f"total_moves = {T}")
        print()
        print("Move sequence:")
        peg_names = ["A", "B", "C", "D"]
        for t in range(T):
            d_val = m[moved[t]].as_long()
            from_p = m[peg[t][d_val]].as_long()
            to_p = m[peg[t+1][d_val]].as_long()
            print(f"Step {t+1}: Disk {d_val+1} from {peg_names[from_p]} to {peg_names[to_p]}")
        
        # Also print the full state at each step
        print()
        print("Full state trace:")
        for t in range(T+1):
            state_str = f"Time {t}: "
            for p_name, p_idx in [("A",0),("B",1),("C",2),("D",3)]:
                disks_on_peg = []
                for d in range(NUM_DISKS):
                    if m[peg[t][d]].as_long() == p_idx:
                        disks_on_peg.append(d+1)
                state_str += f"{p_name}:{disks_on_peg} "
            print(state_str)
        break
else:
    print("STATUS: unsat")
    print("No solution found up to T=29")