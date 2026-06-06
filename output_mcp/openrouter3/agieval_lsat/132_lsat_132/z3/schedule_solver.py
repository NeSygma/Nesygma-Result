from z3 import *

# Create solver
solver = Solver()

# Define movies
movies = ["horror", "mystery", "romance", "scifi", "western"]
movie_vars = {m: Int(f"movie_{m}") for m in movies}

# Define screens and times
# Screen 1: 7pm and 9pm
# Screen 2: 7pm and 9pm  
# Screen 3: 8pm only
# We'll represent screen assignment as Int (1,2,3) and time as Int (7,8,9)
screen = {m: Int(f"screen_{m}") for m in movies}
time = {m: Int(f"time_{m}") for m in movies}

# Each movie shown exactly once - all different screens and times
# But note: screen 1 and 2 have two movies each at different times
# Screen 3 has one movie at 8pm

# Basic constraints: each movie on a screen 1-3
for m in movies:
    solver.add(screen[m] >= 1)
    solver.add(screen[m] <= 3)
    solver.add(Or(time[m] == 7, time[m] == 8, time[m] == 9))

# Screen 3 must have exactly one movie at 8pm
screen3_movies = [m for m in movies]
solver.add(Sum([If(screen[m] == 3, 1, 0) for m in movies]) == 1)
for m in movies:
    solver.add(Implies(screen[m] == 3, time[m] == 8))

# Screen 1 and 2 must have exactly two movies each
solver.add(Sum([If(screen[m] == 1, 1, 0) for m in movies]) == 2)
solver.add(Sum([If(screen[m] == 2, 1, 0) for m in movies]) == 2)

# For screens 1 and 2: one movie at 7pm, one at 9pm
for s in [1, 2]:
    screen_m = [m for m in movies if m in movies]  # all movies
    solver.add(Sum([If(And(screen[m] == s, time[m] == 7), 1, 0) for m in movies]) == 1)
    solver.add(Sum([If(And(screen[m] == s, time[m] == 9), 1, 0) for m in movies]) == 1)

# All movies have distinct screen-time combinations (each shown exactly once)
# Since screen 3 has only 8pm, and screens 1/2 have 7pm and 9pm, we need to ensure
# no two movies share same screen and time
for i, m1 in enumerate(movies):
    for m2 in movies[i+1:]:
        solver.add(Or(screen[m1] != screen[m2], time[m1] != time[m2]))

# Condition 1: The western begins at some time before the horror film does
solver.add(time["western"] < time["horror"])

# Condition 2: The sci-fi film is not shown on screen 3
solver.add(screen["scifi"] != 3)

# Condition 3: The romance is not shown on screen 2
solver.add(screen["romance"] != 2)

# Condition 4: The horror film and the mystery are shown on different screens
solver.add(screen["horror"] != screen["mystery"])

# Now test each option for screen 1
# Option A: sci-fi at 7pm, horror at 9pm on screen 1
opt_a = And(screen["scifi"] == 1, time["scifi"] == 7,
            screen["horror"] == 1, time["horror"] == 9)

# Option B: sci-fi at 7pm, mystery at 9pm on screen 1
opt_b = And(screen["scifi"] == 1, time["scifi"] == 7,
            screen["mystery"] == 1, time["mystery"] == 9)

# Option C: western at 7pm, horror at 9pm on screen 1
opt_c = And(screen["western"] == 1, time["western"] == 7,
            screen["horror"] == 1, time["horror"] == 9)

# Option D: western at 7pm, mystery at 9pm on screen 1
opt_d = And(screen["western"] == 1, time["western"] == 7,
            screen["mystery"] == 1, time["mystery"] == 9)

# Option E: western at 7pm, sci-fi at 9pm on screen 1
opt_e = And(screen["western"] == 1, time["western"] == 7,
            screen["scifi"] == 1, time["scifi"] == 9)

found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
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