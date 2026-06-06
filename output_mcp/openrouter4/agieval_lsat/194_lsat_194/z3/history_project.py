from z3 import *

solver = Solver()

# Students: 0=Louis, 1=Mollie, 2=Onyx, 3=Ryan, 4=Tiffany, 5=Yoshio
# Years: 1=1921, 2=1922, 3=1923, 4=1924, 0=not assigned
year = [Int(f'year_{i}') for i in range(6)]

# Domain: each year_i is between 0 and 4
for i in range(6):
    solver.add(And(year[i] >= 0, year[i] <= 4))

# Each year (1..4) has exactly one student assigned
for y in [1, 2, 3, 4]:
    solver.add(Sum([If(year[i] == y, 1, 0) for i in range(6)]) == 1)

# Exactly 4 students assigned (year != 0)
solver.add(Sum([If(year[i] != 0, 1, 0) for i in range(6)]) == 4)

# Constraint 1: Only Louis or Tiffany can be assigned to 1923
# The student for year 3 is either Louis (0) or Tiffany (4)
solver.add(Or(year[0] == 3, year[4] == 3))

# Constraint 2: If Mollie (1) is assigned, she must be 1921 or 1922
solver.add(Implies(year[1] != 0, Or(year[1] == 1, year[1] == 2)))

# Constraint 3: If Tiffany (4) is assigned, then Ryan (3) must be assigned
solver.add(Implies(year[4] != 0, year[3] != 0))

# Constraint 4: If Ryan (3) is assigned, then Onyx (2) must be the year immediately prior
solver.add(Implies(year[3] != 0, year[2] == year[3] - 1))

# Given: Yoshio is not assigned
solver.add(year[5] == 0)

# Now test the options
# Option A: Louis is not assigned -> year[0] == 0
# Option B: Ryan is not assigned -> year[3] == 0
# Option C: Tiffany is not assigned -> year[4] == 0
# Option D: Onyx is assigned to 1922 -> year[2] == 2
# Option E: Louis is assigned to 1924 -> year[0] == 4

found_options = []

# Option A
solver.push()
solver.add(year[0] == 0)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B
solver.push()
solver.add(year[3] == 0)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C
solver.push()
solver.add(year[4] == 0)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D
solver.push()
solver.add(year[2] == 2)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E
solver.push()
solver.add(year[0] == 4)
if solver.check() == sat:
    found_options.append("E")
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