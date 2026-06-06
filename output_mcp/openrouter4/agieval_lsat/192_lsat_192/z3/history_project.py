from z3 import *

solver = Solver()

# Years: 1=1921, 2=1922, 3=1923, 4=1924
# 0 means not assigned

Louis, Mollie, Onyx, Ryan, Tiffany, Yoshio = Ints('Louis Mollie Onyx Ryan Tiffany Yoshio')
students = [Louis, Mollie, Onyx, Ryan, Tiffany, Yoshio]
names = ['Louis', 'Mollie', 'Onyx', 'Ryan', 'Tiffany', 'Yoshio']

# Domain: each student is either not assigned (0) or assigned to year 1-4
for s in students:
    solver.add(And(s >= 0, s <= 4))

# Each year value (1-4) appears exactly once among assigned students
for year in range(1, 5):
    solver.add(Sum([If(s == year, 1, 0) for s in students]) == 1)

# Exactly 4 students are assigned (0 appears twice)
solver.add(Sum([If(s == 0, 1, 0) for s in students]) == 2)

# Condition 1: Only Louis or Tiffany can be assigned to 1923 (year 3)
# Year 3 must be assigned to either Louis or Tiffany
solver.add(Or(Louis == 3, Tiffany == 3))

# Condition 2: If Mollie is assigned, then she must be assigned to either 1921 or 1922
solver.add(Implies(Mollie != 0, Or(Mollie == 1, Mollie == 2)))

# Condition 3: If Tiffany is assigned, then Ryan must be assigned
solver.add(Implies(Tiffany != 0, Ryan != 0))

# Condition 4: If Ryan is assigned, then Onyx must be assigned to the year immediately prior to Ryan's
solver.add(Implies(Ryan != 0, And(Onyx != 0, Onyx + 1 == Ryan)))

# Condition from the query: Both Ryan and Yoshio are assigned
solver.add(Ryan != 0)
solver.add(Yoshio != 0)

# Now check each option
found_options = []

# A: Louis is assigned to 1923 (year 3)
opt_a = (Louis == 3)

# B: Mollie is assigned to 1921 (year 1)
opt_b = (Mollie == 1)

# C: Onyx is assigned to 1922 (year 2)
opt_c = (Onyx == 2)

# D: Tiffany is assigned to 1924 (year 4)
opt_d = (Tiffany == 4)

# E: Yoshio is assigned to 1922 (year 2)
opt_e = (Yoshio == 2)

options = [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]

for letter, constr in options:
    solver.push()
    solver.add(constr)
    result = solver.check()
    if result == sat:
        found_options.append(letter)
        print(f"Option {letter}: SAT")
        m = solver.model()
        for s_name, s_var in zip(names, students):
            print(f"  {s_name} = {m.eval(s_var)}")
    else:
        print(f"Option {letter}: UNSAT")
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