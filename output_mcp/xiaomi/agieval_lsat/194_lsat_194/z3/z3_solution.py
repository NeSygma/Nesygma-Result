from z3 import *

solver = Solver()

# Define the years: 1921=0, 1922=1, 1923=2, 1924=3
# Define students: Louis=0, Mollie=1, Onyx=2, Ryan=3, Tiffany=4, Yoshio=5

# assigned[s] = True if student s is assigned to the project
assigned = [Bool(f'assigned_{s}') for s in range(6)]
names = ['Louis', 'Mollie', 'Onyx', 'Ryan', 'Tiffany', 'Yoshio']

# year[s] = which year (0-3) student s is assigned to (only meaningful if assigned)
year = [Int(f'year_{s}') for s in range(6)]

# Exactly 4 students are assigned
solver.add(Sum([If(assigned[s], 1, 0) for s in range(6)]) == 4)

# Each assigned student gets a year in {0,1,2,3}
for s in range(6):
    solver.add(Implies(assigned[s], And(year[s] >= 0, year[s] <= 3)))

# Each year has exactly one student assigned
for y in range(4):
    solver.add(Sum([If(And(assigned[s], year[s] == y), 1, 0) for s in range(6)]) == 1)

# Yoshio is NOT assigned (given condition)
solver.add(Not(assigned[5]))

# Condition 1: Only Louis or Tiffany can be assigned to 1923 (year=2)
for s in range(6):
    if s != 0 and s != 4:  # not Louis and not Tiffany
        solver.add(Implies(assigned[s], year[s] != 2))

# Condition 2: If Mollie is assigned, she must be assigned to 1921 or 1922
solver.add(Implies(assigned[1], Or(year[1] == 0, year[1] == 1)))

# Condition 3: If Tiffany is assigned, then Ryan must be assigned
solver.add(Implies(assigned[4], assigned[3]))

# Condition 4: If Ryan is assigned, then Onyx must be assigned to the year immediately prior to Ryan's
solver.add(Implies(assigned[3], And(assigned[2], year[2] == year[3] - 1)))

# Now evaluate each option
# (A) Louis is not assigned to the project.
opt_a = Not(assigned[0])

# (B) Ryan is not assigned to the project.
opt_b = Not(assigned[3])

# (C) Tiffany is not assigned to the project.
opt_c = Not(assigned[4])

# (D) Onyx is assigned to 1922.
opt_d = And(assigned[2], year[2] == 1)

# (E) Louis is assigned to 1924.
opt_e = And(assigned[0], year[0] == 3)

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