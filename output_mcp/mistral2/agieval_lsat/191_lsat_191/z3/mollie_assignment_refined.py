from z3 import *

# Declare students and years as integers for easier handling
students = ['Louis', 'Mollie', 'Onyx', 'Ryan', 'Tiffany', 'Yoshio']
student_to_int = {s: i for i, s in enumerate(students)}
int_to_student = {i: s for i, s in enumerate(students)}

# Years as integers for easier handling
years = [1921, 1922, 1923, 1924]
year_to_int = {y: i for i, y in enumerate(years)}
int_to_year = {i: y for i, y in enumerate(years)}

# Create a solver
solver = Solver()

# Declare symbolic variables for year_to_student and student_to_year as Ints
# year_to_student[i] = student assigned to year i (0-3 for 1921-1924)
year_to_student = [Int(f'year_to_student_{i}') for i in range(len(years))]
# student_to_year[s] = year assigned to student s (0-3 for 1921-1924)
student_to_year = [Int(f'student_to_year_{s}') for s in range(len(students))]

# Constraint: Each year is assigned exactly one student
for i in range(len(years)):
    solver.add(year_to_student[i] >= 0, year_to_student[i] < len(students))

# Constraint: No two years have the same student
solver.add(Distinct(year_to_student))

# Constraint 1: Only Louis (0) or Tiffany (4) can be assigned to 1923 (year index 2)
solver.add(Or(year_to_student[2] == student_to_int['Louis'], 
              year_to_student[2] == student_to_int['Tiffany']))

# Constraint 2: If Mollie (1) is assigned, she must be assigned to 1921 (0) or 1922 (1)
solver.add(Implies(Or([year_to_student[i] == student_to_int['Mollie'] for i in range(len(years))]),
                  Or(student_to_year[student_to_int['Mollie']] == 0, 
                    student_to_year[student_to_int['Mollie']] == 1)))

# Constraint 3: If Tiffany (4) is assigned, Ryan (3) must also be assigned
solver.add(Implies(Or([year_to_student[i] == student_to_int['Tiffany'] for i in range(len(years))]),
                  Or([year_to_student[i] == student_to_int['Ryan'] for i in range(len(years))])))

# Constraint 4: If Ryan (3) is assigned, Onyx (2) must be assigned to the year immediately prior to Ryan's
for i in range(len(years)):
    if i > 0:
        solver.add(Implies(year_to_student[i] == student_to_int['Ryan'],
                          year_to_student[i-1] == student_to_int['Onyx']))

# Helper: Define student_to_year from year_to_student
for s in range(len(students)):
    solver.add(Or([And(year_to_student[i] == s, student_to_year[s] == i) for i in range(len(years))]))

# Now, evaluate each answer choice to see if it forces Mollie to be assigned to 1922 (year index 1).
found_options = []

# Choice A: Louis is assigned to 1924 (year index 3)
solver.push()
solver.add(year_to_student[3] == student_to_int['Louis'])
if solver.check() == sat:
    m = solver.model()
    mollie_year = m[student_to_year[student_to_int['Mollie']]]
    if mollie_year == 1:  # 1922
        found_options.append("A")
solver.pop()

# Choice B: Onyx is assigned to 1921 (year index 0)
solver.push()
solver.add(year_to_student[0] == student_to_int['Onyx'])
if solver.check() == sat:
    m = solver.model()
    mollie_year = m[student_to_year[student_to_int['Mollie']]]
    if mollie_year == 1:  # 1922
        found_options.append("B")
solver.pop()

# Choice C: Onyx is assigned to 1924 (year index 3)
solver.push()
solver.add(year_to_student[3] == student_to_int['Onyx'])
if solver.check() == sat:
    m = solver.model()
    mollie_year = m[student_to_year[student_to_int['Mollie']]]
    if mollie_year == 1:  # 1922
        found_options.append("C")
solver.pop()

# Choice D: Tiffany is assigned to 1923 (year index 2)
solver.push()
solver.add(year_to_student[2] == student_to_int['Tiffany'])
if solver.check() == sat:
    m = solver.model()
    mollie_year = m[student_to_year[student_to_int['Mollie']]]
    if mollie_year == 1:  # 1922
        found_options.append("D")
solver.pop()

# Choice E: Yoshio is assigned to 1921 (year index 0)
solver.push()
solver.add(year_to_student[0] == student_to_int['Yoshio'])
if solver.check() == sat:
    m = solver.model()
    mollie_year = m[student_to_year[student_to_int['Mollie']]]
    if mollie_year == 1:  # 1922
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