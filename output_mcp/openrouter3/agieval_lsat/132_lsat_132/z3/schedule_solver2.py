from z3 import *

# Create solver
solver = Solver()

# Define movies
movies = ["horror", "mystery", "romance", "scifi", "western"]
movie_vars = {m: Int(f"movie_{m}") for m in movies}

# Define screens and times
screen = {m: Int(f"screen_{m}") for m in movies}
time = {m: Int(f"time_{m}") for m in movies}

# Basic constraints: each movie on a screen 1-3
for m in movies:
    solver.add(screen[m] >= 1)
    solver.add(screen[m] <= 3)
    solver.add(Or(time[m] == 7, time[m] == 8, time[m] == 9))

# Screen 3 must have exactly one movie at 8pm
solver.add(Sum([If(screen[m] == 3, 1, 0) for m in movies]) == 1)
for m in movies:
    solver.add(Implies(screen[m] == 3, time[m] == 8))

# Screen 1 and 2 must have exactly two movies each
solver.add(Sum([If(screen[m] == 1, 1, 0) for m in movies]) == 2)
solver.add(Sum([If(screen[m] == 2, 1, 0) for m in movies]) == 2)

# For screens 1 and 2: one movie at 7pm, one at 9pm
for s in [1, 2]:
    solver.add(Sum([If(And(screen[m] == s, time[m] == 7), 1, 0) for m in movies]) == 1)
    solver.add(Sum([If(And(screen[m] == s, time[m] == 9), 1, 0) for m in movies]) == 1)

# All movies have distinct screen-time combinations
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

# We need to find which option CANNOT be true (i.e., leads to UNSAT)
impossible_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(constr)
    result = solver.check()
    if result == unsat:
        impossible_options.append(letter)
    solver.pop()

# According to the problem, exactly one option should be impossible
if len(impossible_options) == 1:
    print("STATUS: sat")
    print(f"answer:{impossible_options[0]}")
elif len(impossible_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple impossible options found {impossible_options}")
else:
    print("STATUS: unsat")
    print("Refine: No impossible options found")