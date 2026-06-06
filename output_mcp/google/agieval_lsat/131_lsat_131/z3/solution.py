from z3 import *

# Movies
movies = ['H', 'M', 'R', 'S', 'W']
# Slots: (screen, time)
slots = [(1, 7), (1, 9), (2, 7), (2, 9), (3, 8)]

# Variables
# movie_screen[m] is the screen of movie m
# movie_time[m] is the time of movie m
movie_screen = {m: Int(f'screen_{m}') for m in movies}
movie_time = {m: Int(f'time_{m}') for m in movies}

solver = Solver()

# Each movie is in one of the slots
for m in movies:
    solver.add(Or([And(movie_screen[m] == s, movie_time[m] == t) for s, t in slots]))

# Each slot is used exactly once (all slots distinct)
# We can use a list of pairs and ensure they are distinct
movie_slots = [And(movie_screen[m] == s, movie_time[m] == t) for m in movies for s, t in slots]
# Actually, simpler:
# For each slot, exactly one movie is assigned to it
for s, t in slots:
    solver.add(Sum([If(And(movie_screen[m] == s, movie_time[m] == t), 1, 0) for m in movies]) == 1)

# Constraints
# 1. The western begins at some time before the horror film does.
solver.add(movie_time['W'] < movie_time['H'])

# 2. The sci-fi film is not shown on screen 3.
solver.add(movie_screen['S'] != 3)

# 3. The romance is not shown on screen 2.
solver.add(movie_screen['R'] != 2)

# 4. The horror film and the mystery are shown on different screens.
solver.add(movie_screen['H'] != movie_screen['M'])

# Condition: The romance is scheduled to begin before the western does.
solver.add(movie_time['R'] < movie_time['W'])

# Options
options = {
    "A": movie_screen['H'] == 1,
    "B": movie_time['M'] == 7,
    "C": movie_screen['M'] == 2,
    "D": movie_time['S'] == 9,
    "E": movie_screen['S'] == 2
}

found_options = []
for letter, constr in options.items():
    solver.push()
    solver.add(Not(constr))
    if solver.check() == unsat:
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