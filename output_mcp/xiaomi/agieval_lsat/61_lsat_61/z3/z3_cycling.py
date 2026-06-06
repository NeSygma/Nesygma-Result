from z3 import *

# Riders: Reynaldo=0, Seamus=1, Theresa=2, Yuki=3
# Bicycles: F=0, G=1, H=2, J=3

# day1[r] = bicycle tested by rider r on day 1
# day2[r] = bicycle tested by rider r on day 2

day1 = [Int(f'day1_{r}') for r in range(4)]
day2 = [Int(f'day2_{r}') for r in range(4)]

solver = Solver()

# Domain constraints: each assignment is 0-3
for r in range(4):
    solver.add(day1[r] >= 0, day1[r] <= 3)
    solver.add(day2[r] >= 0, day2[r] <= 3)

# All different on each day
solver.add(Distinct(day1))
solver.add(Distinct(day2))

# Each rider tests a different bicycle on day 2 vs day 1
for r in range(4):
    solver.add(day1[r] != day2[r])

# Reynaldo cannot test F (bicycle 0) on either day
solver.add(day1[0] != 0)
solver.add(day2[0] != 0)

# Yuki cannot test J (bicycle 3) on either day
solver.add(day1[3] != 3)
solver.add(day2[3] != 3)

# Theresa must be one of the testers for H (bicycle 2)
solver.add(Or(day1[2] == 2, day2[2] == 2))

# The bicycle that Yuki tests on day 1 must be tested by Seamus on day 2
solver.add(day2[1] == day1[3])

# Additional condition: Theresa tests G on the second day
solver.add(day2[2] == 1)  # G = 1

# Now evaluate each answer choice
# (A) Reynaldo tests H on the first day. -> day1[0] == 2
# (B) Reynaldo tests J on the first day. -> day1[0] == 3
# (C) Theresa tests H on the second day. -> day2[2] == 2
# (D) Theresa tests J on the first day. -> day1[2] == 3
# (E) Yuki tests H on the second day. -> day2[3] == 2

options = [
    ("A", day1[0] == 2),
    ("B", day1[0] == 3),
    ("C", day2[2] == 2),
    ("D", day1[2] == 3),
    ("E", day2[3] == 2),
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