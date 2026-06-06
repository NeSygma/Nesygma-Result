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

print("Checking base constraints...")
result = solver.check()
if result == sat:
    print("Base constraints are satisfiable.")
    m = solver.model()
    print("Example model:")
    for i in range(4):
        print(f"  Rider {i}: day1={m[day1[i]]}, day2={m[day2[i]]}")
elif result == unsat:
    print("Base constraints are unsatisfiable!")
else:
    print("Unknown")