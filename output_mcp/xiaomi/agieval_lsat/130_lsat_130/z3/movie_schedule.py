from z3 import *

solver = Solver()

# Movies: 0=horror, 1=mystery, 2=romance, 3=sci-fi, 4=western
movies = [0, 1, 2, 3, 4]
movie_names = {0: "horror", 1: "mystery", 2: "romance", 3: "sci-fi", 4: "western"}

# Time slots: 0=7pm, 1=8pm, 2=9pm
# Screen 1: slots 0 and 2
# Screen 2: slots 0 and 2
# Screen 3: slot 1 only

# For each movie, assign a screen (1,2,3) and a time slot (0,1,2)
screen = [Int(f'screen_{i}') for i in range(5)]
time = [Int(f'time_{i}') for i in range(5)]

# Domain constraints
for i in range(5):
    solver.add(Or(screen[i] == 1, screen[i] == 2, screen[i] == 3))
    solver.add(Or(time[i] == 0, time[i] == 1, time[i] == 2))

# Valid screen-time combinations
for i in range(5):
    # Screen 1: only 7pm (0) or 9pm (2)
    solver.add(Implies(screen[i] == 1, Or(time[i] == 0, time[i] == 2)))
    # Screen 2: only 7pm (0) or 9pm (2)
    solver.add(Implies(screen[i] == 2, Or(time[i] == 0, time[i] == 2)))
    # Screen 3: only 8pm (1)
    solver.add(Implies(screen[i] == 3, time[i] == 1))

# Each movie shown exactly once - all (screen, time) pairs must be distinct
for i in range(5):
    for j in range(i+1, 5):
        solver.add(Or(screen[i] != screen[j], time[i] != time[j]))

# Screen 1 has exactly 2 movies (at 7pm and 9pm)
solver.add(Sum([If(screen[i] == 1, 1, 0) for i in range(5)]) == 2)
# Screen 2 has exactly 2 movies (at 7pm and 9pm)
solver.add(Sum([If(screen[i] == 2, 1, 0) for i in range(5)]) == 2)
# Screen 3 has exactly 1 movie (at 8pm)
solver.add(Sum([If(screen[i] == 3, 1, 0) for i in range(5)]) == 1)

# Constraint 1: Western (4) begins before horror (0)
solver.add(time[4] < time[0])

# Constraint 2: Sci-fi (3) not on screen 3
solver.add(screen[3] != 3)

# Constraint 3: Romance (2) not on screen 2
solver.add(screen[2] != 2)

# Constraint 4: Horror (0) and mystery (1) on different screens
solver.add(screen[0] != screen[1])

# Additional condition: Western (4) and sci-fi (3) on the same screen
solver.add(screen[4] == screen[3])

# Now evaluate each answer choice
found_options = []

# (A) Horror is shown on screen 2
opt_a = (screen[0] == 2)

# (B) Mystery begins at 9 P.M.
opt_b = (time[1] == 2)

# (C) Romance is shown on screen 3
opt_c = (screen[2] == 3)

# (D) Sci-fi film begins at 7 P.M.
opt_d = (time[3] == 0)

# (E) Western begins at 8 P.M.
opt_e = (time[4] == 1)

for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
        m = solver.model()
        print(f"Option {letter} is SAT:")
        for i in range(5):
            print(f"  {movie_names[i]}: screen={m[screen[i]]}, time={m[time[i]]}")
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