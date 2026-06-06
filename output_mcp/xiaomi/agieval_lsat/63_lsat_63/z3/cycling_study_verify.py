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

# Option C: Theresa tests F (bicycle 0) on the second day
solver.add(day2[2] == 0)

result = solver.check()
print(f"Option C satisfiability: {result}")

if result == sat:
    m = solver.model()
    print("STATUS: sat")
    print("Option C CAN be true")
    print("Day 1 assignments:")
    for r in range(4):
        rider_names = ["Reynaldo", "Seamus", "Theresa", "Yuki"]
        bike_names = ["F", "G", "H", "J"]
        print(f"  {rider_names[r]}: {bike_names[m[day1[r]].as_long()]}")
    print("Day 2 assignments:")
    for r in range(4):
        print(f"  {rider_names[r]}: {bike_names[m[day2[r]].as_long()]}")
else:
    print("STATUS: proved")
    print("Option C CANNOT be true")