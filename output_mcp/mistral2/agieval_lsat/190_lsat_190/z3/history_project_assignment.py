from z3 import *

solver = Solver()

# Years to assign
Years = [1921, 1922, 1923, 1924]

# Students
Students = ["Louis", "Mollie", "Onyx", "Ryan", "Tiffany", "Yoshio"]

# Assignments: year -> student
assignment = {year: Int(f"assignment_{year}") for year in Years}

# Each year must be assigned exactly one student
for year in Years:
    solver.add(assignment[year] >= 0, assignment[year] < len(Students))

# Each student can be assigned to at most one year
for s1 in Students:
    for s2 in Students:
        if s1 != s2:
            for year in Years:
                solver.add(Or(assignment[year] != Students.index(s1), 
                              assignment[year] != Students.index(s2)))
    # Actually, the above is incorrect. Instead, we should ensure that no two years have the same student.
    # Let's correct this by ensuring all assignments are distinct.

# Correct distinctness constraint: all assignments must be distinct
solver.add(Distinct([assignment[year] for year in Years]))

# Only Louis or Tiffany can be assigned to 1923
solver.add(Or(assignment[1923] == Students.index("Louis"), 
              assignment[1923] == Students.index("Tiffany")))

# If Mollie is assigned, she must be assigned to 1921 or 1922
solver.add(Implies(Or([assignment[year] == Students.index("Mollie") for year in Years]),
                   Or(assignment[1921] == Students.index("Mollie"),
                      assignment[1922] == Students.index("Mollie"))))

# If Tiffany is assigned, then Ryan must be assigned
solver.add(Implies(Or([assignment[year] == Students.index("Tiffany") for year in Years]),
                   Or([assignment[year] == Students.index("Ryan") for year in Years])))

# If Ryan is assigned, then Onyx must be assigned to the year immediately prior to Ryan's
# We need to find Ryan's year and ensure Onyx is assigned to the previous year
# This is a bit tricky because we need to relate the assignments symbolically.
# We can use a helper function or a loop to enforce this.

# Let's define a helper function to get the year before a given year
for year in Years:
    if year > 1921:
        solver.add(Implies(assignment[year] == Students.index("Ryan"),
                           assignment[year - 1] == Students.index("Onyx")))

# Now, evaluate each option
found_options = []

# Option A: Louis, Onyx, Ryan, Yoshio
solver.push()
solver.add(assignment[1921] == Students.index("Louis"))
solver.add(assignment[1922] == Students.index("Onyx"))
solver.add(assignment[1923] == Students.index("Ryan"))
solver.add(assignment[1924] == Students.index("Yoshio"))
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: Mollie, Yoshio, Tiffany, Onyx
solver.push()
solver.add(assignment[1921] == Students.index("Mollie"))
solver.add(assignment[1922] == Students.index("Yoshio"))
solver.add(assignment[1923] == Students.index("Tiffany"))
solver.add(assignment[1924] == Students.index("Onyx"))
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: Onyx, Ryan, Louis, Tiffany
solver.push()
solver.add(assignment[1921] == Students.index("Onyx"))
solver.add(assignment[1922] == Students.index("Ryan"))
solver.add(assignment[1923] == Students.index("Louis"))
solver.add(assignment[1924] == Students.index("Tiffany"))
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: Tiffany, Onyx, Louis, Ryan
solver.push()
solver.add(assignment[1921] == Students.index("Tiffany"))
solver.add(assignment[1922] == Students.index("Onyx"))
solver.add(assignment[1923] == Students.index("Louis"))
solver.add(assignment[1924] == Students.index("Ryan"))
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: Yoshio, Onyx, Louis, Mollie
solver.push()
solver.add(assignment[1921] == Students.index("Yoshio"))
solver.add(assignment[1922] == Students.index("Onyx"))
solver.add(assignment[1923] == Students.index("Louis"))
solver.add(assignment[1924] == Students.index("Mollie"))
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