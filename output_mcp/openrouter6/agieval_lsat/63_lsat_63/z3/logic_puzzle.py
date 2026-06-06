from z3 import *

# Map riders to indices: 0:Reynaldo, 1:Seamus, 2:Theresa, 3:Yuki
# Map bicycles to indices: 0:F, 1:G, 2:H, 3:J

# Variables for day1 and day2 assignments
day1 = [Int(f'day1_{i}') for i in range(4)]
day2 = [Int(f'day2_{i}') for i in range(4)]

solver = Solver()

# Base constraints: each day is a permutation of {0,1,2,3}
for d in [day1, day2]:
    solver.add(Distinct(d))
    for x in d:
        solver.add(x >= 0, x <= 3)

# Constraint 1: Reynaldo cannot test F (0)
solver.add(day1[0] != 0)
solver.add(day2[0] != 0)

# Constraint 2: Yuki cannot test J (3)
solver.add(day1[3] != 3)
solver.add(day2[3] != 3)

# Constraint 3: Theresa must test H (2) on at least one day
solver.add(Or(day1[2] == 2, day2[2] == 2))

# Constraint 4: Yuki's day1 bike is Seamus's day2 bike
solver.add(day2[1] == day1[3])

# Define option constraints
opt_a = (day2[0] == 1)  # Reynaldo tests G on second day
opt_b = (day1[1] == 0)  # Seamus tests F on first day
opt_c = (day2[2] == 0)  # Theresa tests F on second day
opt_d = (day1[0] == 2)  # Reynaldo tests H on first day
opt_e = (day2[3] == 0)  # Yuki tests F on second day

# Evaluate each option: if adding it makes the problem unsat, then it cannot be true
found_unsat = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(constr)
    result = solver.check()
    if result == unsat:
        found_unsat.append(letter)
    solver.pop()

# According to the problem, exactly one option cannot be true
if len(found_unsat) == 1:
    print("STATUS: sat")
    print(f"answer:{found_unsat[0]}")
elif len(found_unsat) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_unsat}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")