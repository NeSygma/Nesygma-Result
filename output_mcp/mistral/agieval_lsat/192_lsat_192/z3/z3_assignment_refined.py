from z3 import *

# Declare the years and students
Years = [1921, 1922, 1923, 1924]
Students = ["Louis", "Mollie", "Onyx", "Ryan", "Tiffany", "Yoshio"]

# Create a solver
solver = Solver()

# Assignments: assignment[year] = student assigned to that year
assignment = {year: Int(f"assignment_{year}") for year in Years}

# Each year has exactly one student
for year in Years:
    solver.add(assignment[year] >= 0, assignment[year] < len(Students))

# All four years must be assigned to distinct students
solver.add(Distinct([assignment[y] for y in Years]))

# Only Louis or Tiffany can be assigned to 1923
solver.add(Or(assignment[1923] == Students.index("Louis"), assignment[1923] == Students.index("Tiffany")))

# If Mollie is assigned, she must be assigned to either 1921 or 1922
solver.add(Or(
    assignment[1921] == Students.index("Mollie"),
    assignment[1922] == Students.index("Mollie"),
    Not(Or([assignment[y] == Students.index("Mollie") for y in Years]))
))

# If Tiffany is assigned, Ryan must be assigned
solver.add(Or(
    Not(Or([assignment[y] == Students.index("Tiffany") for y in Years])),
    Or([assignment[y] == Students.index("Ryan") for y in Years])
))

# If Ryan is assigned, Onyx must be assigned to the year immediately prior to Ryan's
for year in Years:
    if year > 1921:
        solver.add(Implies(
            assignment[year] == Students.index("Ryan"),
            assignment[year - 1] == Students.index("Onyx")
        ))

# Base condition: Both Ryan and Yoshio are assigned to the project
solver.add(Or([assignment[y] == Students.index("Ryan") for y in Years]))
solver.add(Or([assignment[y] == Students.index("Yoshio") for y in Years]))

# Now evaluate each option
found_options = []

# Option A: Louis is assigned to 1923
solver.push()
solver.add(assignment[1923] == Students.index("Louis"))
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: Mollie is assigned to 1921
solver.push()
solver.add(assignment[1921] == Students.index("Mollie"))
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: Onyx is assigned to 1922
solver.push()
solver.add(assignment[1922] == Students.index("Onyx"))
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: Tiffany is assigned to 1924
solver.push()
solver.add(assignment[1924] == Students.index("Tiffany"))
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: Yoshio is assigned to 1922
solver.push()
solver.add(assignment[1922] == Students.index("Yoshio"))
if solver.check() == sat:
    found_options.append("E")
solver.pop()

# Output the result
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")