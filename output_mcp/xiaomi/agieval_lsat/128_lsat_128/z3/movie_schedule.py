from z3 import *

solver = Solver()

# Define the movies
movies = ['horror', 'mystery', 'romance', 'sci-fi', 'western']

# Define the screens and times
# Screen 1: 7pm, 9pm
# Screen 2: 7pm, 9pm
# Screen 3: 8pm

# We'll create variables for each movie's screen and time
# screen[m] = which screen (1, 2, 3)
# time[m] = which time slot (7, 8, 9)

screen = {m: Int(f'screen_{m}') for m in movies}
time = {m: Int(f'time_{m}') for m in movies}

# Domain constraints
for m in movies:
    solver.add(Or(screen[m] == 1, screen[m] == 2, screen[m] == 3))
    solver.add(Or(time[m] == 7, time[m] == 8, time[m] == 9))

# Each movie is shown exactly once (already implicit in variable assignment)

# Screen constraints:
# Screen 1: two movies, one at 7pm, one at 9pm
# Screen 2: two movies, one at 7pm, one at 9pm
# Screen 3: one movie at 8pm

# Count movies per screen
for s in [1, 2]:
    solver.add(Sum([If(screen[m] == s, 1, 0) for m in movies]) == 2)
solver.add(Sum([If(screen[m] == 3, 1, 0) for m in movies]) == 1)

# Time constraints per screen
# Screen 1: exactly one movie at 7pm, one at 9pm
solver.add(Sum([If(And(screen[m] == 1, time[m] == 7), 1, 0) for m in movies]) == 1)
solver.add(Sum([If(And(screen[m] == 1, time[m] == 9), 1, 0) for m in movies]) == 1)

# Screen 2: exactly one movie at 7pm, one at 9pm
solver.add(Sum([If(And(screen[m] == 2, time[m] == 7), 1, 0) for m in movies]) == 1)
solver.add(Sum([If(And(screen[m] == 2, time[m] == 9), 1, 0) for m in movies]) == 1)

# Screen 3: exactly one movie at 8pm
solver.add(Sum([If(And(screen[m] == 3, time[m] == 8), 1, 0) for m in movies]) == 1)

# Additional constraints from problem statement:
# 1. Western begins before horror film
solver.add(time['western'] < time['horror'])

# 2. Sci-fi not on screen 3
solver.add(screen['sci-fi'] != 3)

# 3. Romance not on screen 2
solver.add(screen['romance'] != 2)

# 4. Horror and mystery on different screens
solver.add(screen['horror'] != screen['mystery'])

# Now define each option as constraints
def option_constraints(opt):
    """Return list of constraints for a given option."""
    cons = []
    if opt == 'A':
        # Screen 1: romance at 7, horror at 9
        cons.append(And(screen['romance'] == 1, time['romance'] == 7))
        cons.append(And(screen['horror'] == 1, time['horror'] == 9))
        # Screen 2: western at 7, sci-fi at 9
        cons.append(And(screen['western'] == 2, time['western'] == 7))
        cons.append(And(screen['sci-fi'] == 2, time['sci-fi'] == 9))
        # Screen 3: mystery at 8
        cons.append(And(screen['mystery'] == 3, time['mystery'] == 8))
    elif opt == 'B':
        # Screen 1: mystery at 7, romance at 9
        cons.append(And(screen['mystery'] == 1, time['mystery'] == 7))
        cons.append(And(screen['romance'] == 1, time['romance'] == 9))
        # Screen 2: horror at 7, sci-fi at 9
        cons.append(And(screen['horror'] == 2, time['horror'] == 7))
        cons.append(And(screen['sci-fi'] == 2, time['sci-fi'] == 9))
        # Screen 3: western at 8
        cons.append(And(screen['western'] == 3, time['western'] == 8))
    elif opt == 'C':
        # Screen 1: western at 7, sci-fi at 9
        cons.append(And(screen['western'] == 1, time['western'] == 7))
        cons.append(And(screen['sci-fi'] == 1, time['sci-fi'] == 9))
        # Screen 2: mystery at 7, horror at 9
        cons.append(And(screen['mystery'] == 2, time['mystery'] == 7))
        cons.append(And(screen['horror'] == 2, time['horror'] == 9))
        # Screen 3: romance at 8
        cons.append(And(screen['romance'] == 3, time['romance'] == 8))
    elif opt == 'D':
        # Screen 1: romance at 7, mystery at 9
        cons.append(And(screen['romance'] == 1, time['romance'] == 7))
        cons.append(And(screen['mystery'] == 1, time['mystery'] == 9))
        # Screen 2: western at 7, horror at 9
        cons.append(And(screen['western'] == 2, time['western'] == 7))
        cons.append(And(screen['horror'] == 2, time['horror'] == 9))
        # Screen 3: sci-fi at 8
        cons.append(And(screen['sci-fi'] == 3, time['sci-fi'] == 8))
    elif opt == 'E':
        # Screen 1: western at 7, mystery at 9
        cons.append(And(screen['western'] == 1, time['western'] == 7))
        cons.append(And(screen['mystery'] == 1, time['mystery'] == 9))
        # Screen 2: sci-fi at 7, romance at 9
        cons.append(And(screen['sci-fi'] == 2, time['sci-fi'] == 7))
        cons.append(And(screen['romance'] == 2, time['romance'] == 9))
        # Screen 3: horror at 8
        cons.append(And(screen['horror'] == 3, time['horror'] == 8))
    return cons

found_options = []
for letter in ['A', 'B', 'C', 'D', 'E']:
    solver.push()
    solver.add(option_constraints(letter))
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