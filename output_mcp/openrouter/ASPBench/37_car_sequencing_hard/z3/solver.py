from z3 import *

# Mapping: 0=A, 1=B, 2=C, 3=D
n = 12
car = [Int(f'car_{i}') for i in range(n)]
solver = Solver()
# Domain constraints
for i in range(n):
    solver.add(And(car[i] >= 0, car[i] <= 3))

# Count constraints
solver.add(Sum([If(car[i] == 0, 1, 0) for i in range(n)]) == 3)  # A
solver.add(Sum([If(car[i] == 1, 1, 0) for i in range(n)]) == 3)  # B
solver.add(Sum([If(car[i] == 2, 1, 0) for i in range(n)]) == 4)  # C
solver.add(Sum([If(car[i] == 3, 1, 0) for i in range(n)]) == 2)  # D

# Positional ban: no B at position 0 or 11 (1 or 12)
solver.add(car[0] != 1)
solver.add(car[11] != 1)

# Equipment cooldown for C (type 2): at least 2-slot gap
for i in range(n):
    for d in (1,2):
        if i+d < n:
            solver.add(Not(And(car[i] == 2, car[i+d] == 2)))

# Standard capacity: at most 2 effective Option1 (type A or D) in any window of 4
for s in range(n-3):
    window = [If(Or(car[i] == 0, car[i] == 3), 1, 0) for i in range(s, s+4)]
    solver.add(Sum(window) <= 2)

# Conditional capacity for Option3 (type B)
for p in range(n):
    # Determine limit based on preceding car
    if p == 0:
        limit = 2
    else:
        limit = If(car[p-1] == 1, 1, 2)
    # window indices p .. min(p+3, n-1)
    end = min(p+3, n-1)
    window = [If(car[i] == 1, 1, 0) for i in range(p, end+1)]
    # Since limit may be an If expression, we need to assert Sum <= limit
    solver.add(Sum(window) <= limit)

# Solve
result = solver.check()
if result == sat:
    m = solver.model()
    print("STATUS: sat")
    print("solution_found = True")
    # Helper to map int to letter
    mapping = {0: 'A', 1: 'B', 2: 'C', 3: 'D'}
    for i in range(n):
        typ = m.eval(car[i]).as_long()
        letter = mapping[typ]
        # options per type
        if typ == 0:
            opts = [1]
        elif typ == 1:
            opts = [3,4]
        elif typ == 2:
            opts = [2]
        else:  # D
            opts = [5]
        print(f"position {i+1}: car_type = {letter}, options = {opts}")
else:
    print("STATUS: unsat")