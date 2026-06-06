from z3 import *

solver = Solver()

# Riders: 0=Reynaldo, 1=Seamus, 2=Theresa, 3=Yuki
# Bicycles: 0=F, 1=G, 2=H, 3=J
# Variables: day1[r] = bicycle tested by rider r on day 1
#            day2[r] = bicycle tested by rider r on day 2

day1 = [Int(f'day1_{r}') for r in range(4)]
day2 = [Int(f'day2_{r}') for r in range(4)]

# Domain constraints: each assignment is 0-3
for r in range(4):
    solver.add(day1[r] >= 0, day1[r] <= 3)
    solver.add(day2[r] >= 0, day2[r] <= 3)

# All different on each day (each bicycle tested by exactly one rider)
solver.add(Distinct(day1))
solver.add(Distinct(day2))

# Each rider tests a different bicycle on day 2 than day 1
for r in range(4):
    solver.add(day1[r] != day2[r])

# Constraint 1: Reynaldo cannot test F (bicycle 0) on either day
solver.add(day1[0] != 0)
solver.add(day2[0] != 0)

# Constraint 2: Yuki cannot test J (bicycle 3) on either day
solver.add(day1[3] != 3)
solver.add(day2[3] != 3)

# Constraint 3: Theresa must test H (bicycle 2) on at least one day
solver.add(Or(day1[2] == 2, day2[2] == 2))

# Constraint 4: Bicycle Yuki tests on day 1 must be tested by Seamus on day 2
solver.add(day2[1] == day1[3])

# Now test each option to see which CANNOT be true
# Option A: Reynaldo tests G (bicycle 1) on the second day
opt_a = (day2[0] == 1)
# Option B: Seamus tests F (bicycle 0) on the first day
opt_b = (day1[1] == 0)
# Option C: Theresa tests F (bicycle 0) on the second day
opt_c = (day2[2] == 0)
# Option D: Reynaldo tests H (bicycle 2) on the first day
opt_d = (day1[0] == 2)
# Option E: Yuki tests F (bicycle 0) on the second day
opt_e = (day2[3] == 0)

found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
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