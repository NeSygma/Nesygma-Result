from z3 import *

# Declare movies and screens
movies = ["horror", "mystery", "romance", "sci_fi", "western"]
screens = [1, 2, 3]

# Create symbolic variables for screen assignments of each movie
screen = {m: Int(f"screen_{m}") for m in movies}

# Create symbolic variables for time slots of each movie
time = {m: Int(f"time_{m}") for m in movies}

# Create a solver
solver = Solver()

# Constraint 1: Each movie is assigned to exactly one screen
for m in movies:
    solver.add(Or([screen[m] == s for s in screens]))

# Constraint 2: Each movie is assigned to exactly one time slot
for m in movies:
    solver.add(Or([time[m] == t for t in [7, 8, 9]]))

# Constraint 3: Screen 3 only shows one movie at 8 P.M.
solver.add(Or([And(screen[m] == 3, time[m] == 8) for m in movies]))
# Ensure only one movie is on screen 3
solver.add(Sum([If(screen[m] == 3, 1, 0) for m in movies]) == 1)

# Constraint 4: Screens 1 and 2 show two movies each (at 7 P.M. and 9 P.M.)
# So, the movies on screens 1 and 2 must have time slots 7 or 9
for m in movies:
    solver.add(Implies(Or(screen[m] == 1, screen[m] == 2), Or(time[m] == 7, time[m] == 9)))

# Constraint 5: The western begins before the horror film does
solver.add(time["western"] < time["horror"])

# Constraint 6: The sci-fi film is not shown on screen 3
solver.add(screen["sci_fi"] != 3)

# Constraint 7: The romance is not shown on screen 2
solver.add(screen["romance"] != 2)

# Constraint 8: The horror film and the mystery are shown on different screens
solver.add(screen["horror"] != screen["mystery"])

# Ensure all screen assignments are distinct (no two movies on the same screen at the same time)
solver.add(Distinct(list(screen.values())))

# Now, let's define the answer choices as constraints for screen 1.
# For each answer choice, we will constrain screen 1 to have the specified movies at 7 P.M. and 9 P.M.

def check_choice(letter, first_movie, second_movie):
    solver.push()
    # Screen 1 must show the first movie at 7 P.M. and the second movie at 9 P.M.
    solver.add(screen[first_movie] == 1)
    solver.add(screen[second_movie] == 1)
    solver.add(time[first_movie] == 7)
    solver.add(time[second_movie] == 9)

    result = solver.check()
    solver.pop()
    return result == sat

# Check each answer choice
found_options = []
if check_choice("A", "sci_fi", "horror"):
    found_options.append("A")
if check_choice("B", "sci_fi", "mystery"):
    found_options.append("B")
if check_choice("C", "western", "horror"):
    found_options.append("C")
if check_choice("D", "western", "mystery"):
    found_options.append("D")
if check_choice("E", "western", "sci_fi"):
    found_options.append("E")

# Output the result
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")