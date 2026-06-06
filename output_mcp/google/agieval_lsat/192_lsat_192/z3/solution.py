from z3 import *

# Students
students = ['L', 'M', 'O', 'R', 'T', 'Y']
years = [1921, 1922, 1923, 1924]

# Variables: assigned[s] is the year assigned to student s, or 0 if not assigned
assigned = {s: Int(f'assigned_{s}') for s in students}

solver = Solver()

# Each student is either assigned to a year or 0
for s in students:
    solver.add(Or([assigned[s] == y for y in years] + [assigned[s] == 0]))

# Exactly 4 students are assigned
solver.add(Sum([If(assigned[s] != 0, 1, 0) for s in students]) == 4)

# Each year has exactly one student
for y in years:
    solver.add(Sum([If(assigned[s] == y, 1, 0) for s in students]) == 1)

# Condition 1: Only Louis or Tiffany can be assigned to 1923
# (This means 1923 must be assigned to either L or T)
solver.add(Or(assigned['L'] == 1923, assigned['T'] == 1923))

# Condition 2: If Mollie is assigned, she must be in 1921 or 1922
solver.add(Implies(assigned['M'] != 0, Or(assigned['M'] == 1921, assigned['M'] == 1922)))

# Condition 3: If Tiffany is assigned, Ryan must be assigned
solver.add(Implies(assigned['T'] != 0, assigned['R'] != 0))

# Condition 4: If Ryan is assigned, Onyx must be assigned to the year immediately prior
# (If R is 1921, this is impossible, so R cannot be 1921)
solver.add(Implies(assigned['R'] != 0, And(assigned['O'] == assigned['R'] - 1, assigned['R'] != 1921)))

# Question: Ryan and Yoshio are assigned
solver.add(assigned['R'] != 0)
solver.add(assigned['Y'] != 0)

# Options
options = [
    ("A", assigned['L'] == 1923),
    ("B", assigned['M'] == 1921),
    ("C", assigned['O'] == 1922),
    ("D", assigned['T'] == 1924),
    ("E", assigned['Y'] == 1922)
]

found_options = []
for letter, constr in options:
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