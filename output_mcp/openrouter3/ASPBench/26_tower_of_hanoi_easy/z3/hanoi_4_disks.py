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
    # For the moved disk, check it's on the source peg at previous time
    moved_disk = moves_disk[t]
    source_peg = moves_from[t]
    
    # The moved disk must be on the source peg at time t-1
    for d in range(1, num_disks + 1):
        solver.add(
            If(moved_disk == d,
               disk_peg[d-1][t-1] == source_peg,
               True)  # No constraint for other disks
        )
    
    # Check that no smaller disk is on top of the moved disk at the source peg
    # For each smaller disk (disk < moved_disk), it cannot be on the same peg
    # unless it's already been moved away
    for smaller in range(1, num_disks + 1):
        solver.add(
            Implies(
                And(moved_disk > smaller, disk_peg[smaller-1][t-1] == source_peg),
                False  # This would mean smaller disk is on top - invalid
            )
        )

# Constraint: Larger disk cannot be placed on smaller disk
# For each time step, check the ordering on each peg
for t in range(max_moves + 1):
    for peg in range(num_pegs):
        # For each pair of disks (d1, d2) where d1 > d2 (d1 is larger)
        # If both are on the same peg at time t, then d2 must be above d1
        # This means d2 must have been moved more recently than d1
        # We'll enforce this by checking that if both are on same peg,
        # then the larger disk cannot be placed after the smaller one
        for d1 in range(1, num_disks + 1):
            for d2 in range(1, num_disks + 1):
                if d1 > d2:  # d1 is larger than d2
                    # If both on same peg at time t, then d2 must be above d1
                    # This is complex to model directly, so we'll use a simpler approach:
                    # At any time, for any peg, the disks on that peg must be in decreasing order
                    # We'll track the "top" disk on each peg at each time
                    pass

# Alternative approach: Track the top disk on each peg at each time
# top_disk[peg][t] = the smallest disk on peg at time t (or 0 if empty)
top_disk = [[Int(f'top_{peg}_time_{t}') for t in range(max_moves + 1)] for peg in range(num_pegs)]

# Initialize top_disk at time 0
# Peg A has disks 4,3,2,1 (bottom to top), so top is disk 1
solver.add(top_disk[0][0] == 1)  # Peg A top is disk 1
solver.add(top_disk[1][0] == 0)  # Peg B empty
solver.add(top_disk[2][0] == 0)  # Peg C empty

# Update top_disk based on moves
for t in range(1, max_moves + 1):
    moved_disk = moves_disk[t]
    from_peg = moves_from[t]
    to_peg = moves_to[t]
    
    # For source peg: top becomes the next smallest disk on that peg
    # We need to find the next disk on the source peg after moving moved_disk
    # This is complex, so we'll use a different approach
    
    # For destination peg: top becomes the moved disk (since it's smaller than any existing)
    # Actually, we need to ensure moved_disk is smaller than current top
    solver.add(top_disk[to_peg][t] == moved_disk)
    
    # For source peg: top becomes the next disk (if any)
    # We'll handle this by checking all disks

# Simpler approach: Use explicit ordering constraints
# For each time step, ensure that on each peg, disks are in correct order
for t in range(max_moves + 1):
    for peg in range(num_pegs):
        # Get all disks on this peg at time t
        disks_on_peg = [d for d in range(1, num_disks + 1) if d <= num_disks]
        
        # For each pair (d1, d2) where d1 > d2 (d1 larger)
        # If both on same peg, then d2 must be "above" d1
        # We'll enforce this by ensuring that if d1 is on peg, then d2 cannot be on peg
        # unless d2 was moved more recently (which we track via time)
        
        # Actually, let's use a simpler constraint:
        # At any time, for any peg, if disk d1 > d2 and both are on the peg,
        # then d2 must have been moved to this peg after d1
        # We'll track the last move time for each disk on each peg
        
        # This is getting complex. Let's try a different approach:
        # Use the fact that in Tower of Hanoi, the solution is recursive
        # We'll just enforce the basic rules and let Z3 find the solution

# Let's simplify: Just enforce that no larger disk is on top of a smaller one
# by checking that at any time, for any peg, the disks on that peg are in decreasing order
# We'll use a "stack" representation: for each peg and time, track the sequence of disks
# But this is complex in Z3

# Alternative: Use the classic Tower of Hanoi constraints
# 1. Only one disk moves per step
# 2. Disk can only move to a peg where it's smaller than the top disk (or peg is empty)
# 3. Initial and final states as given

# Let's implement the classic constraints more directly
for t in range(1, max_moves + 1):
    moved_disk = moves_disk[t]
    from_peg = moves_from[t]
    to_peg = moves_to[t]
    
    # Constraint: moved_disk must be on from_peg at time t-1
    for d in range(1, num_disks + 1):
        solver.add(
            Implies(moved_disk == d, disk_peg[d-1][t-1] == from_peg)
        )
    
    # Constraint: moved_disk must be smaller than top disk on to_peg at time t-1
    # or to_peg must be empty
    # We'll check all smaller disks: if any smaller disk is on to_peg at t-1,
    # then moved_disk cannot be larger than it
    for smaller in range(1, moved_disk):
        solver.add(
            Implies(disk_peg[smaller-1][t-1] == to_peg, False)  # This would mean smaller disk is on to_peg
        )
    
    # Actually, the constraint is: moved_disk must be smaller than ALL disks on to_peg
    # So for any disk d on to_peg at t-1, we must have moved_disk < d
    for d in range(1, num_disks + 1):
        solver.add(
            Implies(
                And(disk_peg[d-1][t-1] == to_peg, d != moved_disk),
                moved_disk < d
            )
        )

# Add constraint that we use exactly 15 moves
# We'll add a constraint that all moves are valid (no "null" moves)
# and that we have exactly 15 moves

# For simplicity, let's just check if a solution exists with 15 moves
# and print the moves

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
    print("No solution found with 15 moves. Trying with more moves...")
else:
    print("STATUS: unknown")