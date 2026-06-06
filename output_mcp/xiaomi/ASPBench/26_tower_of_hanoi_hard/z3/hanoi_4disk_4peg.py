from z3 import *

# We'll use an optimization approach to find the minimum number of moves.
# Model: at each time step t, each disk is on some peg.
# We need to track which peg each disk is on at each step.

NUM_DISKS = 4
NUM_PEGS = 4
# We'll try increasing move counts starting from a lower bound
# For 4 disks, 4 pegs, Frame-Stewart gives ~9 moves without extra constraints
# With pilgrim constraint, expected optimal is 19

MAX_MOVES = 25  # Upper bound for search

# Peg encoding: A=0, B=1, C=2, D=3
PEG_A, PEG_B, PEG_C, PEG_D = 0, 1, 2, 3

def solve_hanoi(num_moves):
    """Try to solve with exactly num_moves moves."""
    solver = Solver()
    
    # disk_peg[d][t] = peg where disk d is at time step t
    # Disks indexed 0..3 (disk 0 = smallest, disk 3 = largest)
    disk_peg = [[Int(f'disk_{d}_step_{t}') for t in range(num_moves + 1)] for d in range(NUM_DISKS)]
    
    # Each disk is on a valid peg at each step
    for d in range(NUM_DISKS):
        for t in range(num_moves + 1):
            solver.add(And(disk_peg[d][t] >= 0, disk_peg[d][t] <= 3))
    
    # Initial state: all disks on peg A
    for d in range(NUM_DISKS):
        solver.add(disk_peg[d][0] == PEG_A)
    
    # Goal state: all disks on peg D
    for d in range(NUM_DISKS):
        solver.add(disk_peg[d][num_moves] == PEG_D)
    
    # Move variables: move_disk[t] = disk moved at step t (0-indexed)
    move_disk = [Int(f'move_disk_{t}') for t in range(num_moves)]
    move_from = [Int(f'move_from_{t}') for t in range(num_moves)]
    move_to = [Int(f'move_to_{t}') for t in range(num_moves)]
    
    for t in range(num_moves):
        solver.add(And(move_disk[t] >= 0, move_disk[t] < NUM_DISKS))
        solver.add(And(move_from[t] >= 0, move_from[t] <= 3))
        solver.add(And(move_to[t] >= 0, move_to[t] <= 3))
        solver.add(move_from[t] != move_to[t])
    
    # Consistency: if disk d is moved at step t, its peg changes from move_from to move_to
    # If disk d is NOT moved at step t, its peg stays the same
    for t in range(num_moves):
        for d in range(NUM_DISKS):
            is_moved = (move_disk[t] == d)
            solver.add(Implies(is_moved, And(
                move_from[t] == disk_peg[d][t],
                move_to[t] == disk_peg[d][t + 1]
            )))
            solver.add(Implies(Not(is_moved), disk_peg[d][t + 1] == disk_peg[d][t]))
    
    # Exactly one disk moved per step (already implicit from move_disk being a single Int)
    
    # Standard Hanoi rules: larger disk cannot be on top of smaller disk
    # At each time step, for any two disks on the same peg, smaller must be above larger
    # "Above" means: if disk i < disk j (i is smaller), and they're on the same peg,
    # then there's no disk between them that violates ordering.
    # Simpler: on each peg, disks must be in decreasing order of size from bottom to top.
    # Since we only track which peg each disk is on (not position on peg),
    # we need: if disk d1 and d2 are on the same peg and d1 < d2 (d1 smaller),
    # then d1 must have been placed after d2 was already there.
    # Actually, the key constraint is: a larger disk cannot be placed ON a smaller disk.
    # When moving disk d to a peg at step t, all disks already on that peg must be larger than d.
    
    for t in range(num_moves):
        for d in range(NUM_DISKS):
            # When disk d is moved to move_to[t] at step t:
            # All disks currently on move_to[t] (at time t, before the move) must be larger
            is_moved = (move_disk[t] == d)
            for d2 in range(NUM_DISKS):
                if d2 != d:
                    # If d2 is on the destination peg at time t and d is being moved there
                    # d2 must be larger than d (d2 > d means d2 has larger number)
                    solver.add(Implies(
                        And(is_moved, disk_peg[d2][t] == move_to[t]),
                        d2 > d  # d2 is a larger disk
                    ))
    
    # Pilgrim's Journey: every disk must visit peg B and peg C at least once
    for d in range(NUM_DISKS):
        visited_B = Or([disk_peg[d][t] == PEG_B for t in range(num_moves + 1)])
        visited_C = Or([disk_peg[d][t] == PEG_C for t in range(num_moves + 1)])
        solver.add(visited_B)
        solver.add(visited_C)
    
    return solver, disk_peg, move_disk, move_from, move_to

# Try from 19 moves upward
for num_moves in range(19, MAX_MOVES + 1):
    print(f"Trying {num_moves} moves...")
    solver, disk_peg, move_disk, move_from, move_to = solve_hanoi(num_moves)
    result = solver.check()
    
    if result == sat:
        m = solver.model()
        print(f"\nSTATUS: sat")
        print(f"total_moves: {num_moves}")
        print(f"\nMoves:")
        for t in range(num_moves):
            d = m[move_disk[t]].as_long()
            f = m[move_from[t]].as_long()
            to = m[move_to[t]].as_long()
            peg_names = ['A', 'B', 'C', 'D']
            print(f"  Step {t+1}: Move disk {d+1} from {peg_names[f]} to {peg_names[to]}")
        
        # Verify pilgrim constraint
        print(f"\nPilgrim journey verification:")
        for d in range(NUM_DISKS):
            pegs_visited = set()
            for t in range(num_moves + 1):
                pegs_visited.add(m[disk_peg[d][t]].as_long())
            peg_names = ['A', 'B', 'C', 'D']
            visited = [peg_names[p] for p in sorted(pegs_visited)]
            print(f"  Disk {d+1} visited pegs: {visited}")
        break
    else:
        print(f"  No solution with {num_moves} moves.")