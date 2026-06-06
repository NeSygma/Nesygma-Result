from z3 import *

solver = Solver()

# Define movie indices
horror = 0
mystery = 1
romance = 2
sci_fi = 3
western = 4

# Variables for each movie: screen and time
screen = [Int(f'screen_{i}') for i in range(5)]
time = [Int(f'time_{i}') for i in range(5)]

# Domain constraints for screen: 1,2,3
for i in range(5):
    solver.add(Or(screen[i] == 1, screen[i] == 2, screen[i] == 3))

# Domain constraints for time: 7,8,9
for i in range(5):
    solver.add(Or(time[i] == 7, time[i] == 8, time[i] == 9))

# Screen-time consistency: if screen is 3, time must be 8
for i in range(5):
    solver.add(Implies(screen[i] == 3, time[i] == 8))

# Ensure each screen has correct number of movies:
# Count movies on screen 1
solver.add(Sum([If(screen[i] == 1, 1, 0) for i in range(5)]) == 2)
# Count movies on screen 2
solver.add(Sum([If(screen[i] == 2, 1, 0) for i in range(5)]) == 2)
# Count movies on screen 3
solver.add(Sum([If(screen[i] == 3, 1, 0) for i in range(5)]) == 1)

# Ensure no two movies share same screen and time (i.e., each slot is unique)
for i in range(5):
    for j in range(i+1, 5):
        solver.add(Implies(screen[i] == screen[j], time[i] != time[j]))

# Now add the specific constraints from the problem:
# 1. Western before horror: time[western] < time[horror]
solver.add(time[western] < time[horror])
# 2. Sci-fi not on screen 3
solver.add(screen[sci_fi] != 3)
# 3. Romance not on screen 2
solver.add(screen[romance] != 2)
# 4. Horror and mystery on different screens
solver.add(screen[horror] != screen[mystery])

# Define option assignments as list of (letter, list of (movie, screen, time))
options = [
    ("A", [(romance, 1, 7), (horror, 1, 9), (western, 2, 7), (sci_fi, 2, 9), (mystery, 3, 8)]),
    ("B", [(mystery, 1, 7), (romance, 1, 9), (horror, 2, 7), (sci_fi, 2, 9), (western, 3, 8)]),
    ("C", [(western, 1, 7), (sci_fi, 1, 9), (mystery, 2, 7), (horror, 2, 9), (romance, 3, 8)]),
    ("D", [(romance, 1, 7), (mystery, 1, 9), (western, 2, 7), (horror, 2, 9), (sci_fi, 3, 8)]),
    ("E", [(western, 1, 7), (mystery, 1, 9), (sci_fi, 2, 7), (romance, 2, 9), (horror, 3, 8)])
]

found_options = []
for letter, assignments in options:
    solver.push()
    # Add assignments for each movie
    for movie, scr, tm in assignments:
        solver.add(screen[movie] == scr)
        solver.add(time[movie] == tm)
    # Check satisfiability
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