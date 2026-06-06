from z3 import *

# Create solver
solver = Solver()

# Define riders and bicycles
riders = ['R', 'S', 'T', 'Y']  # Reynaldo, Seamus, Theresa, Yuki
bicycles = ['F', 'G', 'H', 'J']

# Create assignment variables: assign[day][rider] = bicycle
# Day 0 = Day 1, Day 1 = Day 2
assign = [[Int(f"assign_{day}_{rider}") for rider in riders] for day in range(2)]

# Map bicycle names to integers for easier constraint handling
bike_to_int = {bike: i for i, bike in enumerate(bicycles)}
int_to_bike = {i: bike for i, bike in enumerate(bicycles)}

# Domain constraints: each assignment must be a valid bicycle index (0-3)
for day in range(2):
    for rider in riders:
        solver.add(assign[day][riders.index(rider)] >= 0)
        solver.add(assign[day][riders.index(rider)] <= 3)

# Constraint 1: Each rider tests exactly one bicycle per day (already enforced by variable)
# Constraint 2: Each bicycle is tested by exactly one rider per day
for day in range(2):
    # For each bicycle, exactly one rider has that bicycle
    for bike_idx in range(4):
        solver.add(Sum([If(assign[day][rider_idx] == bike_idx, 1, 0) for rider_idx in range(4)]) == 1)

# Constraint 3: Reynaldo cannot test F (on either day)
# F is index 0
for day in range(2):
    solver.add(assign[day][riders.index('R')] != bike_to_int['F'])

# Constraint 4: Yuki cannot test J (on either day)
# J is index 3
for day in range(2):
    solver.add(assign[day][riders.index('Y')] != bike_to_int['J'])

# Constraint 5: Theresa must be one of the testers for H (on either day)
# H is index 2
solver.add(Or(
    assign[0][riders.index('T')] == bike_to_int['H'],
    assign[1][riders.index('T')] == bike_to_int['H']
))

# Constraint 6: The bicycle that Yuki tests on Day 1 must be tested by Seamus on Day 2
yuki_day1_bike = assign[0][riders.index('Y')]
seamus_day2_bike = assign[1][riders.index('S')]
solver.add(seamus_day2_bike == yuki_day1_bike)

# Additional condition: Theresa tests G on the second day
# G is index 1
solver.add(assign[1][riders.index('T')] == bike_to_int['G'])

# Now check which options MUST be true
# For each option, we check if the NEGATION of the option leads to unsatisfiability
# If negation is unsatisfiable, then the option must be true in all models

# Answer choices:
# (A) Reynaldo tests H on the first day.
# (B) Reynaldo tests J on the first day.
# (C) Theresa tests H on the second day.
# (D) Theresa tests J on the first day.
# (E) Yuki tests H on the second day.

# Define option constraints
opt_a = assign[0][riders.index('R')] == bike_to_int['H']  # Reynaldo tests H on Day 1
opt_b = assign[0][riders.index('R')] == bike_to_int['J']  # Reynaldo tests J on Day 1
opt_c = assign[1][riders.index('T')] == bike_to_int['H']  # Theresa tests H on Day 2
opt_d = assign[0][riders.index('T')] == bike_to_int['J']  # Theresa tests J on Day 1
opt_e = assign[1][riders.index('Y')] == bike_to_int['H']  # Yuki tests H on Day 2

# Check each option
must_be_true_options = []

# Option A
solver.push()
solver.add(Not(opt_a))
result_a = solver.check()
solver.pop()
if result_a == unsat:
    must_be_true_options.append('A')

# Option B
solver.push()
solver.add(Not(opt_b))
result_b = solver.check()
solver.pop()
if result_b == unsat:
    must_be_true_options.append('B')

# Option C
solver.push()
solver.add(Not(opt_c))
result_c = solver.check()
solver.pop()
if result_c == unsat:
    must_be_true_options.append('C')

# Option D
solver.push()
solver.add(Not(opt_d))
result_d = solver.check()
solver.pop()
if result_d == unsat:
    must_be_true_options.append('D')

# Option E
solver.push()
solver.add(Not(opt_e))
result_e = solver.check()
solver.pop()
if result_e == unsat:
    must_be_true_options.append('E')

# Print results
if len(must_be_true_options) == 1:
    print("STATUS: sat")
    print(f"answer:{must_be_true_options[0]}")
elif len(must_be_true_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options must be true: {must_be_true_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options must be true")