from z3 import *

# Problem parameters
N_DISKS = 4
A, B, C, D = 0, 1, 2, 3
TOTAL_MOVES = 19  # Expected optimal

solver = Solver()
solver.set("timeout", 300000)  # 5 min timeout

# Decision variables
# peg[d][t] = which peg (0=A,1=B,2=C,3=D) disk d occupies at time step t
peg = [[Int(f'p{d}_{t}') for t in range(TOTAL_MOVES + 1)] for d in range(N_DISKS)]
# moved[d][t] = True iff disk d is the one moved at step t
moved = [[Bool(f'm{d}_{t}') for t in range(TOTAL_MOVES)] for d in range(N_DISKS)]

# === INITIAL STATE: all disks on peg A ===
for d in range(N_DISKS):
    solver.add(peg[d][0] == A)

# === VALID PEG DOMAIN ===
for d in range(N_DISKS):
    for t in range(TOTAL_MOVES + 1):
        solver.add(And(peg[d][t] >= 0, peg[d][t] <= 3))

# === EXACTLY ONE DISK MOVED PER STEP ===
for t in range(TOTAL_MOVES):
    solver.add(Sum([If(moved[d][t], 1, 0) for d in range(N_DISKS)]) == 1)

# === MOVEMENT EFFECTS ===
for d in range(N_DISKS):
    for t in range(TOTAL_MOVES):
        # If disk d is moved, its peg must change
        solver.add(Implies(moved[d][t], peg[d][t+1] != peg[d][t]))
        # If disk d is NOT moved, its peg stays the same
        solver.add(Implies(Not(moved[d][t]), peg[d][t+1] == peg[d][t]))

# === TOP DISK CONSTRAINT ===
# Only the smallest disk on a peg can be moved (no smaller disk on same peg)
for d in range(N_DISKS):
    for t in range(TOTAL_MOVES):
        for s in range(d):  # s < d means s is a smaller disk
            solver.add(Implies(moved[d][t], peg[s][t] != peg[d][t]))

# === DESTINATION CONSTRAINT ===
# Cannot place disk d on a peg that has a smaller disk
for d in range(N_DISKS):
    for t in range(TOTAL_MOVES):
        for s in range(d):
            solver.add(Implies(moved[d][t], peg[s][t] != peg[d][t+1]))

# === GOAL STATE: all disks on peg D at final time step ===
for d in range(N_DISKS):
    solver.add(peg[d][TOTAL_MOVES] == D)

# === PILGRIM'S JOURNEY ===
# Every disk must land on peg B at least once AND peg C at least once
for d in range(N_DISKS):
    # Must land on B
    solver.add(Or([And(moved[d][t], peg[d][t+1] == B) for t in range(TOTAL_MOVES)]))
    # Must land on C
    solver.add(Or([And(moved[d][t], peg[d][t+1] == C) for t in range(TOTAL_MOVES)]))

# === SOLVE ===
result = solver.check()

if result == sat:
    m = solver.model()
    print("STATUS: sat")
    print(f"total_moves: {TOTAL_MOVES}")
    
    peg_names = ['A', 'B', 'C', 'D']
    moves_list = []
    for t in range(TOTAL_MOVES):
        for d in range(N_DISKS):
            if is_true(m.evaluate(moved[d][t], model_completion=True)):
                fp = int(str(m.evaluate(peg[d][t], model_completion=True)))
                tp = int(str(m.evaluate(peg[d][t+1], model_completion=True)))
                moves_list.append((t+1, d+1, peg_names[fp], peg_names[tp]))
                break
    
    print("\nMove sequence:")
    for step, disk, fr, to in moves_list:
        print(f"  Step {step:2d}: Disk {disk} from {fr} to {to}")
    
    # === VERIFICATION ===
    print("\n--- Verification ---")
    
    # Check initial state
    init_ok = all(int(str(m.evaluate(peg[d][0], model_completion=True))) == A for d in range(N_DISKS))
    print(f"  Initial state (all on A): {'OK' if init_ok else 'FAIL'}")
    
    # Check goal state
    goal_ok = all(int(str(m.evaluate(peg[d][TOTAL_MOVES], model_completion=True))) == D for d in range(N_DISKS))
    print(f"  Goal state (all on D): {'OK' if goal_ok else 'FAIL'}")
    
    # Check pilgrim constraint
    all_pilgrim_ok = True
    for d in range(N_DISKS):
        visited_pegs = set()
        for step, disk, fr, to in moves_list:
            t = step - 1
            if is_true(m.evaluate(moved[d][t], model_completion=True)):
                to_p = int(str(m.evaluate(peg[d][t+1], model_completion=True)))
                visited_pegs.add(peg_names[to_p])
        ok = 'B' in visited_pegs and 'C' in visited_pegs
        if not ok:
            all_pilgrim_ok = False
        print(f"  Disk {d+1} pilgrim (B,C): visited {sorted(visited_pegs)} {'OK' if ok else 'FAIL'}")
    
    # Check move legality
    all_moves_ok = True
    for step, disk, fr, to in moves_list:
        t = step - 1
        d = disk - 1
        # Check top disk
        for s in range(d):
            s_peg = int(str(m.evaluate(peg[s][t], model_completion=True)))
            d_peg = int(str(m.evaluate(peg[d][t], model_completion=True)))
            if s_peg == d_peg:
                all_moves_ok = False
                print(f"  FAIL: Step {step} - disk {disk} not on top (smaller disk {s+1} on same peg)")
        # Check destination
        dest = int(str(m.evaluate(peg[d][t+1], model_completion=True)))
        for s in range(d):
            s_peg = int(str(m.evaluate(peg[s][t], model_completion=True)))
            if s_peg == dest:
                all_moves_ok = False
                print(f"  FAIL: Step {step} - destination peg has smaller disk {s+1}")
    print(f"  All moves legal: {'OK' if all_moves_ok else 'FAIL'}")
    
    # === JSON OUTPUT ===
    print("\n--- JSON Output ---")
    print('{')
    print(f'  "total_moves": {TOTAL_MOVES},')
    print('  "moves": [')
    for i, (step, disk, fr, to) in enumerate(moves_list):
        c = ',' if i < len(moves_list) - 1 else ''
        print(f'    {{"step": {step}, "disk": {disk}, "from_peg": "{fr}", "to_peg": "{to}"}}{c}')
    print('  ]')
    print('}')

elif result == unsat:
    print("STATUS: unsat")
    print(f"No solution found with {TOTAL_MOVES} moves")
else:
    print("STATUS: unknown")
    print(f"Solver returned: {result}")