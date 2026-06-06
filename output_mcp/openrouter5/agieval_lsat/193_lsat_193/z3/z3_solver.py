from z3 import *

solver = Solver()

# Students: Louis, Mollie, Onyx, Ryan, Tiffany, Yoshio
# We need to assign each of the 4 years (1921, 1922, 1923, 1924) to exactly one student.
# But not all 6 students are necessarily assigned - only 4 are chosen.
# Let's model: for each student, we have a year they are assigned to (or 0 if not assigned).
# Actually, let's think differently: we have 4 slots (years 1921-1924).
# Each slot gets exactly one student from the 6 available.
# A student can be assigned to at most one year.

# Let's use Int variables for each year: the student assigned to that year.
# We'll encode students as integers 0..5
Louis, Mollie, Onyx, Ryan, Tiffany, Yoshio = 0, 1, 2, 3, 4, 5
student_names = ["Louis", "Mollie", "Onyx", "Ryan", "Tiffany", "Yoshio"]

y1921 = Int('y1921')
y1922 = Int('y1922')
y1923 = Int('y1923')
y1924 = Int('y1924')

years = [y1921, y1922, y1923, y1924]

# Each year gets a student from 0..5
for y in years:
    solver.add(y >= 0, y <= 5)

# Each student can be assigned to at most one year (Distinct)
solver.add(Distinct(years))

# Condition 1: Only Louis or Tiffany can be assigned to 1923.
solver.add(Or(y1923 == Louis, y1923 == Tiffany))

# Condition 2: If Mollie is assigned to the project, then she must be assigned to either 1921 or 1922.
# Mollie is assigned to the project iff Mollie is one of the years.
# So: If Mollie is in {y1921, y1922, y1923, y1924}, then Mollie is in {y1921, y1922}.
solver.add(Implies(
    Or([y == Mollie for y in years]),
    Or(y1921 == Mollie, y1922 == Mollie)
))

# Condition 3: If Tiffany is assigned to the project, then Ryan must be assigned to the project.
# If Tiffany is in {years}, then Ryan is in {years}.
solver.add(Implies(
    Or([y == Tiffany for y in years]),
    Or([y == Ryan for y in years])
))

# Condition 4: If Ryan is assigned to the project, then Onyx must be assigned to the year immediately prior to Ryan's.
# If Ryan is in {years}, then there exists a year y such that y == Ryan and (y-1) == Onyx.
# Since years are 1921,1922,1923,1924, we need to check the year index.
# Let's map: index 0 -> 1921, index 1 -> 1922, index 2 -> 1923, index 3 -> 1924
# So if Ryan is at index i (i>0), then Onyx must be at index i-1.
solver.add(Implies(
    Or([y == Ryan for y in years]),
    Or([
        And(y1922 == Ryan, y1921 == Onyx),
        And(y1923 == Ryan, y1922 == Onyx),
        And(y1924 == Ryan, y1923 == Onyx)
    ])
))

# Now we need to count how many students COULD be assigned to 1921.
# We'll check each student individually.

possible_students = []
for s in [Louis, Mollie, Onyx, Ryan, Tiffany, Yoshio]:
    solver.push()
    solver.add(y1921 == s)
    if solver.check() == sat:
        possible_students.append(student_names[s])
    solver.pop()

print(f"Possible students for 1921: {possible_students}")
count = len(possible_students)

# Map count to answer choices
# (A)six (B)five (C)four (D)three (E)two
answer_map = {6: "A", 5: "B", 4: "C", 3: "D", 2: "E"}

found_options = []
for letter, expected_count in [("A", 6), ("B", 5), ("C", 4), ("D", 3), ("E", 2)]:
    solver.push()
    solver.add(count == expected_count)
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