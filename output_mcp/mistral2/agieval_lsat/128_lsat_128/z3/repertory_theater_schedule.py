from z3 import *

# Base constraints (independent of options)
# We will encode the constraints for each option directly in the loop.

found_options = []

# Define the options as constraints
options = {
    "A": [
        # screen 1: romance at 7 P.M., horror film at 9 P.M.
        ("romance", 1, 7),
        ("horror", 1, 9),
        # screen 2: western at 7 P.M., sci-fi film at 9 P.M.
        ("western", 2, 7),
        ("sci-fi", 2, 9),
        # screen 3: mystery at 8 P.M.
        ("mystery", 3, 8),
    ],
    "B": [
        # screen 1: mystery at 7 P.M., romance at 9 P.M.
        ("mystery", 1, 7),
        ("romance", 1, 9),
        # screen 2: horror film at 7 P.M., sci-fi film at 9 P.M.
        ("horror", 2, 7),
        ("sci-fi", 2, 9),
        # screen 3: western at 8 P.M.
        ("western", 3, 8),
    ],
    "C": [
        # screen 1: western at 7 P.M., sci-fi film at 9 P.M.
        ("western", 1, 7),
        ("sci-fi", 1, 9),
        # screen 2: mystery at 7 P.M., horror film at 9 P.M.
        ("mystery", 2, 7),
        ("horror", 2, 9),
        # screen 3: romance at 8 P.M.
        ("romance", 3, 8),
    ],
    "D": [
        # screen 1: romance at 7 P.M., mystery at 9 P.M.
        ("romance", 1, 7),
        ("mystery", 1, 9),
        # screen 2: western at 7 P.M., horror film at 9 P.M.
        ("western", 2, 7),
        ("horror", 2, 9),
        # screen 3: sci-fi film at 8 P.M.
        ("sci-fi", 3, 8),
    ],
    "E": [
        # screen 1: western at 7 P.M., mystery at 9 P.M.
        ("western", 1, 7),
        ("mystery", 1, 9),
        # screen 2: sci-fi film at 7 P.M., romance at 9 P.M.
        ("sci-fi", 2, 7),
        ("romance", 2, 9),
        # screen 3: horror film at 8 P.M.
        ("horror", 3, 8),
    ],
}

# Helper function to encode constraints for an option
def encode_option_constraints(solver, option_schedule):
    # Unpack the schedule into a dictionary for easier access
    schedule = {}
    for movie, screen, time in option_schedule:
        schedule[movie] = (screen, time)
    
    # Constraint 1: The western begins at some time before the horror film does.
    if "western" in schedule and "horror" in schedule:
        western_screen, western_time = schedule["western"]
        horror_screen, horror_time = schedule["horror"]
        # Western must start before horror
        solver.add(western_time < horror_time)
    else:
        solver.add(False)  # Invalid option if western or horror is missing
    
    # Constraint 2: The sci-fi film is not shown on screen 3.
    if "sci-fi" in schedule:
        sci_fi_screen, _ = schedule["sci-fi"]
        solver.add(sci_fi_screen != 3)
    else:
        solver.add(False)  # Invalid option if sci-fi is missing
    
    # Constraint 3: The romance is not shown on screen 2.
    if "romance" in schedule:
        romance_screen, _ = schedule["romance"]
        solver.add(romance_screen != 2)
    else:
        solver.add(False)  # Invalid option if romance is missing
    
    # Constraint 4: The horror film and the mystery are shown on different screens.
    if "horror" in schedule and "mystery" in schedule:
        horror_screen, _ = schedule["horror"]
        mystery_screen, _ = schedule["mystery"]
        solver.add(horror_screen != mystery_screen)
    else:
        solver.add(False)  # Invalid option if horror or mystery is missing

# Test each option
for letter, schedule in options.items():
    solver = Solver()
    encode_option_constraints(solver, schedule)
    
    if solver.check() == sat:
        found_options.append(letter)

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