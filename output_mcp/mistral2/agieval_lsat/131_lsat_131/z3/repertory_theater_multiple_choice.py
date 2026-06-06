from z3 import *

# Base constraints and setup
solver = Solver()

# Movies: horror, mystery, romance, sci-fi, western
movies = ["horror", "mystery", "romance", "sci-fi", "western"]

# Screens: 1, 2, 3
screens = [1, 2, 3]

# Time slots: 7 P.M., 8 P.M., 9 P.M.
times = [7, 8, 9]

# Screen 3 shows exactly one movie at 8 P.M.
# Screens 1 and 2 show two movies each: one at 7 P.M. and one at 9 P.M.

# Assign each movie to a screen and a time
movie_to_screen = {movie: Int(f"{movie}_screen") for movie in movies}
movie_to_time = {movie: Int(f"{movie}_time") for movie in movies}

# Constraints:
# 1. Each movie is assigned to exactly one screen and one time
for movie in movies:
    solver.add(Or([movie_to_screen[movie] == s for s in screens]))
    solver.add(Or([movie_to_time[movie] == t for t in times]))

# 2. Screen 3 shows exactly one movie at 8 P.M.
solver.add(Sum([If(And(movie_to_screen[movie] == 3, movie_to_time[movie] == 8), 1, 0) for movie in movies]) == 1)

# 3. Screens 1 and 2 show two movies each: one at 7 P.M. and one at 9 P.M.
for screen in [1, 2]:
    solver.add(Sum([If(And(movie_to_screen[movie] == screen, movie_to_time[movie] == 7), 1, 0) for movie in movies]) == 1)
    solver.add(Sum([If(And(movie_to_screen[movie] == screen, movie_to_time[movie] == 9), 1, 0) for movie in movies]) == 1)

# 4. The western begins at some time before the horror film does.
# This means: time(western) < time(horror)
solver.add(movie_to_time["western"] < movie_to_time["horror"])

# 5. The sci-fi film is not shown on screen 3.
solver.add(movie_to_screen["sci-fi"] != 3)

# 6. The romance is not shown on screen 2.
solver.add(movie_to_screen["romance"] != 2)

# 7. The horror film and the mystery are shown on different screens.
solver.add(movie_to_screen["horror"] != movie_to_screen["mystery"])

# Additional constraint from the question:
# The romance is scheduled to begin before the western does.
# This means: time(romance) < time(western)
solver.add(movie_to_time["romance"] < movie_to_time["western"])

# Now, evaluate each option to see which must be true
found_options = []

# Option A: The horror film is shown on screen 1.
opt_a_constr = (movie_to_screen["horror"] == 1)
solver.push()
solver.add(opt_a_constr)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: The mystery begins at 7 P.M.
opt_b_constr = (movie_to_time["mystery"] == 7)
solver.push()
solver.add(opt_b_constr)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: The mystery is shown on screen 2.
opt_c_constr = (movie_to_screen["mystery"] == 2)
solver.push()
solver.add(opt_c_constr)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: The sci-fi film begins at 9 P.M.
opt_d_constr = (movie_to_time["sci-fi"] == 9)
solver.push()
solver.add(opt_d_constr)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: The sci-fi film is shown on screen 2.
opt_e_constr = (movie_to_screen["sci-fi"] == 2)
solver.push()
solver.add(opt_e_constr)
if solver.check() == sat:
    found_options.append("E")
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