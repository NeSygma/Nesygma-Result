from z3 import *

solver = Solver()

# Declare movies and screens
movies = ["horror", "mystery", "romance", "sci-fi", "western"]
screens = [1, 2, 3]
times = [7, 8, 9]  # 7 P.M., 8 P.M., 9 P.M.

# Assign each movie to a screen and a time
screen = {m: Int(f"screen_{m}") for m in movies}
time = {m: Int(f"time_{m}") for m in movies}

# Helper: Ensure each movie is assigned to exactly one screen and one time
for m in movies:
    solver.add(Or([screen[m] == s for s in screens]))
    solver.add(Or([time[m] == t for t in times]))

# Base constraints from the problem:
# 1. The western begins at some time before the horror film does.
solver.add(time["western"] < time["horror"])

# 2. The sci-fi film is not shown on screen 3.
solver.add(screen["sci-fi"] != 3)

# 3. The romance is not shown on screen 2.
solver.add(screen["romance"] != 2)

# 4. The horror film and the mystery are shown on different screens.
solver.add(screen["horror"] != screen["mystery"])

# Additional constraints:
# - Screen 3 has exactly one movie at 8 P.M.
# - Screens 1 and 2 have two movies each: one at 7 P.M. and one at 9 P.M.
# - Total movies per screen: screen 1 = 2, screen 2 = 2, screen 3 = 1

# Count movies per screen
screen_counts = {s: Sum([If(screen[m] == s, 1, 0) for m in movies]) for s in screens}
for s in [1, 2]:
    solver.add(screen_counts[s] == 2)
solver.add(screen_counts[3] == 1)

# Count movies per time slot
time_counts = {t: Sum([If(time[m] == t, 1, 0) for m in movies]) for t in times}
solver.add(time_counts[7] == 2)
solver.add(time_counts[8] == 1)
solver.add(time_counts[9] == 2)

# The western and the sci-fi film are scheduled to be shown on the same screen.
solver.add(screen["western"] == screen["sci-fi"])

# Define the options as constraints
# (A) The horror film is shown on screen 2.
opt_a_constr = (screen["horror"] == 2)

# (B) The mystery begins at 9 P.M.
opt_b_constr = (time["mystery"] == 9)

# (C) The romance is shown on screen 3.
opt_c_constr = (screen["romance"] == 3)

# (D) The sci-fi film begins at 7 P.M.
opt_d_constr = (time["sci-fi"] == 7)

# (E) The western begins at 8 P.M.
opt_e_constr = (time["western"] == 8)

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