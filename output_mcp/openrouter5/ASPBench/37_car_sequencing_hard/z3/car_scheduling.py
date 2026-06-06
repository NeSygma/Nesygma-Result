from z3 import *

# Total positions
N = 12

# Car types: A=0, B=1, C=2, D=3
# Counts
counts = [3, 3, 4, 2]  # A, B, C, D

# Options per type (0-indexed options: 0=Option1, 1=Option2, 2=Option3, 3=Option4, 4=Option5)
type_options = {
    0: [0],       # Type A: Option 1 (Standard Sunroof)
    1: [2, 3],    # Type B: Options 3, 4 (Sport Package, EV Powertrain)
    2: [1],       # Type C: Option 2 (Custom Paint)
    3: [4]        # Type D: Option 5 (Panoramic Sunroof)
}

# Decision variables: car_type at each position (0-indexed positions 0..11)
car_type = [Int(f'car_type_{i}') for i in range(N)]

solver = Solver()

# Domain: each position gets a car type 0..3
for i in range(N):
    solver.add(car_type[i] >= 0, car_type[i] <= 3)

# Constraint 1: Exact counts per type
for t in range(4):
    solver.add(Sum([If(car_type[i] == t, 1, 0) for i in range(N)]) == counts[t])

# Helper: does a car type have a given option?
def has_option(car_type_var, opt_idx):
    """Return a Z3 Bool expression: car_type_var has option opt_idx."""
    return Or([And(car_type_var == t, opt_idx in type_options[t]) for t in range(4)])

# Constraint 2: Hierarchical Options - Option 5 implies Option 1 for constraint purposes.
# For any position i, if car has Option 5, then for constraint purposes it also has Option 1.
# We'll handle this by defining "effective Option 1" as: has Option 1 OR has Option 5.
def has_effective_option1(car_type_var):
    return Or(has_option(car_type_var, 0), has_option(car_type_var, 4))

# Constraint 3: Positional Ban - No car with Option 4 (EV Powertrain) at position 1 or 12 (0-indexed: 0 or 11)
solver.add(Not(has_option(car_type[0], 3)))  # position 1
solver.add(Not(has_option(car_type[11], 3)))  # position 12

# Constraint 4: Equipment Cooldown - Option 2 (Custom Paint) must have at least 2-slot gap
# Cannot be at positions P and P+1, or P and P+2.
for i in range(N):
    for j in range(i+1, min(i+3, N)):
        # Cannot both have Option 2
        solver.add(Not(And(has_option(car_type[i], 1), has_option(car_type[j], 1))))

# Constraint 5: Standard Capacity - At most 2 cars with effective Option 1 in any window of 4 consecutive positions
for start in range(N - 3):
    window = [car_type[start + k] for k in range(4)]
    solver.add(Sum([If(has_effective_option1(car_type[start + k]), 1, 0) for k in range(4)]) <= 2)

# Constraint 6: Conditional Capacity for Option 3 (Sport Package)
# For each window starting at P (0-indexed), window [P, P+3]:
#   If position P-1 (preceding) has EV (Option 4), then at most 1 car with Option 3 in window
#   Otherwise, at most 2 cars with Option 3 in window
for P in range(N - 3):
    # preceding position is P-1 (if P > 0)
    if P > 0:
        preceded_by_ev = has_option(car_type[P-1], 3)  # Option 4 is index 3
    else:
        preceded_by_ev = False  # No preceding car at position 1
    
    count_opt3 = Sum([If(has_option(car_type[P + k], 2), 1, 0) for k in range(4)])
    
    if P > 0:
        solver.add(Implies(preceded_by_ev, count_opt3 <= 1))
        solver.add(Implies(Not(preceded_by_ev), count_opt3 <= 2))
    else:
        solver.add(count_opt3 <= 2)

# Solve
BENCHMARK_MODE = True
result = solver.check()

if result == sat:
    m = solver.model()
    print("STATUS: sat")
    print("solution_found: True")
    print("sequence:")
    type_names = ["A", "B", "C", "D"]
    for i in range(N):
        t = m[car_type[i]].as_long()
        opts = type_options[t]
        print(f"  position: {i+1}, car_type: {type_names[t]}, options: {opts}")
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")