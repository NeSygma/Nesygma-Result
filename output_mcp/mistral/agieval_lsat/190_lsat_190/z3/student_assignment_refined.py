from z3 import *

# Base constraints solver
solver = Solver()

# Years: 1921, 1922, 1923, 1924 (indices 0, 1, 2, 3)
years = 4
students = ['Louis', 'Mollie', 'Onyx', 'Ryan', 'Tiffany', 'Yoshio']
student_indices = {s: i for i, s in enumerate(students)}

# Assignments: year -> student index
assignments = [Int(f"year_{i}") for i in range(years)]

# Each year must be assigned exactly one student
for i in range(years):
    solver.add(assignments[i] >= 0, assignments[i] < len(students))

# Constraint 1: Only Louis or Tiffany can be assigned to 1923 (year index 2)
solver.add(Or(assignments[2] == student_indices['Louis'], assignments[2] == student_indices['Tiffany']))

# Now evaluate each multiple-choice option
found_options = []

# Option A: Louis, Onyx, Ryan, Yoshio
solver.push()
solver.add(And(
    assignments[0] == student_indices['Louis'],
    assignments[1] == student_indices['Onyx'],
    assignments[2] == student_indices['Ryan'],
    assignments[3] == student_indices['Yoshio']
))
# Constraint 3: If Tiffany is assigned, Ryan must be assigned
# Tiffany is not in this option, so no need to add this constraint
# Constraint 4: If Ryan is assigned, Onyx must be assigned to the year immediately prior
# Ryan is assigned to year 2 (1923), so year 1 (1922) must be Onyx
# This is already satisfied by the option's assignment
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: Mollie, Yoshio, Tiffany, Onyx
solver.push()
solver.add(And(
    assignments[0] == student_indices['Mollie'],
    assignments[1] == student_indices['Yoshio'],
    assignments[2] == student_indices['Tiffany'],
    assignments[3] == student_indices['Onyx']
))
# Constraint 3: If Tiffany is assigned, Ryan must be assigned
solver.add(Or([assignments[i] == student_indices['Ryan'] for i in range(years)]))
# Constraint 4: If Ryan is assigned, Onyx must be assigned to the year immediately prior
# Ryan is not assigned in this option, so no need to add this constraint
# Constraint 2: If Mollie is assigned, she must be in 1921 or 1922
# Already satisfied by the option's assignment
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: Onyx, Ryan, Louis, Tiffany
solver.push()
solver.add(And(
    assignments[0] == student_indices['Onyx'],
    assignments[1] == student_indices['Ryan'],
    assignments[2] == student_indices['Louis'],
    assignments[3] == student_indices['Tiffany']
))
# Constraint 3: If Tiffany is assigned, Ryan must be assigned
solver.add(Or([assignments[i] == student_indices['Ryan'] for i in range(years)]))
# Constraint 4: If Ryan is assigned, Onyx must be assigned to the year immediately prior
# Ryan is assigned to year 1 (1922), so year 0 (1921) must be Onyx
# This is already satisfied by the option's assignment
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: Tiffany, Onyx, Louis, Ryan
solver.push()
solver.add(And(
    assignments[0] == student_indices['Tiffany'],
    assignments[1] == student_indices['Onyx'],
    assignments[2] == student_indices['Louis'],
    assignments[3] == student_indices['Ryan']
))
# Constraint 3: If Tiffany is assigned, Ryan must be assigned
solver.add(Or([assignments[i] == student_indices['Ryan'] for i in range(years)]))
# Constraint 4: If Ryan is assigned, Onyx must be assigned to the year immediately prior
# Ryan is assigned to year 3 (1924), so year 2 (1923) must be Onyx
# But year 2 is Louis in this option, so this constraint is violated
solver.add(assignments[2] == student_indices['Onyx'])
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: Yoshio, Onyx, Louis, Mollie
solver.push()
solver.add(And(
    assignments[0] == student_indices['Yoshio'],
    assignments[1] == student_indices['Onyx'],
    assignments[2] == student_indices['Louis'],
    assignments[3] == student_indices['Mollie']
))
# Constraint 3: If Tiffany is assigned, Ryan must be assigned
# Tiffany is not in this option, so no need to add this constraint
# Constraint 2: If Mollie is assigned, she must be in 1921 or 1922
# Mollie is assigned to year 3 (1924), so this constraint is violated
solver.add(Or(
    assignments[0] == student_indices['Mollie'],
    assignments[1] == student_indices['Mollie']
))
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