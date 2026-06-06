from z3 import *

# Tower of Hanoi with 4 disks, 4 pegs, mandatory B and C visits
# We need to find the minimum number of moves.
# Expected optimal: 19 moves.

# Let's model this as a planning problem with bounded steps.
# We'll try increasing T until we find a solution.

# Peg encoding: 0=A, 1=B, 2=C, 3=D
# Disks: 1 (smallest) to 4 (largest)

NUM_DISKS = 4
NUM_PEGS = 4
PEG_A, PEG_B, PEG_C, PEG_D = 0, 1, 2, 3

# We'll search for minimal T
# Expected optimal is 19, so let's start around there

def solve_hanoi(T):
    solver = Solver()
    
    # State variables: peg_of_disk[t][d] = peg where disk d is at time t
    # Time steps: 0 = initial, T = final
    peg = [[Int(f"peg_{t}_{d}") for d in range(NUM_DISKS)] for t in range(T+1)]
    
    # Action variables: move[t] = (disk, from_peg, to_peg) for step t (0-indexed, step t goes from t to t+1)
    # We'll encode which disk is moved at step t
    moved_disk = [Int(f"moved_{t}") for t in range(T)]
    # from_peg and to_peg can be derived from peg state, but we need to constrain them
    
    # Domain constraints
    for t in range(T+1):
        for d in range(NUM_DISKS):
            solver.add(peg[t][d] >= 0, peg[t][d] <= 3)
    
    for t in range(T):
        solver.add(moved_disk[t] >= 0, moved_disk[t] <= 3)
    
    # Initial state: all disks on peg A (0)
    for d in range(NUM_DISKS):
        solver.add(peg[0][d] == PEG_A)
    
    # Goal state: all disks on peg D (3)
    for d in range(NUM_DISKS):
        solver.add(peg[T][d] == PEG_D)
    
    # Standard Tower of Hanoi constraints:
    
    # 1. Only top disk can move: a disk can only move if all smaller disks are on different pegs
    # Actually, a disk can move if no smaller disk is on the same peg.
    # At each step t, the moved disk must be the top disk on its source peg.
    
    for t in range(T):
        d = moved_disk[t]
        # The moved disk must be on top: no smaller disk is on the same peg at time t
        for smaller in range(NUM_DISKS):
            if smaller < 4:  # all disks smaller than d
                # If smaller < d, then smaller disk must NOT be on the same peg as d at time t
                # We use implication: if moved_disk[t] == d, then for all smaller < d, peg[t][smaller] != peg[t][d]
                pass  # We'll handle this differently
        
        # Actually, let's use a different encoding. For each step t and each disk d:
        # disk d moves at step t iff:
        #   - peg[t][d] != peg[t+1][d] (disk changes peg)
        #   - for all smaller disks s < d: peg[t][s] != peg[t][d] (d is top on source)
        #   - for all smaller disks s < d: peg[t+1][s] != peg[t+1][d] (d is top on destination)
        #   - for all other disks k != d: peg[t][k] == peg[t+1][k] (only one disk moves)
    
    # Let's use a cleaner encoding with explicit move variables
    
    # For each step t, exactly one disk moves
    # moved_disk[t] indicates which disk moves (0-3)
    
    # Constraint: only the moved disk changes peg
    for t in range(T):
        for d in range(NUM_DISKS):
            # If disk d is the moved disk, its peg can change
            # If disk d is NOT the moved disk, its peg stays the same
            solver.add(Implies(moved_disk[t] != d, peg[t+1][d] == peg[t][d]))
    
    # Constraint: the moved disk must change peg (it actually moves somewhere)
    for t in range(T):
        d = moved_disk[t]
        solver.add(peg[t+1][d] != peg[t][d])
    
    # Constraint: the moved disk must be the top disk on its source peg
    # i.e., no smaller disk is on the same source peg at time t
    for t in range(T):
        for d in range(NUM_DISKS):
            for s in range(d):  # smaller disks
                # If disk d moves at step t, then smaller disk s is NOT on peg[t][d]
                solver.add(Implies(And(moved_disk[t] == d, peg[t][s] == peg[t][d]), False))
                # Equivalent: If d moves, then peg[t][s] != peg[t][d] for all s < d
                solver.add(Implies(moved_disk[t] == d, peg[t][s] != peg[t][d]))
    
    # Constraint: the moved disk must land on top at destination
    # i.e., no smaller disk is on the destination peg at time t+1
    for t in range(T):
        for d in range(NUM_DISKS):
            for s in range(d):  # smaller disks
                solver.add(Implies(moved_disk[t] == d, peg[t+1][s] != peg[t+1][d]))
    
    # Constraint: larger disk cannot be placed on smaller disk
    # This is already enforced by the top-disk constraints above.
    # If a larger disk moves to a peg, no smaller disk is there (at destination time).
    # If a smaller disk moves to a peg with a larger disk, that's fine.
    
    # Pilgrim's Journey constraint:
    # Every disk must land on peg B (1) at least once AND peg C (2) at least once.
    # A disk "lands on" a peg when it is moved to that peg.
    # So for each disk d, there must exist a step t where moved_disk[t] == d and peg[t+1][d] == PEG_B
    # AND a step t where moved_disk[t] == d and peg[t+1][d] == PEG_C
    
    for d in range(NUM_DISKS):
        # Disk d must land on B at least once
        visited_B = [And(moved_disk[t] == d, peg[t+1][d] == PEG_B) for t in range(T)]
        solver.add(Or(visited_B))
        
        # Disk d must land on C at least once
        visited_C = [And(moved_disk[t] == d, peg[t+1][d] == PEG_C) for t in range(T)]
        solver.add(Or(visited_C))
    
    # Try to solve
    result = solver.check()
    if result == sat:
        m = solver.model()
        return m, peg, moved_disk, T
    else:
        return None, None, None, T

# Try increasing T from some lower bound
# Minimum moves for 4 disks 4 pegs without extra constraint: Frame-Stewart gives 9
# With mandatory B and C visits, expected optimal is 19
# Let's try from 15 upward

for T in range(15, 25):
    print(f"Trying T = {T}...")
    m, peg, moved_disk, steps = solve_hanoi(T)
    if m is not None:
        print(f"Found solution with T = {T}")
        # Print the solution
        print("STATUS: sat")
        print(f"total_moves = {T}")
        print()
        print("Move sequence:")
        for t in range(T):
            d = m[moved_disk[t]].as_long()
            from_p = m[peg[t][d]].as_long()
            to_p = m[peg[t+1][d]].as_long()
            peg_names = ["A", "B", "C", "D"]
            print(f"Step {t+1}: Disk {d+1} from {peg_names[from_p]} to {peg_names[to_p]}")
        break
else:
    print("STATUS: unsat")
    print("No solution found up to T=24")