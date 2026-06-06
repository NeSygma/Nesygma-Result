from z3 import *

# BENCHMARK_MODE: ON (model-finding mode)
BENCHMARK_MODE = True

# Total positions
N = 12

# Car types and counts
car_types = ["A", "B", "C", "D"]
car_counts = {"A": 3, "B": 3, "C": 4, "D": 2}

# Options (0-indexed for Z3)
# Option 1: Standard Sunroof -> index 0
# Option 2: Custom Paint -> index 1
# Option 3: Sport Package -> index 2
# Option 4: EV Powertrain -> index 3
# Option 5: Panoramic Sunroof -> index 4
options = [0, 1, 2, 3, 4]

# Car type-option mapping
car_option_mapping = {
    "A": [0],  # Option 1
    "B": [2, 3],  # Options 3, 4
    "C": [1],  # Option 2
    "D": [4],  # Option 5
}

# Initialize solver
solver = Solver()

# Decision variables
# car_type[i] = car type at position i (0-indexed)
car_type = [Int(f"car_type_{i}") for i in range(N)]

# options_present[i][o] = True if option o is present at position i
options_present = [[Bool(f"options_present_{i}_{o}") for o in options] for i in range(N)]

# Helper: car type to index
type_to_idx = {t: i for i, t in enumerate(car_types)}

# 1. Assignment: Each position has exactly one car type, and counts match
for i in range(N):
    solver.add(Or([car_type[i] == type_to_idx[t] for t in car_types]))

for t in car_types:
    idx = type_to_idx[t]
    solver.add(Sum([If(car_type[i] == idx, 1, 0) for i in range(N)]) == car_counts[t])

# 2. Hierarchical Options: Option 5 (index 4) implies Option 1 (index 0)
for i in range(N):
    solver.add(Implies(options_present[i][4], options_present[i][0]))

# 3. Positional Ban: No Option 4 (index 3) at positions 1 or 12 (1-indexed)
for i in [0, 11]:  # 0-indexed positions 0 and 11 correspond to 1 and 12
    solver.add(Not(options_present[i][3]))

# 4. Equipment Cooldown: Cars with Option 2 (index 1) must have at least a 2-slot gap
# This means no two positions i and j with |i - j| <= 2 can both have Option 2
for i in range(N):
    for j in range(i + 1, min(i + 3, N)):  # Check positions i+1 and i+2
        solver.add(Not(And(options_present[i][1], options_present[j][1])))

# 5. Standard Capacity: At most 2 cars with effective Option 1 (Option 1 or Option 5) in any window of 4 consecutive positions
for i in range(N - 3):
    window = [options_present[j][0] for j in range(i, i + 4)]  # Option 1
    window += [options_present[j][4] for j in range(i, i + 4)]  # Option 5
    solver.add(Sum([If(opt, 1, 0) for opt in window]) <= 2)

# 6. Conditional Capacity: For Option 3 (index 2, Sport Package)
# If a position P is preceded by a car with Option 4 (index 3), then at most 1 car with Option 3 in the window [P, P+3]
# Otherwise, at most 2 cars with Option 3 in the window [P, P+3]
for i in range(1, N - 3):  # P ranges from 1 to 8 (0-indexed)
    # Check if position i-1 has Option 4
    preceded_by_option4 = options_present[i-1][3]
    window_option3 = [options_present[j][2] for j in range(i, i + 4)]  # Option 3
    count_option3 = Sum([If(opt, 1, 0) for opt in window_option3])
    solver.add(Implies(preceded_by_option4, count_option3 <= 1))
    solver.add(Implies(Not(preceded_by_option4), count_option3 <= 2))

# Link car_type to options_present based on car_option_mapping
for i in range(N):
    for o in options:
        # Determine if option o is present at position i based on car_type[i]
        possible = []
        for t in car_types:
            if o in car_option_mapping[t]:
                possible.append(car_type[i] == type_to_idx[t])
        solver.add(options_present[i][o] == Or(possible))

# Check for a solution
result = solver.check()

if result == sat:
    model = solver.model()
    print("STATUS: sat")
    # Extract the sequence
    sequence = []
    for i in range(N):
        t_idx = model[car_type[i]].as_long()
        car_t = car_types[t_idx]
        opts = []
        for o in options:
            if model[options_present[i][o]]:
                opts.append(o + 1)  # Convert back to 1-indexed for output
        sequence.append({
            "position": i + 1,
            "car_type": car_t,
            "options": opts
        })
    # Print the sequence
    for car in sequence:
        print(f"Position {car['position']}: Car Type {car['car_type']}, Options {car['options']}")
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")