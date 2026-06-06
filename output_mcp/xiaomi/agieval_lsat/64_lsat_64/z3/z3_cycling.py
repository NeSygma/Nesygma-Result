from z3 import *

# Riders: 0=Reynaldo, 1=Seamus, 2=Theresa, 3=Yuki
# Bicycles: 0=F, 1=G, 2=H, 3=J

# day1[r] = bicycle tested by rider r on day 1
# day2[r] = bicycle tested by rider r on day 2

day1 = [Int(f'day1_{r}') for r in range(4)]
day2 = [Int(f'day2_{r}') for r in range(4)]

solver = Solver()

# Domain: each assignment is 0..3
for r in range(4):
    solver.add(day1[r] >= 0, day1[r] <= 3)
    solver.add(day2[r] >= 0, day2[r] <= 3)

# All different on each day
solver.add(Distinct(day1))
solver.add(Distinct(day2))

# Each rider tests a different bicycle on day 2 than day 1
for r in range(4):
    solver.add(day1[r] != day2[r])

# Condition 1: Reynaldo cannot test F (bicycle 0)
solver.add(day1[0] != 0)
solver.add(day2[0] != 0)

# Condition 2: Yuki cannot test J (bicycle 3)
solver.add(day1[3] != 3)
solver.add(day2[3] != 3)

# Condition 3: Theresa must be one of the testers for H (bicycle 2)
solver.add(Or(day1[2] == 2, day2[2] == 2))

# Condition 4: The bicycle that Yuki tests on day 1 must be tested by Seamus on day 2
solver.add(day2[1] == day1[3])

# Additional constraint from the question: Theresa tests J on the first day
solver.add(day1[2] == 3)

# Now evaluate each option
# (A) Reynaldo tests G on the second day.
opt_a = (day2[0] == 1)
# (B) Seamus tests H on the first day.
opt_b = (day1[1] == 2)
# (C) Yuki tests H on the second day.
opt_c = (day2[3] == 2)
# (D) Seamus is one of the testers for J.
opt_d = Or(day1[1] == 3, day2[1] == 3)
# (E) Theresa is one of the testers for G.
opt_e = Or(day1[2] == 1, day2[2] == 1)

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