from z3 import *

solver = Solver()

# Constants for car types
A, B, C = 0, 1, 2

# Number of cars
N = 6

# Decision variables: sequence[i] is the car type at position i (0-indexed)
sequence = [Int(f'seq_{i}') for i in range(N)]

# Domain constraints: each position is A, B, or C
for i in range(N):
    solver.add(sequence[i] >= A, sequence[i] <= C)

# Car type count constraints
# Type A: exactly 1 car
solver.add(Sum([If(sequence[i] == A, 1, 0) for i in range(N)]) == 1)
# Type B: exactly 2 cars
solver.add(Sum([If(sequence[i] == B, 1, 0) for i in range(N)]) == 2)
# Type C: exactly 3 cars
solver.add(Sum([If(sequence[i] == C, 1, 0) for i in range(N)]) == 3)

# Define which options each car type has
# Type A (0): has options [1, 2]
# Type B (1): has options [3]
# Type C (2): has options [1]

# Option presence for each position
has_option1 = [Bool(f'opt1_{i}') for i in range(N)]
has_option2 = [Bool(f'opt2_{i}') for i in range(N)]
has_option3 = [Bool(f'opt3_{i}') for i in range(N)]

for i in range(N):
    # Option 1: Type A or Type C has option 1
    solver.add(has_option1[i] == Or(sequence[i] == A, sequence[i] == C))
    # Option 2: Only Type A has option 2
    solver.add(has_option2[i] == (sequence[i] == A))
    # Option 3: Only Type B has option 3
    solver.add(has_option3[i] == (sequence[i] == B))

# Sliding window constraints

# Option 1: at most 2 in every 3 consecutive cars
for start in range(N - 2):  # windows of size 3: positions start, start+1, start+2
    window_sum = Sum([If(has_option1[start + k], 1, 0) for k in range(3)])
    solver.add(window_sum <= 2)

# Option 2: at most 1 in every 2 consecutive cars
for start in range(N - 1):  # windows of size 2: positions start, start+1
    window_sum = Sum([If(has_option2[start + k], 1, 0) for k in range(2)])
    solver.add(window_sum <= 1)

# Option 3: at most 1 in every 2 consecutive cars
for start in range(N - 1):  # windows of size 2: positions start, start+1
    window_sum = Sum([If(has_option3[start + k], 1, 0) for k in range(2)])
    solver.add(window_sum <= 1)

BENCHMARK_MODE = True
result = solver.check()

if result == sat:
    m = solver.model()
    print("STATUS: sat")
    # Map to car type letters
    type_names = {0: 'A', 1: 'B', 2: 'C'}
    seq_str = ''
    for i in range(N):
        val = m[sequence[i]].as_long()
        seq_str += type_names[val]
    print(f"Sequence: {seq_str}")
    # Also show the options breakdown
    print("\nPosition-by-position:")
    for i in range(N):
        val = m[sequence[i]].as_long()
        opt1 = "yes" if is_true(m[has_option1[i]]) else "no"
        opt2 = "yes" if is_true(m[has_option2[i]]) else "no"
        opt3 = "yes" if is_true(m[has_option3[i]]) else "no"
        print(f"  Pos {i+1}: Type {type_names[val]} (opt1={opt1}, opt2={opt2}, opt3={opt3})")
    
    # Verify counts
    print(f"\nCounts - A: {sum(1 for i in range(N) if is_true(m[sequence[i]] == A))}, "
          f"B: {sum(1 for i in range(N) if is_true(m[sequence[i]] == B))}, "
          f"C: {sum(1 for i in range(N) if is_true(m[sequence[i]] == C))}")
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")