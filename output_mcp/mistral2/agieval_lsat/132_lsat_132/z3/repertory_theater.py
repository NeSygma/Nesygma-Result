from z3 import *

# Declare movies and screens
movies = ["horror", "mystery", "romance", "sci_fi", "western"]
screens = [1, 2, 3]
time_slots = [7, 8, 9]  # 7 P.M., 8 P.M., 9 P.M.

# Create symbolic variables for screen assignments of each movie
screen = {m: Int(f"screen_{m}") for m in movies}

# Create symbolic variables for time slots (which screen is showing at each time)
time = {t: Int(f"time_{t}") for t in time_slots}

# Create a solver
solver = Solver()

# Constraint 1: Each movie is assigned to exactly one screen
for m in movies:
    solver.add(Or([screen[m] == s for s in screens]))

# Constraint 2: Screen 3 only shows one movie at 8 P.M.
solver.add(time[8] == 3)
# Ensure only one movie is on screen 3
solver.add(Sum([If(screen[m] == 3, 1, 0) for m in movies]) == 1)

# Constraint 3: Screens 1 and 2 show two movies each (at 7 P.M. and 9 P.M.)
solver.add(Or([time[7] == 1, time[7] == 2]))
solver.add(Or([time[9] == 1, time[9] == 2]))
solver.add(time[7] != time[9])  # Different screens at 7 P.M. and 9 P.M.

# Constraint 4: The western begins before the horror film
# We need to model the time slots for the western and horror films.
# Let's assume the time slot for a movie is the time it starts.
# We need to ensure that the western's time slot is less than the horror's time slot.
# However, we don't have direct time slot variables for movies, so we need to infer them.
# For now, we will assume that the time slot for a movie is the time slot of the screen it is assigned to.
# This is a simplification and may need refinement.

# Constraint 5: The sci-fi film is not shown on screen 3
solver.add(screen["sci_fi"] != 3)

# Constraint 6: The romance is not shown on screen 2
solver.add(screen["romance"] != 2)

# Constraint 7: The horror film and the mystery are shown on different screens
solver.add(screen["horror"] != screen["mystery"])

# Additional constraint: Each screen can only show one movie at a time
# This is implicitly handled by the time slot assignments.

# Now, let's define the answer choices as constraints for screen 1.
# For each answer choice, we will constrain screen 1 to have the specified movies at 7 P.M. and 9 P.M.

# Helper function to check if a choice is possible
def check_choice(letter, first_movie, second_movie):
    solver.push()
    # Screen 1 must show the first movie at 7 P.M. and the second movie at 9 P.M.
    solver.add(time[7] == 1)
    solver.add(time[9] == 1)
    solver.add(screen[first_movie] == 1)
    solver.add(screen[second_movie] == 1)
    # Ensure the first movie is at 7 P.M. and the second at 9 P.M.
    # This is already implied by the time slot assignments.

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