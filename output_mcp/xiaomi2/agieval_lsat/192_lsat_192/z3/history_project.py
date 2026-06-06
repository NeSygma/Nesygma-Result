from z3 import *

solver = Solver()

# Students: 0=Louis, 1=Mollie, 2=Onyx, 3=Ryan, 4=Tiffany, 5=Yoshio
# Years: 0=1921, 1=1922, 2=1923, 3=1924
# assignment[i] = year assigned to student i, or -1 if not assigned
students = ['Louis', 'Mollie', 'Onyx', 'Ryan', 'Tiffany', 'Yoshio']
years = [1921, 1922, 1923, 1924]

assign = [Int(f'assign_{s}') for s in students]

# Each student is assigned to a year 0-3 or -1 (not assigned)
for i in range(6):
    solver.add(Or(assign[i] == -1, assign[i] == 0, assign[i] == 1, assign[i] == 2, assign[i] == 3))

# Exactly 4 students are assigned (each year has exactly one student)
# Each year 0-3 must have exactly one student
for y in range(4):
    # At least one student assigned to year y
    solver.add(Or([assign[i] == y for i in range(6)]))
    # At most one student assigned to year y
    for i in range(6):
        for j in range(i+1, 6):
            solver.add(Implies(And(assign[i] == y, assign[j] == y), False))

# Exactly 4 students assigned means exactly 2 are not assigned
solver.add(Sum([If(assign[i] != -1, 1, 0) for i in range(6)]) == 4)

# Condition 1: Only Louis (0) or Tiffany (4) can be assigned to 1923 (year 2)
for i in range(6):
    if i != 0 and i != 4:  # Not Louis and not Tiffany
        solver.add(assign[i] != 2)

# Condition 2: If Mollie (1) is assigned, she must be at 1921 (0) or 1922 (1)
solver.add(Implies(assign[1] != -1, Or(assign[1] == 0, assign[1] == 1)))

# Condition 3: If Tiffany (4) is assigned, Ryan (3) must be assigned
solver.add(Implies(assign[4] != -1, assign[3] != -1))

# Condition 4: If Ryan (3) is assigned, Onyx (2) must be assigned to year immediately prior
# "immediately prior" means Onyx's year = Ryan's year - 1
solver.add(Implies(assign[3] != -1, And(assign[2] != -1, assign[2] == assign[3] - 1)))

# GIVEN: Both Ryan and Yoshio are assigned
solver.add(assign[3] != -1)  # Ryan assigned
solver.add(assign[5] != -1)  # Yoshio assigned

# Now check each option
found_options = []

# (A) Louis is assigned to 1923
solver.push()
solver.add(assign[0] == 2)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# (B) Mollie is assigned to 1921
solver.push()
solver.add(assign[1] == 0)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# (C) Onyx is assigned to 1922
solver.push()
solver.add(assign[2] == 1)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# (D) Tiffany is assigned to 1924
solver.push()
solver.add(assign[4] == 3)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# (E) Yoshio is assigned to 1922
solver.push()
solver.add(assign[5] == 1)
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

# Also print the valid assignments for verification
print("\n--- Verification: All valid assignments ---")
count = 0
while solver.check() == sat:
    m = solver.model()
    count += 1
    print(f"Solution {count}:")
    for i in range(6):
        val = m[assign[i]]
        if val.as_long() == -1:
            print(f"  {students[i]}: not assigned")
        else:
            print(f"  {students[i]}: {years[val.as_long()]}")
    solver.add(Or([assign[i] != m[assign[i]] for i in range(6)]))
print(f"Total valid assignments: {count}")