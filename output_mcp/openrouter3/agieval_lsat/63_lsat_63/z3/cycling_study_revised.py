from z3 import *

# Create solver
solver = Solver()

# Define bicycle indices
F, G, H, J = 0, 1, 2, 3
bicycles = [F, G, H, J]

# Riders: 0=Reynaldo, 1=Seamus, 2=Theresa, 3=Yuki
riders = [0, 1, 2, 3]
R, S, T, Y = 0, 1, 2, 3

# Variables: day1[rider] = bicycle tested on day 1
#            day2[rider] = bicycle tested on day 2
day1 = [Int(f'day1_{r}') for r in riders]
day2 = [Int(f'day2_{r}') for r in riders]

# Each rider tests exactly one bicycle per day (domain constraints)
for r in riders:
    solver.add(day1[r] >= 0, day1[r] <= 3)
    solver.add(day2[r] >= 0, day2[r] <= 3)

# Each bicycle is tested by exactly one rider per day
for d in [day1, day2]:
    solver.add(Distinct(d))

# Constraint 1: Reynaldo cannot test F (on either day)
solver.add(day1[R] != F)
solver.add(day2[R] != F)

# Constraint 2: Yuki cannot test J (on either day)
solver.add(day1[Y] != J)
solver.add(day2[Y] != J)

# Constraint 3: Theresa must be one of the testers for H (on either day)
solver.add(Or(day1[T] == H, day2[T] == H))

# Constraint 4: The bicycle that Yuki tests on Day 1 must be tested by Seamus on Day 2
# This means: day2[S] == day1[Y]
solver.add(day2[S] == day1[Y])

# Now evaluate each option - we want to find which option CANNOT be true
# Option A: Reynaldo tests G on the second day
opt_a = (day2[R] == G)

# Option B: Seamus tests F on the first day
opt_b = (day1[S] == F)

# Option C: Theresa tests F on the second day
opt_c = (day2[T] == F)

# Option D: Reynaldo tests H on the first day
opt_d = (day1[R] == H)

# Option E: Yuki tests F on the second day
opt_e = (day2[Y] == F)

# Test each option - we want to find which option makes the problem UNSAT
# (i.e., which option CANNOT be true)
cannot_be_true = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(constr)
    result = solver.check()
    if result == unsat:
        cannot_be_true.append(letter)
    solver.pop()

# Print results
if len(cannot_be_true) == 1:
    print("STATUS: sat")
    print(f"answer:{cannot_be_true[0]}")
elif len(cannot_be_true) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options cannot be true {cannot_be_true}")
else:
    print("STATUS: unsat")
    print("Refine: No options found that cannot be true")