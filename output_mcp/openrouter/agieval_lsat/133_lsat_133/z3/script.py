from z3 import *

# Define movies
movies = ['H','M','R','S','W']
# Variables for screen and time
screen = {m: Int(f'screen_{m}') for m in movies}
time = {m: Int(f'time_{m}') for m in movies}

solver = Solver()

# Domain constraints
for m in movies:
    solver.add(Or(screen[m] == 1, screen[m] == 2, screen[m] == 3))
    solver.add(Or(time[m] == 7, time[m] == 8, time[m] == 9))

# Capacity constraints
# Screens 1 and 2: exactly one movie at 7 and one at 9, none at 8
for s in [1,2]:
    solver.add(Sum([If(And(screen[m]==s, time[m]==7), 1, 0) for m in movies]) == 1)
    solver.add(Sum([If(And(screen[m]==s, time[m]==9), 1, 0) for m in movies]) == 1)
    solver.add(Sum([If(And(screen[m]==s, time[m]==8), 1, 0) for m in movies]) == 0)

# Screen 3: exactly one movie, at time 8
solver.add(Sum([If(screen[m]==3, 1, 0) for m in movies]) == 1)
solver.add(Sum([If(And(screen[m]==3, time[m]==8), 1, 0) for m in movies]) == 1)
# Ensure no movie on screen 3 at other times
solver.add(Sum([If(And(screen[m]==3, time[m]==7), 1, 0) for m in movies]) == 0)
solver.add(Sum([If(And(screen[m]==3, time[m]==9), 1, 0) for m in movies]) == 0)

# Given constraints
# Western before horror
solver.add(time['W'] < time['H'])
# Sci-fi not on screen 3
solver.add(screen['S'] != 3)
# Romance not on screen 2
solver.add(screen['R'] != 2)
# Horror and mystery different screens
solver.add(screen['H'] != screen['M'])

# Additional condition: sci-fi and romance on same screen
solver.add(screen['S'] == screen['R'])

# Option constraints definitions
opt_a = (time['W'] == 7)
opt_b = (time['S'] == 9)
opt_c = (time['M'] == 8)
opt_d = (time['R'] == 9)
opt_e = (time['H'] == 8)

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