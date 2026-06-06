from z3 import *

solver = Solver()

N = 6  # number of cars

# Car types: 0=A, 1=B, 2=C
seq = [Int(f'seq_{i}') for i in range(N)]

# Domain: each position is 0 (A), 1 (B), or 2 (C)
for i in range(N):
    solver.add(Or(seq[i] == 0, seq[i] == 1, seq[i] == 2))

# Exactly 1 A, 2 B, 3 C
solver.add(Sum([If(seq[i] == 0, 1, 0) for i in range(N)]) == 1)
solver.add(Sum([If(seq[i] == 1, 1, 0) for i in range(N)]) == 2)
solver.add(Sum([If(seq[i] == 2, 1, 0) for i in range(N)]) == 3)

# Option presence per position:
# Option 1 (sunroof): A has it, C has it => seq[i] == 0 or seq[i] == 2
# Option 2 (leather): A has it => seq[i] == 0
# Option 3 (GPS): B has it => seq[i] == 1

has_opt1 = [Or(seq[i] == 0, seq[i] == 2) for i in range(N)]
has_opt2 = [seq[i] == 0 for i in range(N)]
has_opt3 = [seq[i] == 1 for i in range(N)]

# Constraint 3: Option 1 - at most 2 in every 3 consecutive cars
for i in range(N - 2):  # windows: [0,1,2], [1,2,3], [2,3,4], [3,4,5]
    solver.add(
        Sum([If(has_opt1[i+j], 1, 0) for j in range(3)]) <= 2
    )

# Constraint 4: Option 2 - at most 1 in every 2 consecutive cars
for i in range(N - 1):  # windows: [0,1], [1,2], [2,3], [3,4], [4,5]
    solver.add(
        Sum([If(has_opt2[i+j], 1, 0) for j in range(2)]) <= 1
    )

# Constraint 5: Option 3 - at most 1 in every 2 consecutive cars
for i in range(N - 1):
    solver.add(
        Sum([If(has_opt3[i+j], 1, 0) for j in range(2)]) <= 1
    )

BENCHMARK_MODE = True
result = solver.check()

if result == sat:
    m = solver.model()
    print("STATUS: sat")
    type_names = {0: 'A', 1: 'B', 2: 'C'}
    sequence = [type_names[m[seq[i]].as_long()] for i in range(N)]
    print(f"sequence = {sequence}")
    print(f"length = {N}")
    
    # Verify constraints explicitly
    print("\nVerification:")
    print(f"  Type counts: A={sequence.count('A')}, B={sequence.count('B')}, C={sequence.count('C')}")
    
    # Option 1 windows
    for i in range(N - 2):
        window = sequence[i:i+3]
        opt1_count = sum(1 for c in window if c in ['A', 'C'])
        print(f"  Window [{i+1}-{i+3}] {window}: option1 count = {opt1_count} (max 2)")
    
    # Option 2 windows
    for i in range(N - 1):
        window = sequence[i:i+2]
        opt2_count = sum(1 for c in window if c == 'A')
        print(f"  Window [{i+1}-{i+2}] {window}: option2 count = {opt2_count} (max 1)")
    
    # Option 3 windows
    for i in range(N - 1):
        window = sequence[i:i+2]
        opt3_count = sum(1 for c in window if c == 'B')
        print(f"  Window [{i+1}-{i+2}] {window}: option3 count = {opt3_count} (max 1)")

elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")