from z3 import *

# Map riders to indices: 0:Reynaldo, 1:Seamus, 2:Theresa, 3:Yuki
# Map bicycles to indices: 0:F, 1:G, 2:H, 3:J

day1 = [Int(f'day1_{i}') for i in range(4)]
day2 = [Int(f'day2_{i}') for i in range(4)]

solver = Solver()

# Each day is a permutation of {0,1,2,3}
for d in [day1, day2]:
    solver.add(Distinct(d))
    for x in d:
        solver.add(x >= 0, x <= 3)

# Reynaldo cannot test F (0)
solver.add(day1[0] != 0)
solver.add(day2[0] != 0)

# Yuki cannot test J (3)
solver.add(day1[3] != 3)
solver.add(day2[3] != 3)

# Theresa must test H (2) on at least one day
solver.add(Or(day1[2] == 2, day2[2] == 2))

# Yuki's day1 bike is Seamus's day2 bike
solver.add(day2[1] == day1[3])

# Each rider tests a different bike on day2 vs day1
for i in range(4):
    solver.add(day1[i] != day2[i])

# Define option constraints
opt_a = (day2[0] == 1)   # Reynaldo tests G on second day
opt_b = (day1[1] == 0)   # Seamus tests F on first day
opt_c = (day2[2] == 0)   # Theresa tests F on second day
opt_d = (day1[0] == 2)   # Reynaldo tests H on first day
opt_e = (day2[3] == 0)   # Yuki tests F on second day

options = [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]

impossible_options = []
for letter, constr in options:
    solver.push()
    solver.add(constr)
    if solver.check() == unsat:
        impossible_options.append(letter)
    solver.pop()

if len(impossible_options) == 1:
    print("STATUS: sat")
    print(f"answer:{impossible_options[0]}")
elif len(impossible_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple impossible options found {impossible_options}")
else:
    print("STATUS: unsat")
    print("Refine: No impossible options found")