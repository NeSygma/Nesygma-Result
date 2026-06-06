from z3 import *

# Base constraints solver
solver = Solver()

# Movies
movies = ["horror", "mystery", "romance", "sci-fi", "western"]

# Screens: 1, 2, 3
# Times: 7 (7 PM), 8 (8 PM), 9 (9 PM)
# Screen 3 only shows at 8 PM
# Screens 1 and 2 show at 7 PM and 9 PM

# For each movie, assign a screen and a time
movie_screen = {m: Int(f"screen_{m}") for m in movies}
movie_time = {m: Int(f"time_{m}") for m in movies}

# Domains
for m in movies:
    solver.add(movie_screen[m] >= 1, movie_screen[m] <= 3)
    solver.add(movie_time[m] >= 7, movie_time[m] <= 9)

# Screen 3 only shows at 8 PM
solver.add(movie_time["horror"] != 8)  # Not strictly necessary but clarifies
solver.add(movie_time["mystery"] != 8)
solver.add(movie_time["romance"] != 8)
solver.add(movie_time["sci-fi"] != 8)
solver.add(movie_time["western"] != 8)

# Actually, only one movie is on screen 3 at 8 PM
# Let's enforce that screen 3 has exactly one movie at time 8
# and that movie is the only one on screen 3
screen3_movie = Const("screen3_movie", StringSort())
solver.add(screen3_movie == "none")
count_screen3 = Sum([If(And(movie_screen[m] == 3, movie_time[m] == 8), 1, 0) for m in movies])
solver.add(count_screen3 == 1)

# For screens 1 and 2, they have two movies: one at 7, one at 9
# So for each screen in {1,2}, there must be exactly one movie at time 7 and one at time 9
for screen in [1, 2]:
    count_time7 = Sum([If(And(movie_screen[m] == screen, movie_time[m] == 7), 1, 0) for m in movies])
    count_time9 = Sum([If(And(movie_screen[m] == screen, movie_time[m] == 9), 1, 0) for m in movies])
    solver.add(count_time7 == 1)
    solver.add(count_time9 == 1)

# Western begins before horror (western time < horror time)
solver.add(movie_time["western"] < movie_time["horror"])

# Sci-fi not on screen 3
solver.add(movie_screen["sci-fi"] != 3)

# Romance not on screen 2
solver.add(movie_screen["romance"] != 2)

# Horror and mystery on different screens
solver.add(movie_screen["horror"] != movie_screen["mystery"])

# All movies must be assigned to some screen and time
# This is already covered by the domains and constraints above

# Now, evaluate each multiple-choice option for screen 2
# Each option specifies: (7 PM movie, 9 PM movie) for screen 2

# Helper function to create constraints for each option
def option_constraints(opt_7pm, opt_9pm):
    # Screen 2 must have exactly these two movies at 7 PM and 9 PM
    solver.push()
    # Screen 2 has opt_7pm at 7 and opt_9pm at 9
    solver.add(movie_screen[opt_7pm] == 2)
    solver.add(movie_time[opt_7pm] == 7)
    solver.add(movie_screen[opt_9pm] == 2)
    solver.add(movie_time[opt_9pm] == 9)
    # All other movies must not be on screen 2
    for m in movies:
        if m != opt_7pm and m != opt_9pm:
            solver.add(movie_screen[m] != 2)
    # Check if this is satisfiable
    result = solver.check()
    solver.pop()
    return result == sat

# Evaluate each option
found_options = []

# Option A: sci-fi (7 PM), horror (9 PM)
if option_constraints("sci-fi", "horror"):
    found_options.append("A")

# Option B: sci-fi (7 PM), mystery (9 PM)
if option_constraints("sci-fi", "mystery"):
    found_options.append("B")

# Option C: sci-fi (7 PM), western (9 PM)
if option_constraints("sci-fi", "western"):
    found_options.append("C")

# Option D: western (7 PM), horror (9 PM)
if option_constraints("western", "horror"):
    found_options.append("D")

# Option E: western (7 PM), mystery (9 PM)
if option_constraints("western", "mystery"):
    found_options.append("E")

# Output result
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")