from z3 import *

solver = Solver()

movies = ['horror', 'mystery', 'romance', 'scifi', 'western']
screen = {m: Int(f'screen_{m}') for m in movies}
time = {m: Int(f'time_{m}') for m in movies}

for m in movies:
    solver.add(Or(screen[m] == 1, screen[m] == 2, screen[m] == 3))
    solver.add(Or(time[m] == 7, time[m] == 8, time[m] == 9))

# Screen-time constraints
for m in movies:
    solver.add(Implies(screen[m] == 1, Or(time[m] == 7, time[m] == 9)))
    solver.add(Implies(screen[m] == 2, Or(time[m] == 7, time[m] == 9)))
    solver.add(Implies(screen[m] == 3, time[m] == 8))

# Exactly 2 movies on screen 1, 2 on screen 2, 1 on screen 3
solver.add(Sum([If(screen[m] == 1, 1, 0) for m in movies]) == 2)
solver.add(Sum([If(screen[m] == 2, 1, 0) for m in movies]) == 2)
solver.add(Sum([If(screen[m] == 3, 1, 0) for m in movies]) == 1)

# Exactly 2 movies at 7pm, 1 at 8pm, 2 at 9pm
solver.add(Sum([If(time[m] == 7, 1, 0) for m in movies]) == 2)
solver.add(Sum([If(time[m] == 8, 1, 0) for m in movies]) == 1)
solver.add(Sum([If(time[m] == 9, 1, 0) for m in movies]) == 2)

# All movies must be on different (screen, time) slots
for i in range(len(movies)):
    for j in range(i+1, len(movies)):
        m1, m2 = movies[i], movies[j]
        solver.add(Not(And(screen[m1] == screen[m2], time[m1] == time[m2])))

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

# Now test each answer choice by checking if it MUST be true
# We check if the negation is UNSAT (meaning it must be true)
options = [
    ("A", time['western'] == 7),
    ("B", time['scifi'] == 9),
    ("C", time['mystery'] == 8),
    ("D", time['romance'] == 9),
    ("E", time['horror'] == 8),
]

must_be_true = []
for letter, constr in options:
    s = Solver()
    # Add all base constraints
    for m in movies:
        s.add(Or(screen[m] == 1, screen[m] == 2, screen[m] == 3))
        s.add(Or(time[m] == 7, time[m] == 8, time[m] == 9))
        s.add(Implies(screen[m] == 1, Or(time[m] == 7, time[m] == 9)))
        s.add(Implies(screen[m] == 2, Or(time[m] == 7, time[m] == 9)))
        s.add(Implies(screen[m] == 3, time[m] == 8))
    s.add(Sum([If(screen[m] == 1, 1, 0) for m in movies]) == 2)
    s.add(Sum([If(screen[m] == 2, 1, 0) for m in movies]) == 2)
    s.add(Sum([If(screen[m] == 3, 1, 0) for m in movies]) == 1)
    s.add(Sum([If(time[m] == 7, 1, 0) for m in movies]) == 2)
    s.add(Sum([If(time[m] == 8, 1, 0) for m in movies]) == 1)
    s.add(Sum([If(time[m] == 9, 1, 0) for m in movies]) == 2)
    for i in range(len(movies)):
        for j in range(i+1, len(movies)):
            m1, m2 = movies[i], movies[j]
            s.add(Not(And(screen[m1] == screen[m2], time[m1] == time[m2])))
    s.add(time['western'] < time['horror'])
    s.add(screen['scifi'] != 3)
    s.add(screen['romance'] != 2)
    s.add(screen['horror'] != screen['mystery'])
    s.add(screen['scifi'] == screen['romance'])
    # Add negation of the option
    s.add(Not(constr))
    if s.check() == unsat:
        must_be_true.append(letter)

print(f"Must be true options: {must_be_true}")
if len(must_be_true) == 1:
    print("STATUS: sat")
    print(f"answer:{must_be_true[0]}")
elif len(must_be_true) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple must-be-true options {must_be_true}")
else:
    print("STATUS: unsat")
    print("Refine: No must-be-true options found")