from z3 import *

movies = ['H', 'M', 'R', 'S', 'W']
screen = {m: Int(f'screen_{m}') for m in movies}
time = {m: Int(f'time_{m}') for m in movies}

solver = Solver()

for m in movies:
    solver.add(screen[m] >= 1, screen[m] <= 3)
    solver.add(Or(time[m] == 7, time[m] == 8, time[m] == 9))

for m in movies:
    solver.add(If(screen[m] == 3, time[m] == 8, Or(time[m] == 7, time[m] == 9)))
    solver.add(If(Or(screen[m] == 1, screen[m] == 2), Or(time[m] == 7, time[m] == 9), time[m] == 8))

for s in [1, 2]:
    solver.add(Sum([If(screen[m] == s, 1, 0) for m in movies]) == 2)
solver.add(Sum([If(screen[m] == 3, 1, 0) for m in movies]) == 1)

for t in [7, 9]:
    solver.add(Sum([If(time[m] == t, 1, 0) for m in movies]) == 2)
solver.add(Sum([If(time[m] == 8, 1, 0) for m in movies]) == 1)

solver.add(time['W'] < time['H'])
solver.add(screen['S'] != 3)
solver.add(screen['R'] != 2)
solver.add(screen['H'] != screen['M'])
solver.add(screen['W'] == screen['S'])

# Let's check if there's any other constraint I missed.
# "Each movie is shown exactly once, on one of the theater's three screens: screens 1, 2, and 3."
# "Screens 1 and 2 show two movies each, one beginning at 7 P.M. and the other at 9 P.M."
# "Screen 3 shows exactly one movie, at 8 P.M."
# "The western begins at some time before the horror film does."
# "The sci-fi film is not shown on screen 3."
# "The romance is not shown on screen 2."
# "The horror film and the mystery are shown on different screens."

# Wait, are there any other implicit constraints?
# "Each movie is shown exactly once" - Yes.
# "one beginning at 7 P.M. and the other at 9 P.M." - This implies that for each screen 1 and 2, one movie is at 7 and one is at 9.
# My current constraint:
# solver.add(If(Or(screen[m] == 1, screen[m] == 2), Or(time[m] == 7, time[m] == 9), time[m] == 8))
# This only says that if a movie is on screen 1 or 2, it's at 7 or 9.
# It does NOT say that for each screen, one is 7 and one is 9.
# Let's add that.

for s in [1, 2]:
    solver.add(Sum([If(And(screen[m] == s, time[m] == 7), 1, 0) for m in movies]) == 1)
    solver.add(Sum([If(And(screen[m] == s, time[m] == 9), 1, 0) for m in movies]) == 1)

options = {
    "A": screen['H'] == 2,
    "B": time['M'] == 9,
    "C": screen['R'] == 3,
    "D": time['S'] == 7,
    "E": time['W'] == 8
}

found_options = []
for letter, constr in options.items():
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
    solver.pop()

print(f"Found options: {found_options}")