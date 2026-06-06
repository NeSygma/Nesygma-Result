from z3 import *

solver = Solver()

# Students: Louis=0, Mollie=1, Onyx=2, Ryan=3, Tiffany=4, Yoshio=5
# Years: 1921=0, 1922=1, 1923=2, 1924=3
# assignment[i] = year assigned to student i, or -1 if not assigned
students = ['Louis', 'Mollie', 'Onyx', 'Ryan', 'Tiffany', 'Yoshio']
years = [1921, 1922, 1923, 1924]

assign = [Int(f'assign_{s}') for s in students]
# Each assigned student gets a year 0-3, unassigned gets -1
for a in assign:
    solver.add(Or(a == -1, a == 0, a == 1, a == 2, a == 3))

# Exactly 4 students are assigned (each year has exactly one student)
# So exactly 4 of the 6 students are assigned, and the 4 assigned get distinct years
solver.add(Sum([If(a != -1, 1, 0) for a in assign]) == 4)

# Each year has exactly one student
for y in range(4):
    solver.add(Sum([If(a == y, 1, 0) for a in assign]) == 1)

# Condition 1: Only Louis or Tiffany can be assigned to 1923 (year 2)
for i in range(6):
    if i != 0 and i != 4:  # not Louis and not Tiffany
        solver.add(assign[i] != 2)

# Condition 2: If Mollie is assigned, she must be assigned to 1921 or 1922
solver.add(Implies(assign[1] != -1, Or(assign[1] == 0, assign[1] == 1)))

# Condition 3: If Tiffany is assigned, then Ryan must be assigned
solver.add(Implies(assign[4] != -1, assign[3] != -1))

# Condition 4: If Ryan is assigned, then Onyx must be assigned to the year immediately prior to Ryan's
# "immediately prior" means Ryan's year = Onyx's year + 1
solver.add(Implies(assign[3] != -1, And(assign[2] != -1, assign[3] == assign[2] + 1)))

# Given: Both Ryan and Yoshio are assigned to the project
solver.add(assign[3] != -1)  # Ryan assigned
solver.add(assign[5] != -1)  # Yoshio assigned

# Now evaluate each option
opt_a = (assign[0] == 2)  # Louis is assigned to 1923
opt_b = (assign[1] == 0)  # Mollie is assigned to 1921
opt_c = (assign[2] == 1)  # Onyx is assigned to 1922
opt_d = (assign[4] == 3)  # Tiffany is assigned to 1924
opt_e = (assign[5] == 1)  # Yoshio is assigned to 1922

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