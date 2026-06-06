from z3 import *

# Movies: horror, mystery, romance, sci-fi, western
# Screens: 1, 2, 3
# Times: 7pm, 8pm, 9pm
# Screen 1: 7pm and 9pm
# Screen 2: 7pm and 9pm
# Screen 3: 8pm only

movies = ['horror', 'mystery', 'romance', 'scifi', 'western']

screen = {m: Int(f'screen_{m}') for m in movies}
time = {m: Int(f'time_{m}') for m in movies}

solver = Solver()

# Domain constraints
for m in movies:
    solver.add(Or(screen[m] == 1, screen[m] == 2, screen[m] == 3))
    solver.add(Or(time[m] == 7, time[m] == 8, time[m] == 9))

# Time constraints per screen
for m in movies:
    solver.add(Implies(Or(screen[m] == 1, screen[m] == 2), Or(time[m] == 7, time[m] == 9)))
    solver.add(Implies(screen[m] == 3, time[m] == 8))

# Exactly 2 movies on screen 1, 2 on screen 2, 1 on screen 3
solver.add(Sum([If(screen[m] == 1, 1, 0) for m in movies]) == 2)
solver.add(Sum([If(screen[m] == 2, 1, 0) for m in movies]) == 2)
solver.add(Sum([If(screen[m] == 3, 1, 0) for m in movies]) == 1)

# On each screen with 2 movies, they must have different times
for m1 in movies:
    for m2 in movies:
        if m1 < m2:
            solver.add(Implies(And(screen[m1] == 1, screen[m2] == 1), time[m1] != time[m2]))
            solver.add(Implies(And(screen[m1] == 2, screen[m2] == 2), time[m1] != time[m2]))

# Condition 1: Western begins before horror
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

print(f"Found options: {found_options}")

# The question asks which CANNOT be accurate
# So we need to find which option is NOT satisfiable (cannot be done)
# Options that CAN be done: A, B, D, E
# Option that CANNOT be done: C

if len(found_options) == 4:
    # 4 options are possible, 1 is not - that's the answer
    all_options = ["A", "B", "C", "D", "E"]
    impossible = [o for o in all_options if o not in found_options]
    if len(impossible) == 1:
        print("STATUS: sat")
        print(f"answer:{impossible[0]}")
    else:
        print("STATUS: unsat")
        print(f"Refine: Unexpected result")
elif len(found_options) == 5:
    print("STATUS: unsat")
    print("Refine: All options possible - no CANNOT answer")
else:
    print("STATUS: unsat")
    print(f"Refine: Unexpected number of possible options: {found_options}")