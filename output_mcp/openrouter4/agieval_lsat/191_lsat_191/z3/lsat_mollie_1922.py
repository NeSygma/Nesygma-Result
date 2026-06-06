from z3 import *

solver = Solver()

# Students: 0=Louis, 1=Mollie, 2=Onyx, 3=Ryan, 4=Tiffany, 5=Yoshio
# Year: 0=not assigned, 1=1921, 2=1922, 3=1923, 4=1924
students = [Int(f'student_{i}') for i in range(6)]
names = ['Louis', 'Mollie', 'Onyx', 'Ryan', 'Tiffany', 'Yoshio']

# Domain: each student assigned to 0 (none), 1, 2, 3, or 4
for s in students:
    solver.add(s >= 0, s <= 4)

# Exactly one student per year (1-4)
for y in range(1, 5):
    solver.add(Sum([If(s == y, 1, 0) for s in students]) == 1)

# Exactly 2 students not assigned (since 4 are assigned out of 6)
solver.add(Sum([If(s == 0, 1, 0) for s in students]) == 2)

# Condition 1: Only Louis or Tiffany can be assigned to 1923
# Since exactly one student is assigned to each year, either Louis or Tiffany must be in 1923
solver.add(Or(students[0] == 3, students[4] == 3))

# Condition 2: If Mollie is assigned, she must be 1921 or 1922
solver.add(Implies(students[1] != 0, Or(students[1] == 1, students[1] == 2)))

# Condition 3: If Tiffany is assigned, Ryan must be assigned
solver.add(Implies(students[4] != 0, students[3] != 0))

# Condition 4: If Ryan is assigned, Onyx must be assigned to the year immediately prior
solver.add(Implies(students[3] != 0, And(students[2] != 0, students[2] == students[3] - 1)))

# Options:
# (A) Louis is assigned to 1924: students[0] == 4
# (B) Onyx is assigned to 1921: students[2] == 1
# (C) Onyx is assigned to 1924: students[2] == 4
# (D) Tiffany is assigned to 1923: students[4] == 3
# (E) Yoshio is assigned to 1921: students[5] == 1

options = [
    ("A", students[0] == 4),
    ("B", students[2] == 1),
    ("C", students[2] == 4),
    ("D", students[4] == 3),
    ("E", students[5] == 1)
]

found_options = []
for letter, constr in options:
    solver.push()
    solver.add(constr)
    # Check if Mollie NOT in 1922 is possible
    # If unsat, then Mollie must be in 1922 under this option
    solver.push()
    solver.add(students[1] != 2)  # Mollie not in 1922
    result = solver.check()
    if result == unsat:
        # Mollie must be in 1922 under this option
        found_options.append(letter)
    solver.pop()
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