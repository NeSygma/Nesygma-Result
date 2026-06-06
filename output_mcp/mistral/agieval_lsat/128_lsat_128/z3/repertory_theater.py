from z3 import *

# Base constraints solver
solver = Solver()

# Movies
movies = ["horror", "mystery", "romance", "sci-fi", "western"]

# Screens and times
screens = [1, 2, 3]
times = [7, 8, 9]  # 7 P.M., 8 P.M., 9 P.M.

# For each movie, assign screen and time
movie_screen = {m: Int(f"screen_{m}") for m in movies}
movie_time = {m: Int(f"time_{m}") for m in movies}

# Screen 3 only shows at 8 P.M.
for m in movies:
    solver.add(Implies(movie_screen[m] == 3, movie_time[m] == 8))

# Screens 1 and 2 show at 7 P.M. and 9 P.M.
for m in movies:
    solver.add(Or(movie_screen[m] == 1, movie_screen[m] == 2, movie_screen[m] == 3))
    solver.add(Or(movie_time[m] == 7, movie_time[m] == 8, movie_time[m] == 9))

# Each screen has the correct number of movies:
# Screen 1: 2 movies (7 and 9)
# Screen 2: 2 movies (7 and 9)
# Screen 3: 1 movie (8)

# Count movies per screen
screen_counts = {s: Sum([If(movie_screen[m] == s, 1, 0) for m in movies]) for s in screens}
for s in [1, 2]:
    solver.add(screen_counts[s] == 2)
solver.add(screen_counts[3] == 1)

# Each time slot per screen has at most one movie
# Screen 1: times 7 and 9 must have distinct movies
solver.add(Or(
    And(
        movie_screen["horror"] == 1,
        movie_screen["romance"] == 1,
        movie_time["horror"] != movie_time["romance"]
    ),
    And(
        movie_screen["horror"] == 1,
        movie_screen["mystery"] == 1,
        movie_time["horror"] != movie_time["mystery"]
    ),
    And(
        movie_screen["horror"] == 1,
        movie_screen["sci-fi"] == 1,
        movie_time["horror"] != movie_time["sci-fi"]
    ),
    And(
        movie_screen["horror"] == 1,
        movie_screen["western"] == 1,
        movie_time["horror"] != movie_time["western"]
    ),
    And(
        movie_screen["romance"] == 1,
        movie_screen["mystery"] == 1,
        movie_time["romance"] != movie_time["mystery"]
    ),
    And(
        movie_screen["romance"] == 1,
        movie_screen["sci-fi"] == 1,
        movie_time["romance"] != movie_time["sci-fi"]
    ),
    And(
        movie_screen["romance"] == 1,
        movie_screen["western"] == 1,
        movie_time["romance"] != movie_time["western"]
    ),
    And(
        movie_screen["mystery"] == 1,
        movie_screen["sci-fi"] == 1,
        movie_time["mystery"] != movie_time["sci-fi"]
    ),
    And(
        movie_screen["mystery"] == 1,
        movie_screen["western"] == 1,
        movie_time["mystery"] != movie_time["western"]
    ),
    And(
        movie_screen["sci-fi"] == 1,
        movie_screen["western"] == 1,
        movie_time["sci-fi"] != movie_time["western"]
    )
))

# Screen 2: times 7 and 9 must have distinct movies
solver.add(Or(
    And(
        movie_screen["horror"] == 2,
        movie_screen["romance"] == 2,
        movie_time["horror"] != movie_time["romance"]
    ),
    And(
        movie_screen["horror"] == 2,
        movie_screen["mystery"] == 2,
        movie_time["horror"] != movie_time["mystery"]
    ),
    And(
        movie_screen["horror"] == 2,
        movie_screen["sci-fi"] == 2,
        movie_time["horror"] != movie_time["sci-fi"]
    ),
    And(
        movie_screen["horror"] == 2,
        movie_screen["western"] == 2,
        movie_time["horror"] != movie_time["western"]
    ),
    And(
        movie_screen["romance"] == 2,
        movie_screen["mystery"] == 2,
        movie_time["romance"] != movie_time["mystery"]
    ),
    And(
        movie_screen["romance"] == 2,
        movie_screen["sci-fi"] == 2,
        movie_time["romance"] != movie_time["sci-fi"]
    ),
    And(
        movie_screen["romance"] == 2,
        movie_screen["western"] == 2,
        movie_time["romance"] != movie_time["western"]
    ),
    And(
        movie_screen["mystery"] == 2,
        movie_screen["sci-fi"] == 2,
        movie_time["mystery"] != movie_time["sci-fi"]
    ),
    And(
        movie_screen["mystery"] == 2,
        movie_screen["western"] == 2,
        movie_time["mystery"] != movie_time["western"]
    ),
    And(
        movie_screen["sci-fi"] == 2,
        movie_screen["western"] == 2,
        movie_time["sci-fi"] != movie_time["western"]
    )
))

# Screen 3: only one movie at time 8
solver.add(AtMost(*[movie_time[m] == 8 for m in movies], 1))

# Constraints from the problem statement
# 1. The western begins at some time before the horror film does.
solver.add(movie_time["western"] < movie_time["horror"])

# 2. The sci-fi film is not shown on screen 3.
solver.add(movie_screen["sci-fi"] != 3)

# 3. The romance is not shown on screen 2.
solver.add(movie_screen["romance"] != 2)

# 4. The horror film and the mystery are shown on different screens.
solver.add(movie_screen["horror"] != movie_screen["mystery"])

# Now, evaluate each multiple-choice option
found_options = []

# Option A: screen 1: romance at 7 P.M., horror film at 9 P.M. screen 2: western at 7 P.M., sci-fi film at 9 P.M. screen 3: mystery at 8 P.M.
opt_a_constr = And(
    movie_screen["romance"] == 1, movie_time["romance"] == 7,
    movie_screen["horror"] == 1, movie_time["horror"] == 9,
    movie_screen["western"] == 2, movie_time["western"] == 7,
    movie_screen["sci-fi"] == 2, movie_time["sci-fi"] == 9,
    movie_screen["mystery"] == 3, movie_time["mystery"] == 8
)

# Option B: screen 1: mystery at 7 P.M., romance at 9 P.M. screen 2: horror film at 7 P.M., sci-fi film at 9 P.M. screen 3: western at 8 P.M.
opt_b_constr = And(
    movie_screen["mystery"] == 1, movie_time["mystery"] == 7,
    movie_screen["romance"] == 1, movie_time["romance"] == 9,
    movie_screen["horror"] == 2, movie_time["horror"] == 7,
    movie_screen["sci-fi"] == 2, movie_time["sci-fi"] == 9,
    movie_screen["western"] == 3, movie_time["western"] == 8
)

# Option C: screen 1: western at 7 P.M., sci-fi film at 9 P.M. screen 2: mystery at 7 P.M., horror film at 9 P.M. screen 3: romance at 8 P.M.
opt_c_constr = And(
    movie_screen["western"] == 1, movie_time["western"] == 7,
    movie_screen["sci-fi"] == 1, movie_time["sci-fi"] == 9,
    movie_screen["mystery"] == 2, movie_time["mystery"] == 7,
    movie_screen["horror"] == 2, movie_time["horror"] == 9,
    movie_screen["romance"] == 3, movie_time["romance"] == 8
)

# Option D: screen 1: romance at 7 P.M., mystery at 9 P.M. screen 2: western at 7 P.M., horror film at 9 P.M. screen 3: sci-fi film at 8 P.M.
opt_d_constr = And(
    movie_screen["romance"] == 1, movie_time["romance"] == 7,
    movie_screen["mystery"] == 1, movie_time["mystery"] == 9,
    movie_screen["western"] == 2, movie_time["western"] == 7,
    movie_screen["horror"] == 2, movie_time["horror"] == 9,
    movie_screen["sci-fi"] == 3, movie_time["sci-fi"] == 8
)

# Option E: screen 1: western at 7 P.M., mystery at 9 P.M. screen 2: sci-fi film at 7 P.M., romance at 9 P.M. screen 3: horror film at 8 P.M.
opt_e_constr = And(
    movie_screen["western"] == 1, movie_time["western"] == 7,
    movie_screen["mystery"] == 1, movie_time["mystery"] == 9,
    movie_screen["sci-fi"] == 2, movie_time["sci-fi"] == 7,
    movie_screen["romance"] == 2, movie_time["romance"] == 9,
    movie_screen["horror"] == 3, movie_time["horror"] == 8
)

# Test each option
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