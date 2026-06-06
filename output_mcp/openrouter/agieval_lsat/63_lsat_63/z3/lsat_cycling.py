from z3 import *

# Bike mapping: 0=F,1=G,2=H,3=J
bikes = ['F','G','H','J']
# Riders indices: 0=R,1=S,2=T,3=Y
R, S, T, Y = 0,1,2,3

# Variables for day1 and day2 assignments
# day1[i] = bike assigned to rider i on day1
# day2[i] = bike assigned to rider i on day2
day1 = [Int(f'd1_{r}') for r in range(4)]
day2 = [Int(f'd2_{r}') for r in range(4)]

solver = Solver()

# Domain constraints
for v in day1+day2:
    solver.add(v >= 0, v <= 3)

# Each day uses each bike exactly once (all distinct)
solver.add(Distinct(day1))
solver.add(Distinct(day2))

# Reynaldo cannot test F (bike 0) any day
solver.add(day1[R] != 0)
solver.add(day2[R] != 0)

# Yuki cannot test J (bike 3) any day
solver.add(day1[Y] != 3)
solver.add(day2[Y] != 3)

# Theresa must test H (bike 2) on at least one day
solver.add(Or(day1[T] == 2, day2[T] == 2))

# The bicycle Yuki tests on day1 must be tested by Seamus on day2
solver.add(day2[S] == day1[Y])

# Define option constraints
opt_a = (day2[R] == 1)  # G is bike 1
opt_b = (day1[S] == 0)  # F is bike 0
opt_c = (day2[T] == 0)  # F is bike 0
opt_d = (day1[R] == 2)  # H is bike 2
opt_e = (day2[Y] == 0)  # F is bike 0

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