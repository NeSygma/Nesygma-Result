from z3 import *

# Problem setup
N = 12
types = ['A', 'B', 'C', 'D']
type_counts = {'A': 3, 'B': 3, 'C': 4, 'D': 2}

# Options per type
type_options = {
    'A': [1],
    'B': [3, 4],
    'C': [2],
    'D': [5]
}

# Effective options: Option 5 implies Option 1 for constraint purposes
# So type D effectively has options [5, 1] for sunroof counting
type_effective_options = {
    'A': [1],
    'B': [3, 4],
    'C': [2],
    'D': [5, 1]  # Option 5 implies Option 1
}

solver = Solver()

# Decision variables: car_type at each position (0-indexed internally, 1-indexed for output)
car = [Int(f'car_{i}') for i in range(N)]

# Map types to integers
type_map = {'A': 0, 'B': 1, 'C': 2, 'D': 3}
inv_type_map = {v: k for k, v in type_map.items()}

# Constraint 1: Each position has a valid car type
for i in range(N):
    solver.add(Or([car[i] == type_map[t] for t in types]))

# Constraint 1: Each type appears exactly the specified number of times
for t in types:
    solver.add(Sum([If(car[i] == type_map[t], 1, 0) for i in range(N)]) == type_counts[t])

# Helper: check if car at position i has option opt
def has_option(i, opt):
    # Type A has option 1, B has 3,4, C has 2, D has 5
    if opt == 1:
        return Or(car[i] == type_map['A'], car[i] == type_map['D'])  # D has panoramic which implies 1
    elif opt == 2:
        return car[i] == type_map['C']
    elif opt == 3:
        return car[i] == type_map['B']
    elif opt == 4:
        return car[i] == type_map['B']
    elif opt == 5:
        return car[i] == type_map['D']
    else:
        return False

# Constraint 3: Positional Ban - No car with Option 4 at position 1 or 12
solver.add(Not(has_option(0, 4)))   # position 1 (index 0)
solver.add(Not(has_option(11, 4)))  # position 12 (index 11)

# Constraint 4: Equipment Cooldown - Cars with Option 2 must have at least 2-slot gap
# Cannot be at positions P and P+1, or P and P+2
for i in range(N):
    for j in range(i+1, min(i+3, N)):
        solver.add(Not(And(has_option(i, 2), has_option(j, 2))))

# Constraint 5: Standard Capacity - At most 2 cars with effective Option 1 in any window of 4
for i in range(N - 3):
    window = [If(has_option(j, 1), 1, 0) for j in range(i, i+4)]
    solver.add(Sum(window) <= 2)

# Constraint 6: Conditional Capacity for Option 3
# For each position P (0-indexed), consider window [P, P+3]
# If position P is preceded by a car with EV (Option 4), then at most 1 car with Option 3 in window
# Otherwise, at most 2 cars with Option 3 in window
for p in range(N - 3):
    # Check if position p is preceded by a car with Option 4
    # "preceded by" means position p-1 has Option 4
    preceded_by_ev = False
    if p > 0:
        preceded_by_ev = has_option(p-1, 4)
    
    window_opt3 = [If(has_option(j, 3), 1, 0) for j in range(p, p+4)]
    sum_opt3 = Sum(window_opt3)
    
    # Conditional constraint
    if p > 0:
        solver.add(If(preceded_by_ev, sum_opt3 <= 1, sum_opt3 <= 2))
    else:
        # Position 1 has no predecessor, so use the "otherwise" case
        solver.add(sum_opt3 <= 2)

# Solve
BENCHMARK_MODE = True
result = solver.check()

if result == sat:
    m = solver.model()
    print("STATUS: sat")
    print("solution_found: True")
    print("sequence:")
    for i in range(N):
        t_val = m[car[i]].as_long()
        t_name = inv_type_map[t_val]
        opts = type_options[t_name]
        print(f"  - position: {i+1}")
        print(f"    car_type: \"{t_name}\"")
        print(f"    options: {opts}")
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")