from z3 import *

# BENCHMARK_MODE: ON (model-finding mode)
BENCHMARK_MODE = True

# Declare movies
movies = ["horror", "mystery", "romance", "sci-fi", "western"]

# Declare screen and time variables
screen = {m: Int(f"screen_{m}") for m in movies}
time = {m: Int(f"time_{m}") for m in movies}

# Screen constraints: 1, 2, or 3
for m in movies:
    screen[m] = Int(f"screen_{m}")
    time[m] = Int(f"time_{m}")

# Screen 3 has exactly one movie at 8 P.M.
# Screens 1 and 2 have two movies each: one at 7 P.M., one at 9 P.M.
# We'll model time as 7, 8, 9

# Helper: time slots
TIME_7 = 7
TIME_8 = 8
TIME_9 = 9

# Constraints
solver = Solver()

# Each movie is assigned to exactly one screen
for m in movies:
    solver.add(Or(screen[m] == 1, screen[m] == 2, screen[m] == 3))

# Each movie is assigned exactly one time
for m in movies:
    solver.add(Or(time[m] == TIME_7, time[m] == TIME_8, time[m] == TIME_9))

# Screen 3 has exactly one movie at 8 P.M.
solver.add(Sum([If(And(screen[m] == 3, time[m] == TIME_8), 1, 0) for m in movies]) == 1)

# Screens 1 and 2 have two movies each: one at 7 P.M., one at 9 P.M.
for s in [1, 2]:
    solver.add(Sum([If(And(screen[m] == s, time[m] == TIME_7), 1, 0) for m in movies]) == 1)
    solver.add(Sum([If(And(screen[m] == s, time[m] == TIME_9), 1, 0) for m in movies]) == 1)

# The western begins at some time before the horror film does.
solver.add(time["western"] < time["horror"])

# The sci-fi film is not shown on screen 3.
solver.add(screen["sci-fi"] != 3)

# The romance is not shown on screen 2.
solver.add(screen["romance"] != 2)

# The horror film and the mystery are shown on different screens.
solver.add(screen["horror"] != screen["mystery"])

# The western and the sci-fi film are scheduled to be shown on the same screen.
solver.add(screen["western"] == screen["sci-fi"])

# Now evaluate each option
found_options = []

# Option A: The horror film is shown on screen 2.
solver.push()
solver.add(screen["horror"] == 2)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: The mystery begins at 9 P.M.
solver.push()
solver.add(time["mystery"] == TIME_9)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: The romance is shown on screen 3.
solver.push()
solver.add(screen["romance"] == 3)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: The sci-fi film begins at 7 P.M.
solver.push()
solver.add(time["sci-fi"] == TIME_7)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: The western begins at 8 P.M.
solver.push()
solver.add(time["western"] == TIME_8)
if solver.check() == sat:
    found_options.append("E")
solver.pop()

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