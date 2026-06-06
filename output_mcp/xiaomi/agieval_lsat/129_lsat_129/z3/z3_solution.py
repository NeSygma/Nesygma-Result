from z3 import *

# Movies: horror, mystery, romance, sci-fi, western
# Screens: 1, 2, 3
# Times: 7pm, 8pm, 9pm
# Screen 1: 7pm and 9pm
# Screen 2: 7pm and 9pm
# Screen 3: 8pm only

# Variables: for each movie, which screen and which time
# screen[movie] in {1, 2, 3}
# time[movie] in {7, 8, 9}

movies = ['horror', 'mystery', 'romance', 'scifi', 'western']

screen = {m: Int(f'screen_{m}') for m in movies}
time = {m: Int(f'time_{m}') for m in movies}

solver = Solver()

# Domain constraints
for m in movies:
    solver.add(Or(screen[m] == 1, screen[m] == 2, screen[m] == 3))
    solver.add(Or(time[m] == 7, time[m] == 8, time[m] == 9))

# Screen 1: two movies at 7pm and 9pm
# Screen 2: two movies at 7pm and 9pm
# Screen 3: one movie at 8pm

# Each movie shown exactly once (already by construction)

# Time constraints per screen
for m in movies:
    # If on screen 1 or 2, time must be 7 or 9
    solver.add(Implies(Or(screen[m] == 1, screen[m] == 2), Or(time[m] == 7, time[m] == 9)))
    # If on screen 3, time must be 8
    solver.add(Implies(screen[m] == 3, time[m] == 8))

# Exactly 2 movies on screen 1, 2 on screen 2, 1 on screen 3
solver.add(Sum([If(screen[m] == 1, 1, 0) for m in movies]) == 2)
solver.add(Sum([If(screen[m] == 2, 1, 0) for m in movies]) == 2)
solver.add(Sum([If(screen[m] == 3, 1, 0) for m in movies]) == 1)

# On each screen, no two movies at the same time
# Screen 1: two movies must have different times (7 and 9)
# Screen 2: two movies must have different times (7 and 9)
# Screen 3: only one movie, so no conflict needed

# For screen 1: if two movies are on screen 1, they must have different times
for m1 in movies:
    for m2 in movies:
        if m1 < m2:
            solver.add(Implies(And(screen[m1] == 1, screen[m2] == 1), time[m1] != time[m2]))
            solver.add(Implies(And(screen[m1] == 2, screen[m2] == 2), time[m1] != time[m2]))

# Condition 1: Western begins before horror
# "begins at some time before" means western's time < horror's time
solver.add(time['western'] < time['horror'])

# Condition 2: Sci-fi not on screen 3
solver.add(screen['scifi'] != 3)

# Condition 3: Romance not on screen 2
solver.add(screen['romance'] != 2)

# Condition 4: Horror and mystery on different screens
solver.add(screen['horror'] != screen['mystery'])

# Now evaluate each option for screen 2
# Each option specifies: (7pm movie, 9pm movie) on screen 2

# Option A: sci-fi at 7pm on screen 2, horror at 9pm on screen 2
opt_a = And(screen['scifi'] == 2, time['scifi'] == 7, screen['horror'] == 2, time['horror'] == 9)

# Option B: sci-fi at 7pm on screen 2, mystery at 9pm on screen 2
opt_b = And(screen['scifi'] == 2, time['scifi'] == 7, screen['mystery'] == 2, time['mystery'] == 9)

# Option C: sci-fi at 7pm on screen 2, western at 9pm on screen 2
opt_c = And(screen['scifi'] == 2, time['scifi'] == 7, screen['western'] == 2, time['western'] == 9)

# Option D: western at 7pm on screen 2, horror at 9pm on screen 2
opt_d = And(screen['western'] == 2, time['western'] == 7, screen['horror'] == 2, time['horror'] == 9)

# Option E: western at 7pm on screen 2, mystery at 9pm on screen 2
opt_e = And(screen['western'] == 2, time['western'] == 7, screen['mystery'] == 2, time['mystery'] == 9)

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