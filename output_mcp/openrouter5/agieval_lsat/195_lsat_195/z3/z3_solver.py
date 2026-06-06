from z3 import *

solver = Solver()

# Students: Louis, Mollie, Onyx, Ryan, Tiffany, Yoshio
# Years: 1921 (1), 1922 (2), 1923 (3), 1924 (4)
# Each year gets exactly one student assigned.
# Not all students must be assigned; only 4 of the 6 are assigned.

Louis = Int('Louis')
Mollie = Int('Mollie')
Onyx = Int('Onyx')
Ryan = Int('Ryan')
Tiffany = Int('Tiffany')
Yoshio = Int('Yoshio')

students = [Louis, Mollie, Onyx, Ryan, Tiffany, Yoshio]

# Domain: each student is either 0 (not assigned) or 1..4 (year assigned)
for s in students:
    solver.add(Or(s == 0, And(s >= 1, s <= 4)))

# Exactly 4 students are assigned (one per year)
solver.add(Sum([If(s != 0, 1, 0) for s in students]) == 4)

# Each year 1..4 has exactly one student assigned
for yr in range(1, 5):
    solver.add(Sum([If(s == yr, 1, 0) for s in students]) == 1)

# Condition 1: Only Louis or Tiffany can be assigned to 1923.
# So if someone is assigned to 1923, it must be Louis or Tiffany.
# For any student s that is not Louis and not Tiffany, s != 3.
solver.add(And([s != 3 for s in students if s not in [Louis, Tiffany]]))

# Condition 2: If Mollie is assigned to the project, then she must be assigned to either 1921 or 1922.
solver.add(Implies(Mollie != 0, Or(Mollie == 1, Mollie == 2)))

# Condition 3: If Tiffany is assigned to the project, then Ryan must be assigned to the project.
solver.add(Implies(Tiffany != 0, Ryan != 0))

# Condition 4: If Ryan is assigned to the project, then Onyx must be assigned to the year immediately prior to Ryan's.
solver.add(Implies(Ryan != 0, And(Onyx != 0, Onyx == Ryan - 1)))

# Let's first check if the base constraints are satisfiable
print("Base check:", solver.check())
if solver.check() == sat:
    m = solver.model()
    for s in students:
        print(f"  {s} = {m[s]}")

# Now evaluate each option: which student CANNOT be assigned to 1922?
# The question asks: which student CANNOT be assigned to 1922?
# So we need to find the option that is UNSAT (impossible).

options = [
    ("A", Louis == 2),
    ("B", Mollie == 2),
    ("C", Onyx == 2),
    ("D", Ryan == 2),
    ("E", Yoshio == 2)
]

found_options = []
for letter, constr in options:
    solver.push()
    solver.add(constr)
    res = solver.check()
    print(f"Option {letter} (student assigned to 1922): {res}")
    if res == sat:
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