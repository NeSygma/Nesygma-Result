from z3 import *

def solve_hanoi_with_journey():
    # Peg mapping: 0=A, 1=B, 2=C, 3=D
    peg_names = ['A', 'B', 'C', 'D']
    
    # Try different move counts starting from 19 (expected optimal)
    for T in range(19, 31):
        print(f"Trying T = {T}...")
        
        solver = Solver()
        
        # Define variables
        # loc[d][t] = peg of disk d at time t (d: 0-3 for disks 1-4, t: 0-T)
        loc = [[Int(f"loc_{d}_{t}") for t in range(T+1)] for d in range(4)]
        
        # Move variables for each step i (1-indexed)
        disk_move = [Int(f"disk_{i}") for i in range(1, T+1)]
        from_peg = [Int(f"from_{i}") for i in range(1, T+1)]
        to_peg = [Int(f"to_{i}") for i in range(1, T+1)]
        
        # Initial state: all disks on peg A (0)
        for d in range(4):
            solver.add(loc[d][0] == 0)
        
        # Goal state: all disks on peg D (3)
        for d in range(4):
            solver.add(loc[d][T] == 3)
        
        # Domain constraints for move variables
        for i in range(1, T+1):
            solver.add(disk_move[i-1] >= 1, disk_move[i-1] <= 4)  # disk 1-4
            solver.add(from_peg[i-1] >= 0, from_peg[i-1] <= 3)    # peg 0-3
            solver.add(to_peg[i-1] >= 0, to_peg[i-1] <= 3)        # peg 0-3
            solver.add(from_peg[i-1] != to_peg[i-1])              # cannot stay on same peg
        
        # State transitions and move validity
        for i in range(1, T+1):
            d = disk_move[i-1]
            f = from_peg[i-1]
            t = to_peg[i-1]
            
            # Disk must be on source peg at time i-1
            for disk_idx in range(4):
                solver.add(Implies(d == disk_idx + 1, loc[disk_idx][i-1] == f))
            
            # Disk moves to destination peg at time i
            for disk_idx in range(4):
                solver.add(Implies(d == disk_idx + 1, loc[disk_idx][i] == t))
            
            # Other disks stay in place
            for other_idx in range(4):
                other_disk = other_idx + 1
                solver.add(Implies(d != other_disk, loc[other_idx][i] == loc[other_idx][i-1]))
            
            # Move validity: disk must be top on source peg
            # No larger disk can be on the same source peg at time i-1
            for other_idx in range(4):
                other_disk = other_idx + 1
                solver.add(Implies(And(d != other_disk, loc[other_idx][i-1] == f),
                                  other_disk > d))
            
            # Move validity: disk must be smaller than all disks on destination peg
            for other_idx in range(4):
                other_disk = other_idx + 1
                solver.add(Implies(And(d != other_disk, loc[other_idx][i-1] == t),
                                  other_disk > d))
        
        # Journey constraints: each disk must visit B (peg 1) and C (peg 2)
        for d in range(1, 5):
            # Must visit B at least once
            visit_b = Or([And(disk_move[i-1] == d, to_peg[i-1] == 1) for i in range(1, T+1)])
            solver.add(visit_b)
            
            # Must visit C at least once
            visit_c = Or([And(disk_move[i-1] == d, to_peg[i-1] == 2) for i in range(1, T+1)])
            solver.add(visit_c)
        
        # Check satisfiability
        result = solver.check()
        
        if result == sat:
            print(f"STATUS: sat")
            print(f"Solution found with {T} moves (expected optimal: 19)")
            
            model = solver.model()
            
            # Extract and print moves
            moves = []
            for i in range(1, T+1):
                step = i
                disk = model[disk_move[i-1]].as_long()
                from_p = model[from_peg[i-1]].as_long()
                to_p = model[to_peg[i-1]].as_long()
                moves.append({
                    'step': step,
                    'disk': disk,
                    'from_peg': peg_names[from_p],
                    'to_peg': peg_names[to_p]
                })
            
            # Print moves in required format
            print("moves: [")
            for move in moves:
                print(f"  {{step: {move['step']}, disk: {move['disk']}, from_peg: '{move['from_peg']}', to_peg: '{move['to_peg']}'}},")
            print("]")
            print(f"total_moves: {T}")
            
            # Verify journey constraints
            print("\nVerifying journey constraints:")
            for d in range(1, 5):
                visited_b = any(m['disk'] == d and m['to_peg'] == 'B' for m in moves)
                visited_c = any(m['disk'] == d and m['to_peg'] == 'C' for m in moves)
                print(f"  Disk {d}: visited B = {visited_b}, visited C = {visited_c}")
            
            return True
        
        elif result == unsat:
            print(f"STATUS: unsat for T = {T}")
        else:
            print(f"STATUS: unknown for T = {T}")
    
    print("No solution found within 30 moves")
    return False

# Run the solver
if __name__ == "__main__":
    solve_hanoi_with_journey()