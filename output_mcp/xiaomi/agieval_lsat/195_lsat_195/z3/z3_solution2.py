from z3 import *

solver = Solver()

# Students: Louis=0, Mollie=1, Onyx=2, Ryan=3, Tiffany=4, Yoshio=5
# Years: 1921=0, 1922=1, 1923=2, 1924=3
# Each year gets exactly one student, 4 out of 6 students are chosen

# assigned[i] = year assigned to student i, or -1 if not assigned
assigned = [Int(f'assigned_{s}') for s in range(6)]
student_names = ['Louis', 'Mollie', 'Onyx', 'Ryan', 'Tiffany', 'Yoshio']

# Each student is either assigned to a year (0-3) or not assigned (-1)
for i in range(6):
    solver.add(Or(assigned[i] == -1, And(assigned[i] >= 0, assigned[i] <= 3)))

# Each year has exactly one student
for y in range(4):
    solver.add(Sum([If(assigned[i] == y, 1, 0) for i in range(6)]) == 1)

# Exactly 4 students are assigned (2 are not)
solver.add(Sum([If(assigned[i] == -1, 1, 0) for i in range(6)]) == 2)

# Condition 1: Only Louis or Tiffany can be assigned to 1923 (year 2)
for i in range(6):
    if i != 0 and i != 4:  # Not Louis and not Tiffany
        solver.add(assigned[i] != 2)

# Condition 2: If Mollie is assigned, she must be assigned to 1921 or 1922
solver.add(Implies(assigned[1] != -1, Or(assigned[1] == 0, assigned[1] == 1)))

# Condition 3: If Tiffany is assigned, then Ryan must be assigned
solver.add(Implies(assigned[4] != -1, assigned[3] != -1))

# Condition 4: If Ryan is assigned, then Onyx must be assigned to the year immediately prior
# "immediately prior" means Onyx's year = Ryan's year - 1
solver.add(Implies(assigned[3] != -1, And(assigned[2] != -1, assigned[2] == assigned[3] - 1)))

# The question asks which student CANNOT be assigned to 1922.
# We need to find the one student for whom assigned[X] == 1 is UNSATISFIABLE.
# From the first run, A (Louis) was the only one that couldn't be assigned to 1922.
# Let me verify by checking each option individually and printing details.

options = [
    ("A", 0, "Louis"),
    ("B", 1, "Mollie"),
    ("C", 2, "Onyx"),
    ("D", 3, "Ryan"),
    ("E", 5, "Yoshio"),
]

cannot_assign = []
can_assign = []

for letter, student_idx, name in options:
    solver.push()
    solver.add(assigned[student_idx] == 1)  # Force this student to be assigned to 1922
    result = solver.check()
    if result == sat:
        m = solver.model()
        print(f"Option {letter} ({name}) CAN be assigned to 1922. Model:")
        for i in range(6):
            print(f"  {student_names[i]}: year {m[assigned[i]]}")
        can_assign.append(letter)
    else:
        print(f"Option {letter} ({name}) CANNOT be assigned to 1922.")
        cannot_assign.append(letter)
    solver.pop()

print()
if len(cannot_assign) == 1:
    print("STATUS: sat")
    print(f"answer:{cannot_assign[0]}")
elif len(cannot_assign) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options cannot be assigned {cannot_assign}")
else:
    print("STATUS: unsat")
    print("Refine: All options can be assigned")