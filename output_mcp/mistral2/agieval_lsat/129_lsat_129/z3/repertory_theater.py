from z3 import *

# Movies
movies = ["horror", "mystery", "romance", "sci-fi", "western"]
movie_to_idx = {m: i for i, m in enumerate(movies)}

# Screens and times
screens = [1, 2, 3]
times = [0, 1, 2]  # 0: 7 P.M., 1: 8 P.M., 2: 9 P.M.

# Variables
screen = [Int(f"screen_{m}") for m in movies]
time = [Int(f"time_{m}") for m in movies]

solver = Solver()

# Each movie is assigned to exactly one screen and one time
for m in movies:
    solver.add(Or([screen[movie_to_idx[m]] == s for s in screens]))
    solver.add(Or([time[movie_to_idx[m]] == t for t in times]))

# Screen 3 has exactly one movie at 8 P.M. (time = 1)
solver.add(Sum([If(And(screen[movie_to_idx[m]] == 3, time[movie_to_idx[m]] == 1), 1, 0) for m in movies]) == 1)

# Screens 1 and 2 have two movies each, at 7 P.M. and 9 P.M.
for s in [1, 2]:
    solver.add(Sum([If(screen[movie_to_idx[m]] == s, 1, 0) for m in movies]) == 2)
    solver.add(Sum([If(And(screen[movie_to_idx[m]] == s, time[movie_to_idx[m]] == 0), 1, 0) for m in movies]) == 1)
    solver.add(Sum([If(And(screen[movie_to_idx[m]] == s, time[movie_to_idx[m]] == 2), 1, 0) for m in movies]) == 1)

# The western begins at some time before the horror film
western_idx = movie_to_idx["western"]
horror_idx = movie_to_idx["horror"]
solver.add(time[western_idx] < time[horror_idx])

# The sci-fi film is not shown on screen 3
sci_fi_idx = movie_to_idx["sci-fi"]
solver.add(screen[sci_fi_idx] != 3)

# The romance is not shown on screen 2
romance_idx = movie_to_idx["romance"]
solver.add(screen[romance_idx] != 2)

# The horror film and the mystery are shown on different screens
mystery_idx = movie_to_idx["mystery"]
solver.add(screen[horror_idx] != screen[mystery_idx])

# All movies are distinct on screens and times (no two movies on the same screen at the same time)
for i in range(len(movies)):
    for j in range(i + 1, len(movies)):
        solver.add(Not(And(screen[i] == screen[j], time[i] == time[j])))

# Base constraints for answer choices
# Option A: screen 2 has sci-fi at 7 P.M. and horror at 9 P.M.
opt_a_constr = And(
    screen[movie_to_idx["sci-fi"]] == 2,
    time[movie_to_idx["sci-fi"]] == 0,
    screen[movie_to_idx["horror"]] == 2,
    time[movie_to_idx["horror"]] == 2
)

# Option B: screen 2 has sci-fi at 7 P.M. and mystery at 9 P.M.
opt_b_constr = And(
    screen[movie_to_idx["sci-fi"]] == 2,
    time[movie_to_idx["sci-fi"]] == 0,
    screen[movie_to_idx["mystery"]] == 2,
    time[movie_to_idx["mystery"]] == 2
)

# Option C: screen 2 has sci-fi at 7 P.M. and western at 9 P.M.
opt_c_constr = And(
    screen[movie_to_idx["sci-fi"]] == 2,
    time[movie_to_idx["sci-fi"]] == 0,
    screen[movie_to_idx["western"]] == 2,
    time[movie_to_idx["western"]] == 2
)

# Option D: screen 2 has western at 7 P.M. and horror at 9 P.M.
opt_d_constr = And(
    screen[movie_to_idx["western"]] == 2,
    time[movie_to_idx["western"]] == 0,
    screen[movie_to_idx["horror"]] == 2,
    time[movie_to_idx["horror"]] == 2
)

# Option E: screen 2 has western at 7 P.M. and mystery at 9 P.M.
opt_e_constr = And(
    screen[movie_to_idx["western"]] == 2,
    time[movie_to_idx["western"]] == 0,
    screen[movie_to_idx["mystery"]] == 2,
    time[movie_to_idx["mystery"]] == 2
)

# Evaluate each option
found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
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