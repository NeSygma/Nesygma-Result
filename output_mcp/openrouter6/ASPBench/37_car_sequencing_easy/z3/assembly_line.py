from z3 import *

# Create solver
solver = Solver()

# Define car types as integers: 0=A, 1=B, 2=C
sequence = [Int(f'seq_{i}') for i in range(6)]

# Add domain constraints for sequence (0, 1, or 2)
for i in range(6):
    solver.add(Or(sequence[i] == 0, sequence[i] == 1, sequence[i] == 2))

# Count constraints for car types
# Type A: 1 car, Type B: 2 cars, Type C: 3 cars
solver.add(Sum([If(sequence[i] == 0, 1, 0) for i in range(6)]) == 1)  # A count
solver.add(Sum([If(sequence[i] == 1, 1, 0) for i in range(6)]) == 2)  # B count  
solver.add(Sum([If(sequence[i] == 2, 1, 0) for i in range(6)]) == 3)  # C count

# Option definitions based on car type:
# Option 1 (sunroof): A has it, C has it, B doesn't
# Option 2 (leather): A has it, B and C don't
# Option 3 (GPS): B has it, A and C don't

# Option 1: at most 2 in any 3 consecutive cars
for start in range(4):  # windows: 0-2, 1-3, 2-4, 3-5
    window_sum = Sum([
        If(Or(sequence[start] == 0, sequence[start] == 2), 1, 0),
        If(Or(sequence[start+1] == 0, sequence[start+1] == 2), 1, 0),
        If(Or(sequence[start+2] == 0, sequence[start+2] == 2), 1, 0)
    ])
    solver.add(window_sum <= 2)

# Option 2: at most 1 in any 2 consecutive cars
for start in range(5):  # windows: 0-1, 1-2, 2-3, 3-4, 4-5
    window_sum = Sum([
        If(sequence[start] == 0, 1, 0),      # A has option 2
        If(sequence[start+1] == 0, 1, 0)     # A has option 2
    ])
    solver.add(window_sum <= 1)

# Option 3: at most 1 in any 2 consecutive cars
for start in range(5):  # windows: 0-1, 1-2, 2-3, 3-4, 4-5
    window_sum = Sum([
        If(sequence[start] == 1, 1, 0),      # B has option 3
        If(sequence[start+1] == 1, 1, 0)     # B has option 3
    ])
    solver.add(window_sum <= 1)

# Check for solution
BENCHMARK_MODE = True
result = solver.check()

if result == sat:
    model = solver.model()
    print("STATUS: sat")
    print("Valid sequence found:")
    
    # Map integers back to car types
    type_map = {0: 'A', 1: 'B', 2: 'C'}
    seq_str = []
    for i in range(6):
        val = model[sequence[i]]
        seq_str.append(type_map[int(str(val))])
    
    print(f"Sequence: {' -> '.join(seq_str)}")
    
    # Verify counts
    a_count = sum(1 for t in seq_str if t == 'A')
    b_count = sum(1 for t in seq_str if t == 'B')
    c_count = sum(1 for t in seq_str if t == 'C')
    print(f"Counts: A={a_count}, B={b_count}, C={c_count}")
    
    # Show options per position
    print("\nOptions per position:")
    for i, car_type in enumerate(seq_str):
        options = []
        if car_type == 'A':
            options = [1, 2]
        elif car_type == 'B':
            options = [3]
        elif car_type == 'C':
            options = [1]
        print(f"Position {i+1}: {car_type} -> Options {options}")
    
    # Verify constraints
    print("\nConstraint verification:")
    
    # Option 1 windows
    print("Option 1 (sunroof) windows:")
    for start in range(4):
        count = sum(1 for i in range(start, start+3) if seq_str[i] in ['A', 'C'])
        print(f"  Positions {start+1}-{start+3}: {count} cars with sunroof (max 2)")
    
    # Option 2 windows
    print("Option 2 (leather) windows:")
    for start in range(5):
        count = sum(1 for i in range(start, start+2) if seq_str[i] == 'A')
        print(f"  Positions {start+1}-{start+2}: {count} cars with leather (max 1)")
    
    # Option 3 windows
    print("Option 3 (GPS) windows:")
    for start in range(5):
        count = sum(1 for i in range(start, start+2) if seq_str[i] == 'B')
        print(f"  Positions {start+1}-{start+2}: {count} cars with GPS (max 1)")
    
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")