from z3 import *

# Movies: horror (H), mystery (M), romance (R), sci-fi (S), western (W)
# Screens: 1, 2, 3
# Times: 7PM, 8PM, 9PM
# Screen 1: two movies at 7PM and 9PM
# Screen 2: two movies at 7PM and 9PM
# Screen 3: one movie at 8PM

# We'll model each movie's screen and time.
# Let's use Ints for screen and time.
# screen[movie] in {1,2,3}
# time[movie] in {7,8,9} (representing 7PM, 8PM, 9PM)

H, M, R, S, W = Ints('H M R S W')
movies = [H, M, R, S, W]
movie_names = ['H', 'M', 'R', 'S', 'W']

solver = Solver()

# Domain constraints: each movie's screen is 1,2,3
for mv in movies:
    solver.add(Or([mv == s for s in [1,2,3]]))

# Each movie's time is 7,8,9
# We'll create time variables
tH, tM, tR, tS, tW = Ints('tH tM tR tS tW')
times = [tH, tM, tR, tS, tW]
for t in times:
    solver.add(Or([t == v for v in [7,8,9]]))

# Screen 1 shows two movies: one at 7, one at 9
# Screen 2 shows two movies: one at 7, one at 9
# Screen 3 shows exactly one movie at 8

# For each screen, the movies on that screen must have appropriate times.
# Screen 1: exactly 2 movies, times 7 and 9
# Screen 2: exactly 2 movies, times 7 and 9
# Screen 3: exactly 1 movie, time 8

# Count movies per screen
for scr in [1,2,3]:
    count_on_screen = Sum([If(mv == scr, 1, 0) for mv in movies])
    if scr == 3:
        solver.add(count_on_screen == 1)
    else:
        solver.add(count_on_screen == 2)

# For screen 1: the two movies have times 7 and 9
# For screen 2: the two movies have times 7 and 9
# For screen 3: the one movie has time 8

# Let's encode: for each screen, the set of times of movies on that screen must match.
# Screen 1: times {7,9}
for scr in [1,2]:
    # At least one movie on this screen at 7
    solver.add(Sum([If(And(mv == scr, t == 7), 1, 0) for mv, t in zip(movies, times)]) == 1)
    # At least one movie on this screen at 9
    solver.add(Sum([If(And(mv == scr, t == 9), 1, 0) for mv, t in zip(movies, times)]) == 1)
    # No movie on this screen at 8
    solver.add(Sum([If(And(mv == scr, t == 8), 1, 0) for mv, t in zip(movies, times)]) == 0)

# Screen 3: exactly one movie at 8
solver.add(Sum([If(And(mv == 3, t == 8), 1, 0) for mv, t in zip(movies, times)]) == 1)
solver.add(Sum([If(And(mv == 3, t == 7), 1, 0) for mv, t in zip(movies, times)]) == 0)
solver.add(Sum([If(And(mv == 3, t == 9), 1, 0) for mv, t in zip(movies, times)]) == 0)

# Each movie has exactly one time
# Already enforced by domain constraints, but also ensure each movie has exactly one time value
# (already covered by Or constraints above)

# Condition: The western begins at some time before the horror film does.
solver.add(tW < tH)

# Condition: The sci-fi film is not shown on screen 3.
solver.add(S != 3)

# Condition: The romance is not shown on screen 2.
solver.add(R != 2)

# Condition: The horror film and the mystery are shown on different screens.
solver.add(H != M)

# Additional condition from the question: The western and the sci-fi film are scheduled to be shown on the same screen.
solver.add(W == S)

# Now evaluate each option
# (A) The horror film is shown on screen 2.
opt_a = (H == 2)

# (B) The mystery begins at 9 P.M.
opt_b = (tM == 9)

# (C) The romance is shown on screen 3.
opt_c = (R == 3)

# (D) The sci-fi film begins at 7 P.M.
opt_d = (tS == 7)

# (E) The western begins at 8 P.M.
opt_e = (tW == 8)

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