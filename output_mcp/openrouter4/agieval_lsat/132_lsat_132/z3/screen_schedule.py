from z3 import *

solver = Solver()

# Movies indices: 0=Horror, 1=Mystery, 2=Romance, 3=Sci-fi, 4=Western
H, M, R, S, W = 0, 1, 2, 3, 4
movies_count = 5

screen = [Int(f"screen_{i}") for i in range(movies_count)]
time = [Int(f"time_{i}") for i in range(movies_count)]

# Domain constraints
for i in range(movies_count):
    solver.add(1 <= screen[i], screen[i] <= 3)
    solver.add(0 <= time[i], time[i] <= 2)

# If a movie is on screen 3, it must be at time 1 (8 PM)
for i in range(movies_count):
    solver.add(Implies(screen[i] == 3, time[i] == 1))

# Screen 1 has exactly 2 movies
solver.add(Sum([If(screen[i] == 1, 1, 0) for i in range(movies_count)]) == 2)
# Screen 2 has exactly 2 movies
solver.add(Sum([If(screen[i] == 2, 1, 0) for i in range(movies_count)]) == 2)
# Screen 3 has exactly 1 movie
solver.add(Sum([If(screen[i] == 3, 1, 0) for i in range(movies_count)]) == 1)

# On screen 1: exactly one 7 PM (time 0) and exactly one 9 PM (time 2)
solver.add(Sum([If(And(screen[i] == 1, time[i] == 0), 1, 0) for i in range(movies_count)]) == 1)
solver.add(Sum([If(And(screen[i] == 1, time[i] == 2), 1, 0) for i in range(movies_count)]) == 1)

# On screen 2: exactly one 7 PM (time 0) and exactly one 9 PM (time 2)
solver.add(Sum([If(And(screen[i] == 2, time[i] == 0), 1, 0) for i in range(movies_count)]) == 1)
solver.add(Sum([If(And(screen[i] == 2, time[i] == 2), 1, 0) for i in range(movies_count)]) == 1)

# On screen 3: exactly one 8 PM (time 1)
solver.add(Sum([If(And(screen[i] == 3, time[i] == 1), 1, 0) for i in range(movies_count)]) == 1)

# Given constraints
# 1. Western begins before horror: time[W] < time[H]
solver.add(time[W] < time[H])

# 2. Sci-fi is not shown on screen 3
solver.add(screen[S] != 3)

# 3. Romance is not shown on screen 2
solver.add(screen[R] != 2)

# 4. Horror and mystery on different screens
solver.add(screen[H] != screen[M])

# Now test each option
# Options: (7PM movie, 9PM movie) on screen 1
options = [
    ("A", S, H),  # sci-fi, horror
    ("B", S, M),  # sci-fi, mystery
    ("C", W, H),  # western, horror
    ("D", W, M),  # western, mystery
    ("E", W, S),  # western, sci-fi
]

found_options = []

for letter, first, second in options:
    solver.push()
    # First movie on screen 1 at 7 PM
    solver.add(screen[first] == 1)
    solver.add(time[first] == 0)
    # Second movie on screen 1 at 9 PM
    solver.add(screen[second] == 1)
    solver.add(time[second] == 2)
    
    if solver.check() == sat:
        found_options.append(letter)
        # Print model for debugging
        # m = solver.model()
        # for i in range(movies_count):
        #     print(f"  Movie {i}: screen={m[screen[i]]}, time={m[time[i]]}")
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