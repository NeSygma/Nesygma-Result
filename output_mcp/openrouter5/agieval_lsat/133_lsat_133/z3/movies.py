from z3 import *

solver = Solver()

# Movies: horror, mystery, romance, scifi, western
# We'll assign each movie a screen (1,2,3) and a time slot.
# Screens 1 and 2 have two movies each: one at 7PM, one at 9PM.
# Screen 3 has exactly one movie at 8PM.

# Let's model each movie's screen and time.
# We'll use Int variables for screen (1,2,3) and time (7,8,9).
# But time is determined by screen: screen 3 => time 8; screens 1,2 => time 7 or 9.

movies = ['horror', 'mystery', 'romance', 'scifi', 'western']
screen = {m: Int(f'screen_{m}') for m in movies}
time = {m: Int(f'time_{m}') for m in movies}

# Domains
for m in movies:
    solver.add(screen[m] >= 1, screen[m] <= 3)
    solver.add(time[m] >= 7, time[m] <= 9)
    # time must be 7, 8, or 9
    solver.add(Or(time[m] == 7, time[m] == 8, time[m] == 9))

# Each movie shown exactly once (already covered by one variable per movie)

# Screens 1 and 2 show two movies each, one at 7 and one at 9.
# Screen 3 shows exactly one movie at 8.
# So for each screen, the number of movies on that screen and the times must match.

# Count movies per screen
for scr in [1, 2, 3]:
    count_on_screen = Sum([If(screen[m] == scr, 1, 0) for m in movies])
    if scr == 3:
        solver.add(count_on_screen == 1)
    else:
        solver.add(count_on_screen == 2)

# For screens 1 and 2: exactly one movie at 7 and one at 9
for scr in [1, 2]:
    count_at_7 = Sum([If(And(screen[m] == scr, time[m] == 7), 1, 0) for m in movies])
    count_at_9 = Sum([If(And(screen[m] == scr, time[m] == 9), 1, 0) for m in movies])
    solver.add(count_at_7 == 1)
    solver.add(count_at_9 == 1)

# Screen 3: exactly one movie at 8
count_at_8_on_3 = Sum([If(And(screen[m] == 3, time[m] == 8), 1, 0) for m in movies])
solver.add(count_at_8_on_3 == 1)

# No movie on screen 3 can have time != 8
for m in movies:
    solver.add(Implies(screen[m] == 3, time[m] == 8))
    # Movies on screens 1 or 2 cannot be at 8
    solver.add(Implies(Or(screen[m] == 1, screen[m] == 2), time[m] != 8))

# Conditions:
# 1. The western begins at some time before the horror film does.
solver.add(time['western'] < time['horror'])

# 2. The sci-fi film is not shown on screen 3.
solver.add(screen['scifi'] != 3)

# 3. The romance is not shown on screen 2.
solver.add(screen['romance'] != 2)

# 4. The horror film and the mystery are shown on different screens.
solver.add(screen['horror'] != screen['mystery'])

# Additional condition from the question:
# "If the sci-fi film and the romance are to be shown on the same screen"
solver.add(screen['scifi'] == screen['romance'])

# Now evaluate each option
# (A) The western begins at 7 P.M.
opt_a = (time['western'] == 7)

# (B) The sci-fi film begins at 9 P.M.
opt_b = (time['scifi'] == 9)

# (C) The mystery begins at 8 P.M.
opt_c = (time['mystery'] == 8)

# (D) The romance begins at 9 P.M.
opt_d = (time['romance'] == 9)

# (E) The horror film begins at 8 P.M.
opt_e = (time['horror'] == 8)

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