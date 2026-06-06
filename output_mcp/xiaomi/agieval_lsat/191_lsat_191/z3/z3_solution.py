from z3 import *

solver = Solver()

# Students: Louis=0, Mollie=1, Onyx=2, Ryan=3, Tiffany=4, Yoshio=5
# Years: 1921=0, 1922=1, 1923=2, 1924=3
# We need to assign exactly 4 of the 6 students to the 4 years.

students = ['Louis', 'Mollie', 'Onyx', 'Ryan', 'Tiffany', 'Yoshio']
years = [1921, 1922, 1923, 1924]

# assigned[s] = True if student s is assigned to the project
assigned = [Bool(f'assigned_{s}') for s in students]

# year[s] = which year student s is assigned to (only meaningful if assigned)
year = [Int(f'year_{s}') for s in students]

# Exactly 4 students are assigned
solver.add(Sum([If(assigned[s], 1, 0) for s in range(6)]) == 4)

# Each assigned student gets a valid year (0-3)
for s in range(6):
    solver.add(Implies(assigned[s], And(year[s] >= 0, year[s] <= 3)))

# Each year has exactly one student
for y in range(4):
    solver.add(Sum([If(And(assigned[s], year[s] == y), 1, 0) for s in range(6)]) == 1)

# Condition 1: Only Louis or Tiffany can be assigned to 1923
# If a student is assigned to 1923, that student must be Louis or Tiffany
for s in range(6):
    solver.add(Implies(And(assigned[s], year[s] == 2), Or(s == 0, s == 4)))

# Condition 2: If Mollie is assigned, she must be assigned to 1921 or 1922
solver.add(Implies(assigned[1], Or(year[1] == 0, year[1] == 1)))

# Condition 3: If Tiffany is assigned, then Ryan must be assigned
solver.add(Implies(assigned[4], assigned[3]))

# Condition 4: If Ryan is assigned, then Onyx must be assigned to the year immediately prior to Ryan's
solver.add(Implies(assigned[3], And(assigned[2], year[2] == year[3] - 1)))

# Now test each answer option
# The question: "Mollie must be assigned to 1922 if which one of the following is true?"
# This means: for which option does the option being true FORCE Mollie to be at 1922?
# We check: for each option, is it possible that the option is true AND Mollie is NOT at 1922?
# If it's UNSAT (not possible), then the option forces Mollie to 1922.

options = {
    "A": assigned[0] & (year[0] == 3),  # Louis assigned to 1924
    "B": assigned[2] & (year[2] == 0),  # Onyx assigned to 1921
    "C": assigned[2] & (year[2] == 3),  # Onyx assigned to 1924
    "D": assigned[4] & (year[4] == 2),  # Tiffany assigned to 1923
    "E": assigned[5] & (year[5] == 0),  # Yoshio assigned to 1921
}

found_options = []
for letter, constr in options.items():
    solver.push()
    solver.add(constr)
    # Check if Mollie can be NOT at 1922 while the option is true
    solver.add(Not(And(assigned[1], year[1] == 1)))
    result = solver.check()
    if result == unsat:
        # The option forces Mollie to 1922
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