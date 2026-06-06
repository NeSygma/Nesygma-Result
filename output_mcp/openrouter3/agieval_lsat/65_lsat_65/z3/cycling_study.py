from z3 import *

# Create solver
solver = Solver()

# Bicycle indices: 0=F, 1=G, 2=H, 3=J
bicycles = ['F', 'G', 'H', 'J']

# Riders: 0=Reynaldo, 1=Seamus, 2=Theresa, 3=Yuki
riders = ['Reynaldo', 'Seamus', 'Theresa', 'Yuki']

# Variables: day1[rider] = bicycle index, day2[rider] = bicycle index
day1 = [Int(f'day1_{r}') for r in range(4)]
day2 = [Int(f'day2_{r}') for r in range(4)]

# Domain constraints: each variable must be 0, 1, 2, or 3
for i in range(4):
    solver.add(day1[i] >= 0, day1[i] <= 3)
    solver.add(day2[i] >= 0, day2[i] <= 3)

# Each bicycle is tested by exactly one rider each day
for day in [day1, day2]:
    solver.add(Distinct(day))

# Constraint 1: Reynaldo cannot test F (index 0)
solver.add(day1[0] != 0)  # Reynaldo is rider 0
solver.add(day2[0] != 0)

# Constraint 2: Yuki cannot test J (index 3)
solver.add(day1[3] != 3)  # Yuki is rider 3
solver.add(day2[3] != 3)

# Constraint 3: Theresa must be one of the testers for H (index 2)
# This means Theresa tests H on either day 1 or day 2 (or both)
solver.add(Or(day1[2] == 2, day2[2] == 2))  # Theresa is rider 2

# Constraint 4: The bicycle that Yuki tests on Day 1 must be tested by Seamus on Day 2
# Yuki is rider 3, Seamus is rider 1
solver.add(day2[1] == day1[3])

# Now test each option to see which CANNOT be true
# Option A: Both Reynaldo and Seamus test J (index 3)
opt_a = And(day1[0] == 3, day1[1] == 3)  # Both test J on day 1
# OR both test J on day 2
opt_a = Or(opt_a, And(day2[0] == 3, day2[1] == 3))
# OR one tests J on day 1 and the other on day 2
opt_a = Or(opt_a, And(day1[0] == 3, day2[1] == 3))
opt_a = Or(opt_a, And(day2[0] == 3, day1[1] == 3))

# Option B: Both Reynaldo and Theresa test J (index 3)
opt_b = Or(
    And(day1[0] == 3, day1[2] == 3),
    And(day2[0] == 3, day2[2] == 3),
    And(day1[0] == 3, day2[2] == 3),
    And(day2[0] == 3, day1[2] == 3)
)

# Option C: Both Reynaldo and Yuki test G (index 1)
opt_c = Or(
    And(day1[0] == 1, day1[3] == 1),
    And(day2[0] == 1, day2[3] == 1),
    And(day1[0] == 1, day2[3] == 1),
    And(day2[0] == 1, day1[3] == 1)
)

# Option D: Both Seamus and Theresa test G (index 1)
opt_d = Or(
    And(day1[1] == 1, day1[2] == 1),
    And(day2[1] == 1, day2[2] == 1),
    And(day1[1] == 1, day2[2] == 1),
    And(day2[1] == 1, day1[2] == 1)
)

# Option E: Both Theresa and Yuki test F (index 0)
opt_e = Or(
    And(day1[2] == 0, day1[3] == 0),
    And(day2[2] == 0, day2[3] == 0),
    And(day1[2] == 0, day2[3] == 0),
    And(day2[2] == 0, day1[3] == 0)
)

# Test each option
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