from z3 import *

solver = Solver()

# Students: 0=Louis, 1=Mollie, 2=Onyx, 3=Ryan, 4=Tiffany, 5=Yoshio
# Years: y1921, y1922, y1923, y1924 — each holds a student index (0-5)

y1921, y1922, y1923, y1924 = Ints('y1921 y1922 y1923 y1924')

# Each year gets exactly one student (0-5)
for y in [y1921, y1922, y1923, y1924]:
    solver.add(y >= 0, y <= 5)

# All four years have different students
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

# Constraint 4: If Ryan(3) is assigned, then Onyx(2) must be in the year immediately prior
# Ryan at 1922 -> Onyx at 1921
# Ryan at 1923 -> Onyx at 1922
# Ryan at 1924 -> Onyx at 1923
# (Ryan at 1921 is impossible — no prior year for Onyx)
solver.add(Implies(ryan_assigned,
    Or(
        And(y1922 == 3, y1921 == 2),
        And(y1923 == 3, y1922 == 2),
        And(y1924 == 3, y1923 == 2)
    )
))

# Now test each option: can student X be assigned to 1922?
# (A) Louis=0, (B) Mollie=1, (C) Onyx=2, (D) Ryan=3, (E) Yoshio=5

options = [
    ("A", y1922 == 0),  # Louis
    ("B", y1922 == 1),  # Mollie
    ("C", y1922 == 2),  # Onyx
    ("D", y1922 == 3),  # Ryan
    ("E", y1922 == 5),  # Yoshio
]

found_options = []
for letter, constr in options:
    solver.push()
    solver.add(constr)
    result = solver.check()
    if result == sat:
        m = solver.model()
        print(f"Option {letter} SAT: y1921={m[y1921]}, y1922={m[y1922]}, y1923={m[y1923]}, y1924={m[y1924]}")
        found_options.append(letter)
    else:
        print(f"Option {letter} UNSAT: student CANNOT be assigned to 1922")
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