from z3 import *

solver = Solver()

# 0=Reynaldo, 1=Seamus, 2=Theresa, 3=Yuki
# 0=F, 1=G, 2=H, 3=J
riders = 4
bikes = 4

day1 = [Int(f"day1_{i}") for i in range(riders)]
day2 = [Int(f"day2_{i}") for i in range(riders)]

# Domain: each assignment is 0-3
for i in range(riders):
    solver.add(And(day1[i] >= 0, day1[i] <= 3))
    solver.add(And(day2[i] >= 0, day2[i] <= 3))

# All four bicycles tested each day
solver.add(Distinct(day1))
solver.add(Distinct(day2))

# Each rider tests a different bicycle on day 2
for i in range(riders):
    solver.add(day1[i] != day2[i])

# Reynaldo cannot test F (bike 0)
solver.add(day1[0] != 0)
solver.add(day2[0] != 0)

# Yuki cannot test J (bike 3)
solver.add(day1[3] != 3)
solver.add(day2[3] != 3)

# Theresa must be one of the testers for H (bike 2)
solver.add(Or(day1[2] == 2, day2[2] == 2))

# The bicycle that Yuki tests on first day must be tested by Seamus on second day
solver.add(day2[1] == day1[3])

# Now test each option
options = [
    ("A", day1[0] == 3),   # Reynaldo tests J on first day
    ("B", day2[0] == 3),   # Reynaldo tests J on second day
    ("C", day1[1] == 2),   # Seamus tests H on first day
    ("D", day1[3] == 2),   # Yuki tests H on first day
    ("E", day2[3] == 2),   # Yuki tests H on second day
]

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