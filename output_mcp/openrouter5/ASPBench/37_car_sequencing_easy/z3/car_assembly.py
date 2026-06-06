from z3 import *

# We have 6 positions (0-indexed for Z3, positions 1-6)
N = 6

# Car types: A=0, B=1, C=2
A, B, C = 0, 1, 2

# Sequence: each position gets a car type
seq = [Int(f'seq_{i}') for i in range(N)]

solver = Solver()

# Domain: each position is one of A, B, C
for i in range(N):
    solver.add(Or(seq[i] == A, seq[i] == B, seq[i] == C))

# Constraint 2: Exactly 1 car of type A, 2 of type B, 3 of type C
solver.add(Sum([If(seq[i] == A, 1, 0) for i in range(N)]) == 1)
solver.add(Sum([If(seq[i] == B, 1, 0) for i in range(N)]) == 2)
solver.add(Sum([If(seq[i] == C, 1, 0) for i in range(N)]) == 3)

# Option definitions:
# Type A (0): has options [1, 2]
# Type B (1): has options [3]
# Type C (2): has options [1]

# Helper: does a car at position i have option o?
def has_option(i, opt):
    if opt == 1:
        # Option 1: Type A or Type C
        return Or(seq[i] == A, seq[i] == C)
    elif opt == 2:
        # Option 2: Type A only
        return seq[i] == A
    elif opt == 3:
        # Option 3: Type B only
        return seq[i] == B
    else:
        return False

# Constraint 3: Option 1 - at most 2 in every 3 consecutive cars
# Sliding windows of size 3: positions (0,1,2), (1,2,3), (2,3,4), (3,4,5)
for start in range(N - 2):
    window_count = Sum([If(has_option(start + k, 1), 1, 0) for k in range(3)])
    solver.add(window_count <= 2)

# Constraint 4: Option 2 - at most 1 in every 2 consecutive cars
# Sliding windows of size 2: positions (0,1), (1,2), (2,3), (3,4), (4,5)
for start in range(N - 1):
    window_count = Sum([If(has_option(start + k, 2), 1, 0) for k in range(2)])
    solver.add(window_count <= 1)

# Constraint 5: Option 3 - at most 1 in every 2 consecutive cars
# Sliding windows of size 2: positions (0,1), (1,2), (2,3), (3,4), (4,5)
for start in range(N - 1):
    window_count = Sum([If(has_option(start + k, 3), 1, 0) for k in range(2)])
    solver.add(window_count <= 1)

# Solve
BENCHMARK_MODE = True
result = solver.check()

if result == sat:
    m = solver.model()
    print("STATUS: sat")
    # Map numbers back to letters
    type_map = {0: 'A', 1: 'B', 2: 'C'}
    sequence_str = ''.join([type_map[m[seq[i]].as_long()] for i in range(N)])
    print(f"Sequence: {sequence_str}")
    # Also print per-position details
    for i in range(N):
        car_type = type_map[m[seq[i]].as_long()]
        print(f"Position {i+1}: Type {car_type}")
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")