from z3 import *

solver = Solver()

# Students: 0=Louis, 1=Mollie, 2=Onyx, 3=Ryan, 4=Tiffany, 5=Yoshio
y1921, y1922, y1923, y1924 = Ints('y1921 y1922 y1923 y1924')

for y in [y1921, y1922, y1923, y1924]:
    solver.add(y >= 0, y <= 5)

solver.add(Distinct(y1921, y1922, y1923, y1924))

# Constraint 1: Only Louis(0) or Tiffany(4) can be assigned to 1923
solver.add(Or(y1923 == 0, y1923 == 4))

# Constraint 2: If Mollie(1) is assigned, she must be at 1921 or 1922
mollie_assigned = Or(y1921 == 1, y1922 == 1, y1923 == 1, y1924 == 1)
solver.add(Implies(mollie_assigned, Or(y1921 == 1, y1922 == 1)))

# Constraint 3: If Tiffany(4) is assigned, then Ryan(3) must be assigned
tiffany_assigned = Or(y1921 == 4, y1922 == 4, y1923 == 4, y1924 == 4)
ryan_assigned = Or(y1921 == 3, y1922 == 3, y1923 == 3, y1924 == 3)
solver.add(Implies(tiffany_assigned, ryan_assigned))

# Constraint 4: If Ryan(3) is assigned, Onyx(2) must be in the year immediately prior
solver.add(Implies(ryan_assigned,
    Or(
        And(y1922 == 3, y1921 == 2),
        And(y1923 == 3, y1922 == 2),
        And(y1924 == 3, y1923 == 2)
    )
))

# The question: which student CANNOT be assigned to 1922?
# A student CANNOT be assigned to 1922 if adding that constraint makes it UNSAT.
# We want the option letter where the constraint is UNSAT (i.e., the student cannot be at 1922).

options = [
    ("A", y1922 == 0),  # Louis
    ("B", y1922 == 1),  # Mollie
    ("C", y1922 == 2),  # Onyx
    ("D", y1922 == 3),  # Ryan
    ("E", y1922 == 5),  # Yoshio
]

cannot_options = []
can_options = []
for letter, constr in options:
    solver.push()
    solver.add(constr)
    result = solver.check()
    if result == sat:
        can_options.append(letter)
    else:
        cannot_options.append(letter)
    solver.pop()

# The answer is the student who CANNOT be assigned to 1922
if len(cannot_options) == 1:
    print("STATUS: sat")
    print(f"answer:{cannot_options[0]}")
elif len(cannot_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple CANNOT options found {cannot_options}")
else:
    print("STATUS: unsat")
    print("Refine: No CANNOT options found")