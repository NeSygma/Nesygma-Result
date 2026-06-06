from z3 import *

solver = Solver()

# Movies
movies = ['H', 'M', 'R', 'S', 'W']
H, M, R, S, W = 'H', 'M', 'R', 'S', 'W'

# Variables
screen = {m: Int(f"screen_{m}") for m in movies}
time = {m: Int(f"time_{m}") for m in movies}

# Domain constraints
for m in movies:
    solver.add(screen[m] >= 1, screen[m] <= 3)
    solver.add(Or(time[m] == 7, time[m] == 8, time[m] == 9))

# No two movies share the same (screen, time) pair
for i in range(len(movies)):
    for j in range(i+1, len(movies)):
        mi, mj = movies[i], movies[j]
        solver.add(Not(And(screen[mi] == screen[mj], time[mi] == time[mj])))

# Screen 3 constraints: exactly one movie, at time 8
solver.add(Sum([If(screen[m] == 3, 1, 0) for m in movies]) == 1)
# If on screen 3, must be at 8 PM
for m in movies:
    solver.add(Implies(screen[m] == 3, time[m] == 8))

# Screen 1: exactly 2 movies, one at 7 and one at 9
solver.add(Sum([If(screen[m] == 1, 1, 0) for m in movies]) == 2)
solver.add(Sum([If(And(screen[m] == 1, time[m] == 7), 1, 0) for m in movies]) == 1)
solver.add(Sum([If(And(screen[m] == 1, time[m] == 9), 1, 0) for m in movies]) == 1)

# Screen 2: exactly 2 movies, one at 7 and one at 9
solver.add(Sum([If(screen[m] == 2, 1, 0) for m in movies]) == 2)
solver.add(Sum([If(And(screen[m] == 2, time[m] == 7), 1, 0) for m in movies]) == 1)
solver.add(Sum([If(And(screen[m] == 2, time[m] == 9), 1, 0) for m in movies]) == 1)

# Constraint 4: Western begins at some time before horror
solver.add(time[W] < time[H])

# Constraint 5: Sci-fi not on screen 3
solver.add(screen[S] != 3)

# Constraint 6: Romance not on screen 2
solver.add(screen[R] != 2)

# Constraint 7: Horror and mystery on different screens
solver.add(screen[H] != screen[M])

# Added condition: Western and sci-fi on same screen
solver.add(screen[W] == screen[S])

# Now test each option
# Option A: The horror film is shown on screen 2.
opt_a = (screen[H] == 2)

# Option B: The mystery begins at 9 P.M.
opt_b = (time[M] == 9)

# Option C: The romance is shown on screen 3.
opt_c = (screen[R] == 3)

# Option D: The sci-fi film begins at 7 P.M.
opt_d = (time[S] == 7)

# Option E: The western begins at 8 P.M.
opt_e = (time[W] == 8)

found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(constr)
    result = solver.check()
    if result == sat:
        found_options.append(letter)
        # Print model for debugging
        m = solver.model()
        print(f"Option {letter} is SAT. Model:")
        for movie in movies:
            print(f"  {movie}: screen={m[screen[movie]]}, time={m[time[movie]]}")
    else:
        print(f"Option {letter} is UNSAT")
    solver.pop()

print("---")
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")