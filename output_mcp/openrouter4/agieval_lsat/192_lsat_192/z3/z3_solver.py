from z3 import *

Louis, Mollie, Onyx, Ryan, Tiffany, Yoshio = 0, 1, 2, 3, 4, 5
students = ["Louis", "Mollie", "Onyx", "Ryan", "Tiffany", "Yoshio"]
N = 6

assign = [Int(f"assign_{s}") for s in range(N)]

solver = Solver()

# Domain: 0 (not assigned) or 1..4 (years)
for s in range(N):
    solver.add(Or(assign[s] == 0, And(1 <= assign[s], assign[s] <= 4)))

# Exactly 4 students assigned (non-zero)
solver.add(Sum([If(assign[s] != 0, 1, 0) for s in range(N)]) == 4)

# Each year 1..4 has exactly one student assigned
for y in range(1, 5):
    solver.add(Sum([If(assign[s] == y, 1, 0) for s in range(N)]) == 1)

# Condition 1: Only Louis or Tiffany can be assigned to 1923 (year 3)
for s in range(N):
    if s != Louis and s != Tiffany:
        solver.add(assign[s] != 3)

# Condition 2: If Mollie is assigned, then she must be assigned to either 1921 or 1922
solver.add(Implies(assign[Mollie] != 0, Or(assign[Mollie] == 1, assign[Mollie] == 2)))

# Condition 3: If Tiffany is assigned, then Ryan must be assigned
solver.add(Implies(assign[Tiffany] != 0, assign[Ryan] != 0))

# Condition 4: If Ryan is assigned, then Onyx must be assigned to the year immediately prior to Ryan's
solver.add(Implies(assign[Ryan] != 0, And(assign[Onyx] != 0, assign[Onyx] == assign[Ryan] - 1)))

# Given: Both Ryan and Yoshio are assigned to the project
solver.add(assign[Ryan] != 0)
solver.add(assign[Yoshio] != 0)

# Now check each option
found_options = []

# (A) Louis is assigned to 1923.
opt_a = (assign[Louis] == 3)
solver.push()
solver.add(opt_a)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# (B) Mollie is assigned to 1921.
opt_b = (assign[Mollie] == 1)
solver.push()
solver.add(opt_b)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# (C) Onyx is assigned to 1922.
opt_c = (assign[Onyx] == 2)
solver.push()
solver.add(opt_c)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# (D) Tiffany is assigned to 1924.
opt_d = (assign[Tiffany] == 4)
solver.push()
solver.add(opt_d)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# (E) Yoshio is assigned to 1922.
opt_e = (assign[Yoshio] == 2)
solver.push()
solver.add(opt_e)
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