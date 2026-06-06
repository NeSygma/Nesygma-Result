from z3 import *

# BENCHMARK_MODE: OFF (since unsat is a valid result for counting)
BENCHMARK_MODE = False

# Declare students and years
students = ['Louis', 'Mollie', 'Onyx', 'Ryan', 'Tiffany', 'Yoshio']
years = [1921, 1922, 1923, 1924]

# Assignments: student -> year
assign = {s: Int(f'assign_{s}') for s in students}

# Year assignments: year -> student index
year_assign = {y: Int(f'year_assign_{y}') for y in years}

# Solver
solver = Solver()

# Each student is assigned to exactly one year
for s in students:
    solver.add(Or([assign[s] == y for y in years]))

# Each year is assigned to exactly one student
for y in years:
    solver.add(Or([year_assign[y] == students.index(s) for s in students]))

# Each year is assigned to exactly one student (exclusivity)
for y in years:
    for s1 in students:
        for s2 in students:
            if s1 != s2:
                solver.add(Implies(year_assign[y] == students.index(s1), year_assign[y] != students.index(s2)))

# Constraint 1: Only Louis or Tiffany can be assigned to 1923
solver.add(Or([year_assign[1923] == students.index('Louis'), year_assign[1923] == students.index('Tiffany')]))

# Constraint 2: If Mollie is assigned, she must be assigned to 1921 or 1922
solver.add(Implies(Or([year_assign[y] == students.index('Mollie') for y in years]),
                   Or([year_assign[1921] == students.index('Mollie'), year_assign[1922] == students.index('Mollie')])))

# Constraint 3: If Tiffany is assigned, Ryan must be assigned
solver.add(Implies(Or([year_assign[y] == students.index('Tiffany') for y in years]),
                   Or([year_assign[y] == students.index('Ryan') for y in years])))

# Constraint 4: If Ryan is assigned, Onyx must be assigned to the year immediately prior to Ryan's year
for y in years:
    if y > 1921:
        solver.add(Implies(year_assign[y] == students.index('Ryan'),
                           year_assign[y-1] == students.index('Onyx')))

# Now, count the number of students who could be assigned to 1921
possible_1921_students = []
for s in students:
    solver.push()
    solver.add(year_assign[1921] == students.index(s))
    if solver.check() == sat:
        possible_1921_students.append(s)
    solver.pop()

# Evaluate answer choices
found_options = []
for letter, count in [("A", 6), ("B", 5), ("C", 4), ("D", 3), ("E", 2)]:
    solver.push()
    solver.add(len(possible_1921_students) == count)
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