from z3 import *

# Movies: horror, mystery, romance, sci-fi, western
# Screens: 1, 2, 3
# Times: 7PM, 8PM, 9PM
# Screen 1: two movies at 7PM and 9PM
# Screen 2: two movies at 7PM and 9PM
# Screen 3: one movie at 8PM

# We'll model each movie's screen and time.
# Let's use integers for screen (1,2,3) and time (7,8,9).

movies = ["horror", "mystery", "romance", "scifi", "western"]
screen = {m: Int(f"screen_{m}") for m in movies}
time = {m: Int(f"time_{m}") for m in movies}

solver = Solver()

# Domains
for m in movies:
    solver.add(screen[m] >= 1, screen[m] <= 3)
    solver.add(time[m] >= 7, time[m] <= 9)

# Each movie shown exactly once (already covered by one screen and time per movie)

# Screen 1 and 2 show two movies each, at 7PM and 9PM
# Screen 3 shows exactly one movie at 8PM

# Exactly two movies on screen 1, two on screen 2, one on screen 3
solver.add(Sum([If(screen[m] == 1, 1, 0) for m in movies]) == 2)
solver.add(Sum([If(screen[m] == 2, 1, 0) for m in movies]) == 2)
solver.add(Sum([If(screen[m] == 3, 1, 0) for m in movies]) == 1)

# Screen 1: movies at 7PM and 9PM
for m in movies:
    solver.add(Implies(screen[m] == 1, Or(time[m] == 7, time[m] == 9)))
# Screen 2: movies at 7PM and 9PM
for m in movies:
    solver.add(Implies(screen[m] == 2, Or(time[m] == 7, time[m] == 9)))
# Screen 3: movie at 8PM
for m in movies:
    solver.add(Implies(screen[m] == 3, time[m] == 8))

# On each screen, the two movies must have different times
for scr in [1, 2]:
    movies_on_scr = [m for m in movies]
    # At most one movie at 7PM on screen scr, at most one at 9PM
    solver.add(Sum([If(And(screen[m] == scr, time[m] == 7), 1, 0) for m in movies]) <= 1)
    solver.add(Sum([If(And(screen[m] == scr, time[m] == 9), 1, 0) for m in movies]) <= 1)

# Actually we need exactly one at 7PM and one at 9PM on screens 1 and 2
for scr in [1, 2]:
    solver.add(Sum([If(And(screen[m] == scr, time[m] == 7), 1, 0) for m in movies]) == 1)
    solver.add(Sum([If(And(screen[m] == scr, time[m] == 9), 1, 0) for m in movies]) == 1)

# Conditions:
# 1. The western begins at some time before the horror film does.
solver.add(time["western"] < time["horror"])

# 2. The sci-fi film is not shown on screen 3.
solver.add(screen["scifi"] != 3)

# 3. The romance is not shown on screen 2.
solver.add(screen["romance"] != 2)

# 4. The horror film and the mystery are shown on different screens.
solver.add(screen["horror"] != screen["mystery"])

# Now define each option as a set of constraints

# Option A:
# screen 1: romance at 7 P.M., horror film at 9 P.M.
# screen 2: western at 7 P.M., sci-fi film at 9 P.M.
# screen 3: mystery at 8 P.M.
opt_a = And(
    screen["romance"] == 1, time["romance"] == 7,
    screen["horror"] == 1, time["horror"] == 9,
    screen["western"] == 2, time["western"] == 7,
    screen["scifi"] == 2, time["scifi"] == 9,
    screen["mystery"] == 3, time["mystery"] == 8
)

# Option B:
# screen 1: mystery at 7 P.M., romance at 9 P.M.
# screen 2: horror film at 7 P.M., sci-fi film at 9 P.M.
# screen 3: western at 8 P.M.
opt_b = And(
    screen["mystery"] == 1, time["mystery"] == 7,
    screen["romance"] == 1, time["romance"] == 9,
    screen["horror"] == 2, time["horror"] == 7,
    screen["scifi"] == 2, time["scifi"] == 9,
    screen["western"] == 3, time["western"] == 8
)

# Option C:
# screen 1: western at 7 P.M., sci-fi film at 9 P.M.
# screen 2: mystery at 7 P.M., horror film at 9 P.M.
# screen 3: romance at 8 P.M.
opt_c = And(
    screen["western"] == 1, time["western"] == 7,
    screen["scifi"] == 1, time["scifi"] == 9,
    screen["mystery"] == 2, time["mystery"] == 7,
    screen["horror"] == 2, time["horror"] == 9,
    screen["romance"] == 3, time["romance"] == 8
)

# Option D:
# screen 1: romance at 7 P.M., mystery at 9 P.M.
# screen 2: western at 7 P.M., horror film at 9 P.M.
# screen 3: sci-fi film at 8 P.M.
opt_d = And(
    screen["romance"] == 1, time["romance"] == 7,
    screen["mystery"] == 1, time["mystery"] == 9,
    screen["western"] == 2, time["western"] == 7,
    screen["horror"] == 2, time["horror"] == 9,
    screen["scifi"] == 3, time["scifi"] == 8
)

# Option E:
# screen 1: western at 7 P.M., mystery at 9 P.M.
# screen 2: sci-fi film at 7 P.M., romance at 9 P.M.
# screen 3: horror film at 8 P.M.
opt_e = And(
    screen["western"] == 1, time["western"] == 7,
    screen["mystery"] == 1, time["mystery"] == 9,
    screen["scifi"] == 2, time["scifi"] == 7,
    screen["romance"] == 2, time["romance"] == 9,
    screen["horror"] == 3, time["horror"] == 8
)

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