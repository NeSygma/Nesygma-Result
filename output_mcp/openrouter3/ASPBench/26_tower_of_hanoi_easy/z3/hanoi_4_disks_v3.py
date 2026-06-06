from z3 import *

# Problem parameters
num_disks = 4
num_pegs = 3
max_moves = 15  # We'll try to find a solution with exactly 15 moves

# Peg indices: 0=A, 1=B, 2=C
peg_names = ['A', 'B', 'C']

# Create solver
solver = Solver()

# For each time step (move), track which disk is moved and from/to which peg
# We'll use 1-indexed moves for clarity
moves_disk = [Int(f'moves_disk_{t}') for t in range(max_moves + 1)]  # 0 unused
moves_from = [Int(f'moves_from_{t}') for t in range(max_moves + 1)]
moves_to = [Int(f'moves_to_{t}') for t in range(max_moves + 1)]

# For each disk and time step, track which peg it's on
# disk_peg[d][t] = peg where disk d is at time t (0-indexed time)
disk_peg = [[Int(f'disk_{d}_peg_{t}') for t in range(max_moves + 1)] for d in range(1, num_disks + 1)]

# Initial state: all disks on peg A (index 0)
for d in range(1, num_disks + 1):
    solver.add(disk_peg[d-1][0] == 0)  # All on peg A at time 0

# Goal state: all disks on peg C (index 2) in order [4,3,2,1] (bottom to top)
# This means at final time, disk 4 is at bottom, disk 1 at top
# We just need all disks on peg C at final time
for d in range(1, num_disks + 1):
    solver.add(disk_peg[d-1][max_moves] == 2)  # All on peg C at final time

# Constraint: Only one disk moved per time step
for t in range(1, max_moves + 1):
    # moves_disk[t] must be between 1 and num_disks
    solver.add(moves_disk[t] >= 1)
    solver.add(moves_disk[t] <= num_disks)
    
    # moves_from[t] and moves_to[t] must be between 0 and 2 (A, B, C)
    solver.add(moves_from[t] >= 0)
    solver.add(moves_from[t] <= 2)
    solver.add(moves_to[t] >= 0)
    solver.add(moves_to[t] <= 2)
    
    # From and to must be different
    solver.add(moves_from[t] != moves_to[t])

# Constraint: Disk movement affects state
for t in range(1, max_moves + 1):
    for d in range(1, num_disks + 1):
        # If disk d is moved at time t, it goes from moves_from[t] to moves_to[t]
        # Otherwise, it stays on the same peg as previous time
        solver.add(
            If(moves_disk[t] == d,
               disk_peg[d-1][t] == moves_to[t],
               disk_peg[d-1][t] == disk_peg[d-1][t-1])
        )

# Constraint: Disk can only be moved from top of stack
# For each time step, check that the moved disk is indeed on top of its source peg
for t in range(1, max_moves + 1):
    moved_disk = moves_disk[t]
    source_peg = moves_from[t]
    
    # The moved disk must be on the source peg at time t-1
    for d in range(1, num_disks + 1):
        solver.add(
            Implies(moved_disk == d, disk_peg[d-1][t-1] == source_peg)
        )
    
    # Check that no smaller disk is on top of the moved disk at the source peg
    # For each smaller disk (disk < moved_disk), it cannot be on the same peg
    # unless it's already been moved away
    # We need to check all smaller disks
    for smaller in range(1, num_disks + 1):
        # smaller < moved_disk means smaller is a smaller disk
        solver.add(
            Implies(
                And(moved_disk > smaller, disk_peg[smaller-1][t-1] == source_peg),
                False
            )
        )

# Constraint: Larger disk cannot be placed on smaller disk
# For each time step, check that when moving a disk to a peg,
# it must be smaller than all disks already on that peg
for t in range(1, max_moves + 1):
    moved_disk = moves_disk[t]
    dest_peg = moves_to[t]
    
    # For each disk d on dest_peg at time t-1, moved_disk must be smaller than d
    for d in range(1, num_disks + 1):
        solver.add(
            Implies(
                And(disk_peg[d-1][t-1] == dest_peg, d != moved_disk),
                moved_disk < d
            )
        )

# Add constraint that we use exactly 15 moves
# We'll add a constraint that all moves are valid (no "null" moves)
# and that we have exactly 15 moves

# Check if solution exists
result = solver.check()

if result == sat:
    print("STATUS: sat")
    model = solver.model()
    
    # Extract moves
    moves = []
    for t in range(1, max_moves + 1):
        disk_val = model[moves_disk[t]]
        from_val = model[moves_from[t]]
        to_val = model[moves_to[t]]
        
        if disk_val is not None and from_val is not None and to_val is not None:
            disk = int(str(disk_val))
            from_peg = peg_names[int(str(from_val))]
            to_peg = peg_names[int(str(to_val))]
            
            moves.append({
                'step': t,
                'disk': disk,
                'from_peg': from_peg,
                'to_peg': to_peg
            })
    
    # Print solution
    print(f"total_moves: {len(moves)}")
    print(f"is_optimal: {len(moves) == 15}")
    print("\nMove sequence:")
    for move in moves:
        print(f"Step {move['step']}: Move disk {move['disk']} from {move['from_peg']} to {move['to_peg']}")
    
    # Verify final state
    print("\nFinal disk positions:")
    for d in range(1, num_disks + 1):
        final_peg = model[disk_peg[d-1][max_moves]]
        print(f"Disk {d} on peg {peg_names[int(str(final_peg))]}")
    
elif result == unsat:
    print("STATUS: unsat")
    print("No solution found with 15 moves. The model might be too constrained.")
else:
    print("STATUS: unknown")