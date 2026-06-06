from z3 import *

# Declare variables for each movie: screen and time
movies = ["horror", "mystery", "romance", "sci_fi", "western"]
screen = {m: Int(f"screen_{m}") for m in movies}
time = {m: Int(f"time_{m}") for m in movies}

solver = Solver()

# Base constraints
# 1. Each movie shown exactly once (handled by unique screen/time assignments)
# 2. Screen constraints: screen 1 and 2 have two movies each at 7 and 9 PM
#    Screen 3 has one movie at 8 PM

# Screen constraints: each screen has specific time slots
# Screen 1: movies at 7 PM and 9 PM
# Screen 2: movies at 7 PM and 9 PM  
# Screen 3: movie at 8 PM

# Time values: 7, 8, 9
for m in movies:
    solver.add(Or(screen[m] == 1, screen[m] == 2, screen[m] == 3))
    solver.add(Or(time[m] == 7, time[m] == 8, time[m] == 9))

# Screen 3 must have exactly one movie at 8 PM
screen3_movies = [m for m in movies if screen[m] == 3]
# We'll handle this with the specific option constraints

# Constraint: Western begins before horror film
solver.add(time["western"] < time["horror"])

# Constraint: Sci-fi not on screen 3
solver.add(screen["sci_fi"] != 3)

# Constraint: Romance not on screen 2
solver.add(screen["romance"] != 2)

# Constraint: Horror and mystery on different screens
solver.add(screen["horror"] != screen["mystery"])

# Now define option constraints
# Option A: screen 1: romance at 7 PM, horror at 9 PM
#          screen 2: western at 7 PM, sci-fi at 9 PM
#          screen 3: mystery at 8 PM
opt_a_constr = And(
    screen["romance"] == 1, time["romance"] == 7,
    screen["horror"] == 1, time["horror"] == 9,
    screen["western"] == 2, time["western"] == 7,
    screen["sci_fi"] == 2, time["sci_fi"] == 9,
    screen["mystery"] == 3, time["mystery"] == 8
)

# Option B: screen 1: mystery at 7 PM, romance at 9 PM
#          screen 2: horror at 7 PM, sci-fi at 9 PM
#          screen 3: western at 8 PM
opt_b_constr = And(
    screen["mystery"] == 1, time["mystery"] == 7,
    screen["romance"] == 1, time["romance"] == 9,
    screen["horror"] == 2, time["horror"] == 7,
    screen["sci_fi"] == 2, time["sci_fi"] == 9,
    screen["western"] == 3, time["western"] == 8
)

# Option C: screen 1: western at 7 PM, sci-fi at 9 PM
#          screen 2: mystery at 7 PM, horror at 9 PM
#          screen 3: romance at 8 PM
opt_c_constr = And(
    screen["western"] == 1, time["western"] == 7,
    screen["sci_fi"] == 1, time["sci_fi"] == 9,
    screen["mystery"] == 2, time["mystery"] == 7,
    screen["horror"] == 2, time["horror"] == 9,
    screen["romance"] == 3, time["romance"] == 8
)

# Option D: screen 1: romance at 7 PM, mystery at 9 PM
#          screen 2: western at 7 PM, horror at 9 PM
#          screen 3: sci-fi at 8 PM
opt_d_constr = And(
    screen["romance"] == 1, time["romance"] == 7,
    screen["mystery"] == 1, time["mystery"] == 9,
    screen["western"] == 2, time["western"] == 7,
    screen["horror"] == 2, time["horror"] == 9,
    screen["sci_fi"] == 3, time["sci_fi"] == 8
)

# Option E: screen 1: western at 7 PM, mystery at 9 PM
#          screen 2: sci-fi at 7 PM, romance at 9 PM
#          screen 3: horror at 8 PM
opt_e_constr = And(
    screen["western"] == 1, time["western"] == 7,
    screen["mystery"] == 1, time["mystery"] == 9,
    screen["sci_fi"] == 2, time["sci_fi"] == 7,
    screen["romance"] == 2, time["romance"] == 9,
    screen["horror"] == 3, time["horror"] == 8
)

# Evaluate each option
found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
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