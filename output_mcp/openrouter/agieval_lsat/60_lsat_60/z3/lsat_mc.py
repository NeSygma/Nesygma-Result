from z3 import *

# Rider encoding
R, S, T, Y = 0, 1, 2, 3

# Variables: rider assigned to each bike on each day
# day1_F, day1_G, day1_H, day1_J
# day2_F, day2_G, day2_H, day2_J

day1_F = Int('day1_F')
day1_G = Int('day1_G')
day1_H = Int('day1_H')
day1_J = Int('day1_J')

day2_F = Int('day2_F')
day2_G = Int('day2_G')
day2_H = Int('day2_H')
day2_J = Int('day2_J')

solver = Solver()
# Domain constraints
vars = [day1_F, day1_G, day1_H, day1_J, day2_F, day2_G, day2_H, day2_J]
for v in vars:
    solver.add(v >= 0, v <= 3)
# Each day a permutation of riders
solver.add(Distinct(day1_F, day1_G, day1_H, day1_J))
solver.add(Distinct(day2_F, day2_G, day2_H, day2_J))
# Constraint 1: Reynaldo cannot test F
solver.add(day1_F != R)
solver.add(day2_F != R)
# Constraint 2: Yuki cannot test J
solver.add(day1_J != Y)
solver.add(day2_J != Y)
# Constraint 3: Theresa must test H at least once
solver.add(Or(day1_H == T, day2_H == T))
# Constraint 4: Yuki's bike day1 is Seamus's bike day2
solver.add(Or(
    And(day1_F == Y, day2_F == S),
    And(day1_G == Y, day2_G == S),
    And(day1_H == Y, day2_H == S),
    And(day1_J == Y, day2_J == S)
))

# Helper to create constraint for an option
def option_constraint(assignments):
    # assignments dict: variable -> value
    cons = []
    for var, val in assignments.items():
        cons.append(var == val)
    return And(cons)

# Define each option's assignments
opt_A = {
    day1_F: S, day2_F: R,
    day1_G: Y, day2_G: S,
    day1_H: T, day2_H: Y,
    day1_J: R, day2_J: T,
}
opt_B = {
    day1_F: S, day2_F: Y,
    day1_G: R, day2_G: T,
    day1_H: Y, day2_H: S,
    day1_J: T, day2_J: R,
}
opt_C = {
    day1_F: Y, day2_F: S,
    day1_G: S, day2_G: R,
    day1_H: T, day2_H: Y,
    day1_J: R, day2_J: T,
}
opt_D = {
    day1_F: Y, day2_F: S,
    day1_G: T, day2_G: R,
    day1_H: R, day2_H: T,
    day1_J: S, day2_J: Y,
}
opt_E = {
    day1_F: Y, day2_F: T,
    day1_G: S, day2_G: Y,
    day1_H: T, day2_H: R,
    day1_J: R, day2_J: S,
}

options = [
    ("A", option_constraint(opt_A)),
    ("B", option_constraint(opt_B)),
    ("C", option_constraint(opt_C)),
    ("D", option_constraint(opt_D)),
    ("E", option_constraint(opt_E)),
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