from z3 import *

# Bike indices: 0=F,1=G,2=H,3=J
R, S, T, Y = 0,1,2,3

# Variables for day1 and day2 assignments
day1 = [Int(f'd1_{r}') for r in range(4)]
day2 = [Int(f'd2_{r}') for r in range(4)]

solver = Solver()

# Domain constraints
for v in day1+day2:
    solver.add(v >= 0, v <= 3)

# Each day uses each bike exactly once
solver.add(Distinct(day1))
solver.add(Distinct(day2))

# No rider repeats same bike on both days
for i in range(4):
    solver.add(day2[i] != day1[i])

# Reynaldo cannot test F (0)
solver.add(day1[R] != 0)
solver.add(day2[R] != 0)

# Yuki cannot test J (3)
solver.add(day1[Y] != 3)
solver.add(day2[Y] != 3)

# Theresa must test H (2) on at least one day
solver.add(Or(day1[T] == 2, day2[T] == 2))

# Yuki's day1 bike must be Seamus's day2 bike
solver.add(day2[S] == day1[Y])

# Option constraints
opt_a = (day2[R] == 1)  # Reynaldo tests G on day2
opt_b = (day1[S] == 0)  # Seamus tests F on day1
opt_c = (day2[T] == 0)  # Theresa tests F on day2
opt_d = (day1[R] == 2)  # Reynaldo tests H on day1
opt_e = (day2[Y] == 0)  # Yuki tests F on day2

options = [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]

found_options = []
for letter, constr in options:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
    solver.pop()

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")