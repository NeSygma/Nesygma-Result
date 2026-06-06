from z3 import *

solver = Solver()

N = 12
# Car types: 0=A, 1=B, 2=C, 3=D
car = [Int(f'car_{i}') for i in range(N)]

# Domain: each car is 0..3
for i in range(N):
    solver.add(car[i] >= 0, car[i] <= 3)

# Constraint 1: Exact counts
solver.add(Sum([If(car[i] == 0, 1, 0) for i in range(N)]) == 3)  # A: 3
solver.add(Sum([If(car[i] == 1, 1, 0) for i in range(N)]) == 3)  # B: 3
solver.add(Sum([If(car[i] == 2, 1, 0) for i in range(N)]) == 4)  # C: 4
solver.add(Sum([If(car[i] == 3, 1, 0) for i in range(N)]) == 2)  # D: 2

# Constraint 2: Hierarchical Options
# Option 5 (Panoramic Sunroof, Type D) implies Option 1 (Standard Sunroof)
# This means for constraint purposes, Type D counts as having Option 1 too.
# We'll use "effective Option 1" = Type A OR Type D throughout.

# Constraint 3: Positional Ban - No Option 4 (EV Powertrain = Type B) at position 1 or 12
# Positions are 1-indexed in problem, 0-indexed in array
solver.add(car[0] != 1)   # position 1
solver.add(car[11] != 1)  # position 12

# Constraint 4: Equipment Cooldown - Option 2 (Custom Paint = Type C)
# At least 2-slot gap between any two Type C cars
# |pos_i - pos_j| >= 3 for any two distinct C cars
# Equivalently: no two C's at distance 1 or 2
for i in range(N):
    for j in range(i+1, N):
        if j - i <= 2:
            solver.add(Not(And(car[i] == 2, car[j] == 2)))

# Constraint 5: Standard Capacity - At most 2 cars with effective Option 1
# (Type A or Type D) in any window of 4 consecutive positions
for start in range(N - 3):  # windows: [0..3], [1..4], ..., [8..11]
    window = [car[start + k] for k in range(4)]
    solver.add(Sum([If(Or(window[k] == 0, window[k] == 3), 1, 0) for k in range(4)]) <= 2)

# Constraint 6: Conditional Capacity for Option 3 (Sport Package = Type B)
# For each position P (1-indexed, P from 1 to 12):
#   If P is preceded by a car with Option 4 (Type B), i.e., car at P-1 is Type B,
#     then at most 1 Type B in window [P, P+3] (1-indexed)
#   Otherwise, at most 2 Type B in window [P, P+3]
# Window [P, P+3] in 1-indexed = positions P, P+1, P+2, P+3
# In 0-indexed: indices P-1, P, P+1, P+2

for P in range(1, N + 1):  # P is 1-indexed, from 1 to 12
    # Window indices (0-indexed): P-1, P, P+1, P+2
    # Only include indices that are valid (0..11)
    window_indices = [P - 1 + k for k in range(4) if P - 1 + k < N]
    
    if len(window_indices) == 0:
        continue
    
    count_b_in_window = Sum([If(car[idx] == 1, 1, 0) for idx in window_indices])
    
    if P == 1:
        # No preceding position, so "otherwise" case: at most 2
        solver.add(count_b_in_window <= 2)
    else:
        # Preceding position is P-1 (1-indexed) = index P-2 (0-indexed)
        preceding_is_ev = (car[P - 2] == 1)  # Type B has Option 4
        solver.add(Implies(preceding_is_ev, count_b_in_window <= 1))
        solver.add(Implies(Not(preceding_is_ev), count_b_in_window <= 2))

# Solve
BENCHMARK_MODE = True
result = solver.check()

if result == sat:
    m = solver.model()
    print("STATUS: sat")
    
    type_names = {0: "A", 1: "B", 2: "C", 3: "D"}
    type_options = {0: [1], 1: [3, 4], 2: [2], 3: [5]}
    
    print("solution_found: True")
    print("sequence:")
    for i in range(N):
        ct = m[car[i]].as_long()
        cname = type_names[ct]
        opts = type_options[ct]
        print(f"  position: {i+1}, car_type: \"{cname}\", options: {opts}")
    
    # Verify constraints for debugging
    seq = [m[car[i]].as_long() for i in range(N)]
    print("\n--- Verification ---")
    print(f"Counts: A={seq.count(0)}, B={seq.count(1)}, C={seq.count(2)}, D={seq.count(3)}")
    print(f"Position 1: {type_names[seq[0]]}, Position 12: {type_names[seq[11]]}")
    
    # Check cooldown
    c_positions = [i for i in range(N) if seq[i] == 2]
    min_gap = min([c_positions[j+1]-c_positions[j] for j in range(len(c_positions)-1)]) if len(c_positions) > 1 else 999
    print(f"C positions: {[p+1 for p in c_positions]}, min gap: {min_gap}")
    
    # Check sunroof windows
    for start in range(N - 3):
        sunroof_count = sum(1 for k in range(4) if seq[start+k] in [0, 3])
        if sunroof_count > 2:
            print(f"WARNING: Sunroof window [{start+1}..{start+4}] has {sunroof_count}")
    
    # Check conditional B capacity
    for P in range(1, N+1):
        w_indices = [P-1+k for k in range(4) if P-1+k < N]
        b_count = sum(1 for idx in w_indices if seq[idx] == 1)
        if P > 1 and seq[P-2] == 1:  # preceded by EV
            if b_count > 1:
                print(f"WARNING: Conditional B window at P={P} has {b_count} B's (preceded by B)")
        else:
            if b_count > 2:
                print(f"WARNING: B window at P={P} has {b_count} B's")
    
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")