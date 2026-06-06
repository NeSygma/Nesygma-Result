from z3 import *

solver = Solver()

# Movies: horror, mystery, romance, sci-fi, western
# Screens: 1, 2, 3
# Times: 7pm, 8pm, 9pm
# Screen 1: two movies at 7pm and 9pm
# Screen 2: two movies at 7pm and 9pm
# Screen 3: one movie at 8pm

# Define variables for screen and time of each movie
# screen[m] ∈ {1, 2, 3}
# time[m] ∈ {7, 8, 9}

movies = ['horror', 'mystery', 'romance', 'scifi', 'western']
screen = {m: Int(f'screen_{m}') for m in movies}
time = {m: Int(f'time_{m}') for m in movies}

# Domain constraints
for m in movies:
    solver.add(Or(screen[m] == 1, screen[m] == 2, screen[m] == 3))
    solver.add(Or(time[m] == 7, time[m] == 8, time[m] == 9))

# Screen 1: two movies, one at 7pm and one at 9pm
# Screen 2: two movies, one at 7pm and one at 9pm
# Screen 3: one movie at 8pm

# Each movie shown exactly once (already implicit by having one screen and one time per movie)

# Screen-time constraints:
# If on screen 1 or 2, time must be 7 or 9
# If on screen 3, time must be 8
for m in movies:
    solver.add(Implies(screen[m] == 1, Or(time[m] == 7, time[m] == 9)))
    solver.add(Implies(screen[m] == 2, Or(time[m] == 7, time[m] == 9)))
    solver.add(Implies(screen[m] == 3, time[m] == 8))

# Exactly 2 movies on screen 1, 2 on screen 2, 1 on screen 3
solver.add(Sum([If(screen[m] == 1, 1, 0) for m in movies]) == 2)
solver.add(Sum([If(screen[m] == 2, 1, 0) for m in movies]) == 2)
solver.add(Sum([If(screen[m] == 3, 1, 0) for m in movies]) == 1)

# Exactly 2 movies at 7pm (on screens 1 and 2), 1 at 8pm (on screen 3), 2 at 9pm (on screens 1 and 2)
solver.add(Sum([If(time[m] == 7, 1, 0) for m in movies]) == 2)
solver.add(Sum([If(time[m] == 8, 1, 0) for m in movies]) == 1)
solver.add(Sum([If(time[m] == 9, 1, 0) for m in movies]) == 2)

# Condition 1: The western begins at some time before the horror film does.
solver.add(time['western'] < time['horror'])

# Condition 2: The sci-fi film is not shown on screen 3.
solver.add(screen['scifi'] != 3)

# Condition 3: The romance is not shown on screen 2.
solver.add(screen['romance'] != 2)

# Condition 4: The horror film and the mystery are shown on different screens.
solver.add(screen['horror'] != screen['mystery'])

# Additional condition: sci-fi and romance are on the same screen
solver.add(screen['scifi'] == screen['romance'])

# Now test each answer choice
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