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

# Now test each answer choice
# Answer choices:
# (A) Reynaldo tests H on the first day.
# (B) Reynaldo tests J on the first day.
# (C) Theresa tests H on the second day.
# (D) Theresa tests J on the first day.
# (E) Yuki tests H on the second day.

# Define option constraints
opt_a_constr = assign[0][riders.index('R')] == bike_to_int['H']  # Reynaldo tests H on Day 1
opt_b_constr = assign[0][riders.index('R')] == bike_to_int['J']  # Reynaldo tests J on Day 1
opt_c_constr = assign[1][riders.index('T')] == bike_to_int['H']  # Theresa tests H on Day 2
opt_d_constr = assign[0][riders.index('T')] == bike_to_int['J']  # Theresa tests J on Day 1
opt_e_constr = assign[1][riders.index('Y')] == bike_to_int['H']  # Yuki tests H on Day 2

found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
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