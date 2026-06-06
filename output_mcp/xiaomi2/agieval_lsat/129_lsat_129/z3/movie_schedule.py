from z3 import *

solver = Solver()

# Movies: 0=horror, 1=mystery, 2=romance, 3=sci-fi, 4=western
movies = [0, 1, 2, 3, 4]
names = {0: "horror", 1: "mystery", 2: "romance", 3: "sci-fi", 4: "western"}

# Each movie has a screen (1,2,3) and a time (7,8,9)
screen = [Int(f'screen_{i}') for i in range(5)]
time = [Int(f'time_{i}') for i in range(5)]

for i in movies:
    # Screen domain
    solver.add(Or(screen[i] == 1, screen[i] == 2, screen[i] == 3))
    # Time domain
    solver.add(Or(time[i] == 7, time[i] == 8, time[i] == 9))
    # If screen 1 or 2, time must be 7 or 9
    solver.add(Implies(screen[i] != 3, Or(time[i] == 7, time[i] == 9)))
    # If screen 3, time must be 8
    solver.add(Implies(screen[i] == 3, time[i] == 8))

# Screen 1 has exactly 2 movies
solver.add(Sum([If(screen[i] == 1, 1, 0) for i in movies]) == 2)
# Screen 2 has exactly 2 movies
solver.add(Sum([If(screen[i] == 2, 1, 0) for i in movies]) == 2)
# Screen 3 has exactly 1 movie
solver.add(Sum([If(screen[i] == 3, 1, 0) for i in movies]) == 1)

# Each (screen, time) slot has at most 1 movie
# Screen 1 at 7pm: at most 1
solver.add(Sum([If(And(screen[i] == 1, time[i] == 7), 1, 0) for i in movies]) <= 1)
# Screen 1 at 9pm: at most 1
solver.add(Sum([If(And(screen[i] == 1, time[i] == 9), 1, 0) for i in movies]) <= 1)
# Screen 2 at 7pm: at most 1
solver.add(Sum([If(And(screen[i] == 2, time[i] == 7), 1, 0) for i in movies]) <= 1)
# Screen 2 at 9pm: at most 1
solver.add(Sum([If(And(screen[i] == 2, time[i] == 9), 1, 0) for i in movies]) <= 1)
# Screen 3 at 8pm: exactly 1 (already covered by screen 3 == 1 movie)

# Constraint 1: Western begins before horror
solver.add(time[4] < time[0])

# Constraint 2: Sci-fi not on screen 3
solver.add(screen[3] != 3)

# Constraint 3: Romance not on screen 2
solver.add(screen[2] != 2)

# Constraint 4: Horror and mystery on different screens
solver.add(screen[0] != screen[1])

# Now test each answer choice for screen 2
# Answer choices specify screen 2's 7pm and 9pm movies:
# (A) sci-fi at 7pm, horror at 9pm
# (B) sci-fi at 7pm, mystery at 9pm
# (C) sci-fi at 7pm, western at 9pm
# (D) western at 7pm, horror at 9pm
# (E) western at 7pm, mystery at 9pm

options = {
    "A": And(screen[3] == 2, time[3] == 7, screen[0] == 2, time[0] == 9),
    "B": And(screen[3] == 2, time[3] == 7, screen[1] == 2, time[1] == 9),
    "C": And(screen[3] == 2, time[3] == 7, screen[4] == 2, time[4] == 9),
    "D": And(screen[4] == 2, time[4] == 7, screen[0] == 2, time[0] == 9),
    "E": And(screen[4] == 2, time[4] == 7, screen[1] == 2, time[1] == 9),
}

found_options = []
for letter, constr in options.items():
    solver.push()
    solver.add(constr)
    result = solver.check()
    if result == sat:
        m = solver.model()
        found_options.append(letter)
        print(f"Option {letter}: SAT")
        for i in movies:
            print(f"  {names[i]}: screen={m[screen[i]]}, time={m[time[i]]}")
    else:
        print(f"Option {letter}: {result}")
    solver.pop()

print()
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")