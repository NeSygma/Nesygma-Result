from z3 import *

# Solver configuration
BENCHMARK_MODE = True

# Number of positions
N = 12

# Car type mapping: 0=A, 1=B, 2=C, 3=D
pos_type = [Int(f'pos_{i}') for i in range(N)]

solver = Solver()

# Domain constraints: each position must have a car type 0..3
for i in range(N):
    solver.add(And(pos_type[i] >= 0, pos_type[i] <= 3))

# Count constraints
solver.add(Sum([If(pos_type[i] == 0, 1, 0) for i in range(N)]) == 3)  # A
solver.add(Sum([If(pos_type[i] == 1, 1, 0) for i in range(N)]) == 3)  # B
solver.add(Sum([If(pos_type[i] == 2, 1, 0) for i in range(N)]) == 4)  # C
solver.add(Sum([If(pos_type[i] == 3, 1, 0) for i in range(N)]) == 2)  # D

# Positional ban: no B (type 1) at positions 1 or 12 (indices 0 and 11)
solver.add(pos_type[0] != 1)
solver.add(pos_type[11] != 1)

# Equipment cooldown: C (type 2) must have at least 2-slot gap
for i in range(N-1):
    solver.add(Or(pos_type[i] != 2, pos_type[i+1] != 2))
for i in range(N-2):
    solver.add(Or(pos_type[i] != 2, pos_type[i+2] != 2))

# Standard capacity: at most 2 sunroofs (A or D) in any window of 4 consecutive positions
for start in range(N-3):
    window = [pos_type[start + k] for k in range(4)]
    count_sunroof = Sum([If(Or(w == 0, w == 3), 1, 0) for w in window])
    solver.add(count_sunroof <= 2)

# Conditional capacity for option3 (B)
for p in range(N):
    # Determine window end
    end = min(N-1, p + 3)
    window = [pos_type[k] for k in range(p, end+1)]
    count_B = Sum([If(w == 1, 1, 0) for w in window])
    if p == 0:
        # No preceding car, treat as not preceded by EV
        solver.add(count_B <= 2)
    else:
        # If preceding car is B (EV), at most 1 B in window
        solver.add(Implies(pos_type[p-1] == 1, count_B <= 1))
        # Otherwise, at most 2 B in window
        solver.add(Implies(pos_type[p-1] != 1, count_B <= 2))

# Solve
result = solver.check()

if result == sat:
    m = solver.model()
    # Mapping from type int to string and options list
    type_map = {0: 'A', 1: 'B', 2: 'C', 3: 'D'}
    options_map = {0: [1], 1: [3, 4], 2: [2], 3: [5]}
    seq = []
    for i in range(N):
        t = m[pos_type[i]].as_long()
        seq.append((i+1, type_map[t], options_map[t]))
    # Print results
    print("STATUS: sat")
    print("solution_found: True")
    print("sequence = [" + ", ".join(f"({p},'{ct}',{opts})" for p,ct,opts in seq) + "]")
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")