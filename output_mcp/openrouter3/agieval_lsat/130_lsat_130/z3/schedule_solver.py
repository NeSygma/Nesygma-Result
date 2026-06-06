from z3 import *

# Create solver
solver = Solver()

# Define movies and screens
movies = ['horror', 'mystery', 'romance', 'sci-fi', 'western']
screens = [1, 2, 3]
times = [7, 8, 9]  # 7PM, 8PM, 9PM

# Create variables: screen assignment and start time for each movie
screen = {m: Int(f'screen_{m}') for m in movies}
start_time = {m: Int(f'stime_{m}') for m in movies}

# Domain constraints for screens
for m in movies:
    solver.add(screen[m] >= 1)
    solver.add(screen[m] <= 3)

# Domain constraints for times
for m in movies:
    solver.add(Or([start_time[m] == t for t in times]))

# Screen capacity constraints:
# Screen 1: exactly 2 movies, times 7 and 9
# Screen 2: exactly 2 movies, times 7 and 9  
# Screen 3: exactly 1 movie, time 8

# Count movies per screen
for s in screens:
    if s == 3:
        # Screen 3: exactly 1 movie at 8PM
        movies_on_s3 = [If(screen[m] == s, 1, 0) for m in movies]
        solver.add(Sum(movies_on_s3) == 1)
        # The movie on screen 3 must be at 8PM
        for m in movies:
            solver.add(Implies(screen[m] == s, start_time[m] == 8))
    else:
        # Screens 1 and 2: exactly 2 movies each
        movies_on_s = [If(screen[m] == s, 1, 0) for m in movies]
        solver.add(Sum(movies_on_s) == 2)
        # Movies on screens 1 and 2 must be at 7PM or 9PM
        for m in movies:
            solver.add(Implies(screen[m] == s, Or(start_time[m] == 7, start_time[m] == 9)))

# Each time slot can have at most one movie per screen
# Actually, since we have exactly the right number of slots, we need to ensure
# that on each screen, the two movies (if any) have different times
for s in [1, 2]:
    movies_on_s = [m for m in movies if m in movies]  # all movies
    # For screens 1 and 2, we need exactly one movie at 7PM and one at 9PM
    movies_at_7 = [If(And(screen[m] == s, start_time[m] == 7), 1, 0) for m in movies]
    movies_at_9 = [If(And(screen[m] == s, start_time[m] == 9), 1, 0) for m in movies]
    solver.add(Sum(movies_at_7) == 1)
    solver.add(Sum(movies_at_9) == 1)

# Constraint 1: Western begins before horror film
solver.add(start_time['western'] < start_time['horror'])

# Constraint 2: Sci-fi not on screen 3
solver.add(screen['sci-fi'] != 3)

# Constraint 3: Romance not on screen 2
solver.add(screen['romance'] != 2)

# Constraint 4: Horror and mystery on different screens
solver.add(screen['horror'] != screen['mystery'])

# Additional condition: Western and sci-fi on same screen
solver.add(screen['western'] == screen['sci-fi'])

# Now test each answer choice
found_options = []

# Option A: The horror film is shown on screen 2
solver.push()
solver.add(screen['horror'] == 2)
if solver.check() == sat:
    found_options.append('A')
solver.pop()

# Option B: The mystery begins at 9 P.M.
solver.push()
solver.add(start_time['mystery'] == 9)
if solver.check() == sat:
    found_options.append('B')
solver.pop()

# Option C: The romance is shown on screen 3
solver.push()
solver.add(screen['romance'] == 3)
if solver.check() == sat:
    found_options.append('C')
solver.pop()

# Option D: The sci-fi film begins at 7 P.M.
solver.push()
solver.add(start_time['sci-fi'] == 7)
if solver.check() == sat:
    found_options.append('D')
solver.pop()

# Option E: The western begins at 8 P.M.
solver.push()
solver.add(start_time['western'] == 8)
if solver.check() == sat:
    found_options.append('E')
solver.pop()

# Output results
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")