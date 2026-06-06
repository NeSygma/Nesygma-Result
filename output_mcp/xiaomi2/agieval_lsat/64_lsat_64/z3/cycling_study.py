from z3 import *

solver = Solver()

# Riders: R=0, S=1, T=2, Y=3
# Bicycles: F=0, G=1, H=2, J=3

# Day 1 and Day 2 assignments (bicycle index per rider)
day1 = [Int(f'day1_{i}') for i in range(4)]  # R, S, T, Y
day2 = [Int(f'day2_{i}') for i in range(4)]  # R, S, T, Y

# Domain: each assignment is 0-3 (F, G, H, J)
for i in range(4):
    solver.add(day1[i] >= 0, day1[i] <= 3)
    solver.add(day2[i] >= 0, day2[i] <= 3)

# Each day, all bicycles are tested (all distinct per day)
solver.add(Distinct(day1))
solver.add(Distinct(day2))

# Each rider tests a different bicycle on Day 2 than Day 1
for i in range(4):
    solver.add(day1[i] != day2[i])

# Constraint 1: Reynaldo cannot test F (on either day)
solver.add(day1[0] != 0)  # F=0
solver.add(day2[0] != 0)

# Constraint 2: Yuki cannot test J (on either day)
solver.add(day1[3] != 3)  # J=3
solver.add(day2[3] != 3)

# Constraint 3: Theresa must test H on at least one day
solver.add(Or(day1[2] == 2, day2[2] == 2))  # H=2

# Constraint 4: Yuki's Day 1 bicycle = Seamus's Day 2 bicycle
solver.add(day2[1] == day1[3])

# Question premise: Theresa tests J on the first day
solver.add(day1[2] == 3)  # J=3

# From premise + constraint 3: Theresa must test H on Day 2
# (This follows automatically from the constraints)

# Define answer choice constraints
# (A) Reynaldo tests G on the second day
opt_a = (day2[0] == 1)  # G=1

# (B) Seamus tests H on the first day
opt_b = (day1[1] == 2)  # H=2

# (C) Yuki tests H on the second day
opt_c = (day2[3] == 2)  # H=2

# (D) Seamus is one of the testers for J
opt_d = Or(day1[1] == 3, day2[1] == 3)  # J=3

# (E) Theresa is one of the testers for G
opt_e = Or(day1[2] == 1, day2[2] == 1)  # G=1

# Test each option
found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
        m = solver.model()
        print(f"Option {letter} is SAT:")
        for i in range(4):
            riders = ['Reynaldo', 'Seamus', 'Theresa', 'Yuki']
            bikes = ['F', 'G', 'H', 'J']
            d1 = m[day1[i]].as_long()
            d2 = m[day2[i]].as_long()
            print(f"  {riders[i]}: Day1={bikes[d1]}, Day2={bikes[d2]}")
    else:
        print(f"Option {letter} is UNSAT")
    solver.pop()

print()
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")