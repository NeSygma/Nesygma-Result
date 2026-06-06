from z3 import *

# Students and years
students = ["Louis", "Mollie", "Onyx", "Ryan", "Tiffany", "Yoshio"]
years = [1921, 1922, 1923, 1924]

# Create assignment variables: assign[student] = year
# Each student can be assigned to at most one year (or not assigned)
assign = {s: Int(f"assign_{s}") for s in students}

solver = Solver()

# Each student is assigned to at most one year (0 means not assigned)
for s in students:
    solver.add(Or([assign[s] == y for y in years] + [assign[s] == 0]))

# Each year has exactly one student assigned
for y in years:
    solver.add(Or([assign[s] == y for s in students]))

# Constraint 1: Only Louis or Tiffany can be assigned to 1923
solver.add(Or(assign["Louis"] == 1923, assign["Tiffany"] == 1923))

# Constraint 2: If Mollie is assigned, she must be assigned to 1921 or 1922
solver.add(Implies(assign["Mollie"] != 0, Or(assign["Mollie"] == 1921, assign["Mollie"] == 1922)))

# Constraint 3: If Tiffany is assigned, then Ryan must be assigned
solver.add(Implies(assign["Tiffany"] != 0, assign["Ryan"] != 0))

# Constraint 4: If Ryan is assigned, then Onyx must be assigned to the year immediately prior to Ryan's
# This means: if Ryan is assigned to year Y, then Onyx must be assigned to Y-1
for y in years:
    if y > 1921:  # Only years after 1921 have a prior year
        solver.add(Implies(assign["Ryan"] == y, assign["Onyx"] == y-1))

# Additional constraint: exactly 4 students are assigned (since 4 years)
# Count assigned students
assigned_count = Sum([If(assign[s] != 0, 1, 0) for s in students])
solver.add(assigned_count == 4)

# Now, for each student, check if they can be assigned to 1921
students_who_can_be_in_1921 = []

for student in students:
    solver.push()
    solver.add(assign[student] == 1921)
    if solver.check() == sat:
        students_who_can_be_in_1921.append(student)
    solver.pop()

# Count how many distinct students can be in 1921
count = len(students_who_can_be_in_1921)

print(f"Students who can be assigned to 1921: {students_who_can_be_in_1921}")
print(f"Count: {count}")

# Now match to answer choices
# Answer choices: (A)six (B)five (C)four (D)three (E)two
# We need to find which choice matches the count

# Create options based on count
opt_a = (count == 6)
opt_b = (count == 5)
opt_c = (count == 4)
opt_d = (count == 3)
opt_e = (count == 2)

# Use the exact skeleton for multiple choice evaluation
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