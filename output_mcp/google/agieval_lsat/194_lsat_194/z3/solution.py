from z3 import *

# Students
students = ['L', 'M', 'O', 'R', 'T', 'Y']
years = [1921, 1922, 1923, 1924]

# Variables: assigned[s] is the year assigned to student s, or 0 if not assigned
assigned = {s: Int(f'assigned_{s}') for s in students}

solver = Solver()

# Domain constraints
for s in students:
    solver.add(Or([assigned[s] == y for y in years] + [assigned[s] == 0]))

# Exactly 4 students are assigned
solver.add(Sum([If(assigned[s] != 0, 1, 0) for s in students]) == 4)

# Each year has exactly one student
for y in years:
    solver.add(Sum([If(assigned[s] == y, 1, 0) for s in students]) == 1)

# Constraint 1: Only Louis or Tiffany can be assigned to 1923
# (Since 1923 must be assigned, it must be L or T)
solver.add(Or(assigned['L'] == 1923, assigned['T'] == 1923))

# Constraint 2: If Mollie is assigned, she must be in 1921 or 1922
solver.add(Implies(assigned['M'] != 0, Or(assigned['M'] == 1921, assigned['M'] == 1922)))

# Constraint 3: If Tiffany is assigned, Ryan must be assigned
solver.add(Implies(assigned['T'] != 0, assigned['R'] != 0))

# Constraint 4: If Ryan is assigned, Onyx must be assigned to the year immediately prior
solver.add(Implies(assigned['R'] != 0, assigned['O'] == assigned['R'] - 1))

# Question condition: Yoshio is not assigned
solver.add(assigned['Y'] == 0)

# Options
options = {
    "A": assigned['L'] == 0,
    "B": assigned['R'] == 0,
    "C": assigned['T'] == 0,
    "D": assigned['O'] == 1922,
    "E": assigned['L'] == 1924
}

found_options = []
for letter, constr in options.items():
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