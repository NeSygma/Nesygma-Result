from z3 import *

# Employees
employees = ['R', 'S', 'T', 'V', 'X', 'Y']
# Map each employee to their space number (1-6)
space_of = {e: Int(f'space_{e}') for e in employees}

solver = Solver()

# Constraint 1: Each employee gets one unique space (1-6)
for e in employees:
    solver.add(space_of[e] >= 1, space_of[e] <= 6)
solver.add(Distinct([space_of[e] for e in employees]))

# Constraint 2: Young > Togowa
solver.add(space_of['Y'] > space_of['T'])
# Constraint 3: Xu > Souza
solver.add(space_of['X'] > space_of['S'])
# Constraint 4: Robertson > Young
solver.add(space_of['R'] > space_of['Y'])
# Constraint 5: Robertson is 1, 2, 3, or 4
solver.add(Or(space_of['R'] == 1, space_of['R'] == 2, space_of['R'] == 3, space_of['R'] == 4))

# Define options
def check_option(assignment):
    # assignment is a dict: {employee: space_number}
    s = Solver()
    # Add base constraints
    for e in employees:
        s.add(space_of[e] >= 1, space_of[e] <= 6)
    s.add(Distinct([space_of[e] for e in employees]))
    s.add(space_of['Y'] > space_of['T'])
    s.add(space_of['X'] > space_of['S'])
    s.add(space_of['R'] > space_of['Y'])
    s.add(Or(space_of['R'] == 1, space_of['R'] == 2, space_of['R'] == 3, space_of['R'] == 4))
    
    # Add option-specific constraints
    for e, space in assignment.items():
        s.add(space_of[e] == space)
    
    return s.check() == sat

options = {
    "A": {'Y': 1, 'S': 2, 'V': 3, 'R': 4, 'T': 5, 'X': 6},
    "B": {'V': 1, 'T': 2, 'Y': 3, 'S': 4, 'R': 5, 'X': 6},
    "C": {'T': 1, 'Y': 2, 'X': 3, 'R': 4, 'S': 5, 'V': 6},
    "D": {'T': 1, 'R': 2, 'Y': 3, 'S': 4, 'V': 5, 'X': 6},
    "E": {'S': 1, 'T': 2, 'Y': 3, 'R': 4, 'X': 5, 'V': 6}
}

found_options = []
for letter, assignment in options.items():
    if check_option(assignment):
        found_options.append(letter)

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")