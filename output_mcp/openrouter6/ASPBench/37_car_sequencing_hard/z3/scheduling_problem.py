from z3 import *

# Problem parameters
N = 12  # total positions
car_types = ["A", "B", "C", "D"]
type_counts = {"A": 3, "B": 3, "C": 4, "D": 2}
type_to_int = {"A": 0, "B": 1, "C": 2, "D": 3}

# Create solver
solver = Solver()

# Variables: type[i] for position i (0-indexed)
type_vars = [Int(f"type_{i}") for i in range(N)]

# Domain constraints for each position: type must be 0,1,2,3
for i in range(N):
    solver.add(Or([type_vars[i] == t for t in range(4)]))

# 1. Count constraints
for t_name, t_int in type_to_int.items():
    count = Sum([If(type_vars[i] == t_int, 1, 0) for i in range(N)])
    solver.add(count == type_counts[t_name])

# Helper functions for options (using If expressions)
def has_option1(i):
    # Option 1: Type A (0) OR Type D (3) because D has Option 5 which implies Option 1
    return Or(type_vars[i] == 0, type_vars[i] == 3)

def has_option2(i):
    # Option 2: Type C (2)
    return type_vars[i] == 2

def has_option3(i):
    # Option 3: Type B (1)
    return type_vars[i] == 1

def has_option4(i):
    # Option 4: Type B (1)
    return type_vars[i] == 1

def has_option5(i):
    # Option 5: Type D (3)
    return type_vars[i] == 3

# 2. Positional ban: No Option 4 at positions 1 or 12 (0-indexed: 0 and 11)
solver.add(Not(has_option4(0)))  # position 1
solver.add(Not(has_option4(11))) # position 12

# 3. Equipment cooldown for Option 2: at least 2-slot gap
for i in range(N-1):
    # Cannot have Option 2 at consecutive positions
    solver.add(Not(And(has_option2(i), has_option2(i+1))))
for i in range(N-2):
    # Cannot have Option 2 with one gap (positions i and i+2)
    solver.add(Not(And(has_option2(i), has_option2(i+2))))

# 4. Standard Capacity: At most 2 cars with effective Option 1 in any window of 4 consecutive positions
for start in range(N-3):  # windows starting at 0..8 (positions 1..9)
    window_sum = Sum([If(has_option1(start + j), 1, 0) for j in range(4)])
    solver.add(window_sum <= 2)

# 5. Conditional Capacity for Option 3
for p in range(N-3):  # p from 0 to 8 (positions 1 to 9)
    # Check if position p (0-indexed) is preceded by a car with EV (Option 4)
    # For p=0, there's no preceding car, so treat as "otherwise"
    if p == 0:
        # No preceding car, so at most 2 Option 3 in window [p, p+3]
        window_sum = Sum([If(has_option3(p + j), 1, 0) for j in range(4)])
        solver.add(window_sum <= 2)
    else:
        # Check if position p-1 has Option 4
        preceded_by_ev = has_option4(p-1)
        window_sum = Sum([If(has_option3(p + j), 1, 0) for j in range(4)])
        # If preceded by EV, at most 1; else at most 2
        solver.add(If(preceded_by_ev, window_sum <= 1, window_sum <= 2))

# Check for solution
result = solver.check()

if result == sat:
    model = solver.model()
    print("STATUS: sat")
    print("solution_found: True")
    print("sequence: [")
    for i in range(N):
        type_val = model[type_vars[i]].as_long()
        car_type = car_types[type_val]
        # Determine options for this car type
        options = []
        if car_type == "A":
            options = [1]
        elif car_type == "B":
            options = [3, 4]
        elif car_type == "C":
            options = [2]
        elif car_type == "D":
            options = [5]
        # Print position (1-indexed)
        print(f'  {{"position": {i+1}, "car_type": "{car_type}", "options": {options}}}', end="")
        if i < N-1:
            print(",")
        else:
            print()
    print("]")
elif result == unsat:
    print("STATUS: unsat")
    print("solution_found: False")
    print("No valid sequence found.")
else:
    print("STATUS: unknown")
    print("solver returned unknown")