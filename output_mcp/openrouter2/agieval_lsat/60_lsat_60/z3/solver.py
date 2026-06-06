from z3 import *

# Define riders and bikes indices
riders = ['R', 'S', 'T', 'Y']  # Reynaldo, Seamus, Theresa, Yuki
bikes = ['F', 'G', 'H', 'J']

# Map names to indices
r_idx = {name:i for i,name in enumerate(riders)}
b_idx = {name:i for i,name in enumerate(bikes)}

# Create solver and variables
solver = Solver()
# day1 and day2 bike assignments for each rider
day1 = [Int(f'd1_{r}') for r in riders]
day2 = [Int(f'd2_{r}') for r in riders]

# Domain constraints
for v in day1+day2:
    solver.add(v >= 0, v <= 3)

# Distinctness per day
solver.add(Distinct(day1))
solver.add(Distinct(day2))

# Each rider tests a different bike each day
for i in range(4):
    solver.add(day1[i] != day2[i])

# Constraints from problem statement
# Reynaldo cannot test F on any day
solver.add(day1[r_idx['R']] != b_idx['F'])
solver.add(day2[r_idx['R']] != b_idx['F'])
# Yuki cannot test J on any day
solver.add(day1[r_idx['Y']] != b_idx['J'])
solver.add(day2[r_idx['Y']] != b_idx['J'])
# Theresa must test H on either day
solver.add(Or(day1[r_idx['T']] == b_idx['H'], day2[r_idx['T']] == b_idx['H']))
# Yuki's day1 bike must be tested by Seamus on day2
solver.add(day2[r_idx['S']] == day1[r_idx['Y']])

# Define option constraints
options = {
    'A': [
        (day1[r_idx['S']], b_idx['F']), (day2[r_idx['R']], b_idx['F']),
        (day1[r_idx['Y']], b_idx['G']), (day2[r_idx['S']], b_idx['G']),
        (day1[r_idx['T']], b_idx['H']), (day2[r_idx['Y']], b_idx['H']),
        (day1[r_idx['R']], b_idx['J']), (day2[r_idx['T']], b_idx['J'])
    ],
    'B': [
        (day1[r_idx['S']], b_idx['F']), (day2[r_idx['Y']], b_idx['F']),
        (day1[r_idx['R']], b_idx['G']), (day2[r_idx['T']], b_idx['G']),
        (day1[r_idx['Y']], b_idx['H']), (day2[r_idx['S']], b_idx['H']),
        (day1[r_idx['T']], b_idx['J']), (day2[r_idx['R']], b_idx['J'])
    ],
    'C': [
        (day1[r_idx['Y']], b_idx['F']), (day2[r_idx['S']], b_idx['F']),
        (day1[r_idx['S']], b_idx['G']), (day2[r_idx['R']], b_idx['G']),
        (day1[r_idx['T']], b_idx['H']), (day2[r_idx['Y']], b_idx['H']),
        (day1[r_idx['R']], b_idx['J']), (day2[r_idx['T']], b_idx['J'])
    ],
    'D': [
        (day1[r_idx['Y']], b_idx['F']), (day2[r_idx['S']], b_idx['F']),
        (day1[r_idx['T']], b_idx['G']), (day2[r_idx['R']], b_idx['G']),
        (day1[r_idx['R']], b_idx['H']), (day2[r_idx['T']], b_idx['H']),
        (day1[r_idx['S']], b_idx['J']), (day2[r_idx['Y']], b_idx['J'])
    ],
    'E': [
        (day1[r_idx['Y']], b_idx['F']), (day2[r_idx['T']], b_idx['F']),
        (day1[r_idx['S']], b_idx['G']), (day2[r_idx['Y']], b_idx['G']),
        (day1[r_idx['T']], b_idx['H']), (day2[r_idx['R']], b_idx['H']),
        (day1[r_idx['R']], b_idx['J']), (day2[r_idx['S']], b_idx['J'])
    ]
}

found_options = []
for letter, constrs in options.items():
    solver.push()
    for var, val in constrs:
        solver.add(var == val)
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