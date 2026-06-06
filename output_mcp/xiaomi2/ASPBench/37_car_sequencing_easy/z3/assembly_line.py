from z3 import *

solver = Solver()

# 6 positions in the assembly line
N = 6
# Car types: 0=A, 1=B, 2=C
seq = [Int(f'seq_{i}') for i in range(N)]

# Domain: each position is 0 (A), 1 (B), or 2 (C)
for i in range(N):
    solver.add(Or(seq[i] == 0, seq[i] == 1, seq[i] == 2))

# Count constraints: 1×A, 2×B, 3×C
solver.add(Sum([If(seq[i] == 0, 1, 0) for i in range(N)]) == 1)
solver.add(Sum([If(seq[i] == 1, 1, 0) for i in range(N)]) == 2)
solver.add(Sum([If(seq[i] == 2, 1, 0) for i in range(N)]) == 3)

# Option presence at each position:
# Option 1 (sunroof): present in type A (0) and type C (2)
# Option 2 (leather): present in type A (0) only
# Option 3 (GPS): present in type B (1) only

opt1 = [If(Or(seq[i] == 0, seq[i] == 2), 1, 0) for i in range(N)]
opt2 = [If(seq[i] == 0, 1, 0) for i in range(N)]
opt3 = [If(seq[i] == 1, 1, 0) for i in range(N)]

# Constraint 3: No sliding window of 3 consecutive cars has more than 2 with option 1
for i in range(N - 2):
    solver.add(opt1[i] + opt1[i+1] + opt1[i+2] <= 2)

# Constraint 4: No sliding window of 2 consecutive cars has more than 1 with option 2
for i in range(N - 1):
    solver.add(opt2[i] + opt2[i+1] <= 1)

# Constraint 5: No sliding window of 2 consecutive cars has more than 1 with option 3
for i in range(N - 1):
    solver.add(opt3[i] + opt3[i+1] <= 1)

BENCHMARK_MODE = True
result = solver.check()

if result == sat:
    m = solver.model()
    print("STATUS: sat")
    type_names = {0: 'A', 1: 'B', 2: 'C'}
    sequence = [type_names[m[seq[i]].as_long()] for i in range(N)]
    print(f"sequence = {sequence}")
    for i in range(N):
        print(f"Position {i+1}: Type {sequence[i]}")
    # Verify constraints
    print("\nVerification:")
    print(f"  Count A: {sequence.count('A')} (need 1)")
    print(f"  Count B: {sequence.count('B')} (need 2)")
    print(f"  Count C: {sequence.count('C')} (need 3)")
    # Option 1 windows
    opt1_map = {'A': 1, 'B': 0, 'C': 1}
    opt2_map = {'A': 1, 'B': 0, 'C': 0}
    opt3_map = {'A': 0, 'B': 1, 'C': 0}
    for i in range(N - 2):
        s = sum(opt1_map[sequence[j]] for j in range(i, i+3))
        print(f"  Window [{i+1}-{i+3}] opt1 count: {s} (max 2)")
    for i in range(N - 1):
        s2 = sum(opt2_map[sequence[j]] for j in range(i, i+2))
        s3 = sum(opt3_map[sequence[j]] for j in range(i, i+2))
        print(f"  Window [{i+1}-{i+2}] opt2 count: {s2} (max 1), opt3 count: {s3} (max 1)")
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")