from z3 import *

# Movies: horror, mystery, romance, scifi, western
# Let's assign each movie a screen (1,2,3) and a time slot.
# Screens 1 and 2 have two movies each: one at 7pm (slot 0) and one at 9pm (slot 1).
# Screen 3 has exactly one movie at 8pm (slot 2).

# We'll model each movie's screen and time slot.
# screen[m] in {1,2,3}
# time[m] in {0,1,2} where 0=7pm, 1=9pm, 2=8pm
# Constraints:
# - Screen 3 only shows at 8pm (time=2), and only one movie.
# - Screens 1 and 2 show at 7pm and 9pm (times 0 and 1), exactly two movies each.
# - Western before horror: time(western) < time(horror)
# - Sci-fi not on screen 3
# - Romance not on screen 2
# - Horror and mystery on different screens

movies = ['horror', 'mystery', 'romance', 'scifi', 'western']
# Indices
H, M, R, S, W = 0, 1, 2, 3, 4

screen = [Int(f'screen_{m}') for m in movies]
time = [Int(f'time_{m}') for m in movies]

solver = Solver()

# Domains
for m in range(5):
    solver.add(screen[m] >= 1, screen[m] <= 3)
    solver.add(time[m] >= 0, time[m] <= 2)

# Screen 3 only shows at 8pm (time=2), and exactly one movie on screen 3.
# So: if screen[m] == 3 then time[m] == 2
for m in range(5):
    solver.add(Implies(screen[m] == 3, time[m] == 2))

# Exactly one movie on screen 3
solver.add(Sum([If(screen[m] == 3, 1, 0) for m in range(5)]) == 1)

# Screens 1 and 2: each shows exactly two movies, at times 0 and 1 (7pm and 9pm)
for scr in [1, 2]:
    solver.add(Sum([If(screen[m] == scr, 1, 0) for m in range(5)]) == 2)
    # For each screen 1 or 2, the two movies must have times 0 and 1 (one each)
    solver.add(Sum([If(And(screen[m] == scr, time[m] == 0), 1, 0) for m in range(5)]) == 1)
    solver.add(Sum([If(And(screen[m] == scr, time[m] == 1), 1, 0) for m in range(5)]) == 1)

# No movie on screen 3 at time 0 or 1 (already implied, but add explicitly)
solver.add(Sum([If(And(screen[m] == 3, time[m] == 0), 1, 0) for m in range(5)]) == 0)
solver.add(Sum([If(And(screen[m] == 3, time[m] == 1), 1, 0) for m in range(5)]) == 0)

# Western before horror: time(W) < time(H)
solver.add(time[W] < time[H])

# Sci-fi not on screen 3
solver.add(screen[S] != 3)

# Romance not on screen 2
solver.add(screen[R] != 2)

# Horror and mystery on different screens
solver.add(screen[H] != screen[M])

# Each movie has a unique (screen, time) combination? Actually each movie is distinct,
# and each screen-time slot can have at most one movie. Let's enforce uniqueness:
# For each screen-time pair, at most one movie.
for scr in [1, 2, 3]:
    for t in [0, 1, 2]:
        solver.add(Sum([If(And(screen[m] == scr, time[m] == t), 1, 0) for m in range(5)]) <= 1)

# Now evaluate each option.
# Each option lists two movies for screen 2, 7pm first then 9pm.
# So for option X: the first movie is on screen 2 at time 0, second on screen 2 at time 1.

options = {
    "A": ("scifi", "horror"),
    "B": ("scifi", "mystery"),
    "C": ("scifi", "western"),
    "D": ("western", "horror"),
    "E": ("western", "mystery")
}

movie_index = {"horror": H, "mystery": M, "romance": R, "scifi": S, "western": W}

found_options = []

for letter, (first, second) in options.items():
    solver.push()
    # first movie on screen 2 at time 0
    solver.add(screen[movie_index[first]] == 2)
    solver.add(time[movie_index[first]] == 0)
    # second movie on screen 2 at time 1
    solver.add(screen[movie_index[second]] == 2)
    solver.add(time[movie_index[second]] == 1)
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