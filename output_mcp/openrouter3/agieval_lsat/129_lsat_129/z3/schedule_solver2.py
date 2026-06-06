from z3 import *

# Define movie types
movies = ["horror", "mystery", "romance", "sci-fi", "western"]
screens = [1, 2, 3]
times = [7, 8, 9]  # PM

# Create variables: for each movie, which screen and time
movie_screen = {m: Int(f"screen_{m}") for m in movies}
movie_time = {m: Int(f"time_{m}") for m in movies}

# Domain constraints: each movie on one screen, one time
base_constraints = []
for m in movies:
    base_constraints.append(Or([movie_screen[m] == s for s in screens]))
    base_constraints.append(Or([movie_time[m] == t for t in times]))

# Screen capacity constraints
screen_time_count = {}
for s in screens:
    for t in times:
        count = Sum([If(And(movie_screen[m] == s, movie_time[m] == t), 1, 0) for m in movies])
        screen_time_count[(s, t)] = count

# Screen 1: exactly 2 movies total, one at 7, one at 9
base_constraints.append(Sum([screen_time_count[(1, t)] for t in times]) == 2)
base_constraints.append(screen_time_count[(1, 7)] == 1)
base_constraints.append(screen_time_count[(1, 9)] == 1)
base_constraints.append(screen_time_count[(1, 8)] == 0)

# Screen 2: exactly 2 movies total, one at 7, one at 9
base_constraints.append(Sum([screen_time_count[(2, t)] for t in times]) == 2)
base_constraints.append(screen_time_count[(2, 7)] == 1)
base_constraints.append(screen_time_count[(2, 9)] == 1)
base_constraints.append(screen_time_count[(2, 8)] == 0)

# Screen 3: exactly 1 movie at 8
base_constraints.append(Sum([screen_time_count[(3, t)] for t in times]) == 1)
base_constraints.append(screen_time_count[(3, 8)] == 1)
base_constraints.append(screen_time_count[(3, 7)] == 0)
base_constraints.append(screen_time_count[(3, 9)] == 0)

# Each movie assigned to exactly one screen/time combination
for m in movies:
    base_constraints.append(Sum([If(And(movie_screen[m] == s, movie_time[m] == t), 1, 0) for s in screens for t in times]) == 1)

# Constraint 1: Western begins before horror film
base_constraints.append(movie_time["western"] < movie_time["horror"])

# Constraint 2: Sci-fi not on screen 3
base_constraints.append(movie_screen["sci-fi"] != 3)

# Constraint 3: Romance not on screen 2
base_constraints.append(movie_screen["romance"] != 2)

# Constraint 4: Horror and mystery on different screens
base_constraints.append(movie_screen["horror"] != movie_screen["mystery"])

# Now test each option for screen 2
# Option A: sci-fi at 7 PM, horror at 9 PM on screen 2
opt_a = And(movie_screen["sci-fi"] == 2, movie_time["sci-fi"] == 7,
            movie_screen["horror"] == 2, movie_time["horror"] == 9)

# Option B: sci-fi at 7 PM, mystery at 9 PM on screen 2
opt_b = And(movie_screen["sci-fi"] == 2, movie_time["sci-fi"] == 7,
            movie_screen["mystery"] == 2, movie_time["mystery"] == 9)

# Option C: sci-fi at 7 PM, western at 9 PM on screen 2
opt_c = And(movie_screen["sci-fi"] == 2, movie_time["sci-fi"] == 7,
            movie_screen["western"] == 2, movie_time["western"] == 9)

# Option D: western at 7 PM, horror at 9 PM on screen 2
opt_d = And(movie_screen["western"] == 2, movie_time["western"] == 7,
            movie_screen["horror"] == 2, movie_time["horror"] == 9)

# Option E: western at 7 PM, mystery at 9 PM on screen 2
opt_e = And(movie_screen["western"] == 2, movie_time["western"] == 7,
            movie_screen["mystery"] == 2, movie_time["mystery"] == 9)

# For each option, check if adding it makes the problem UNSAT
impossible_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    s = Solver()
    s.add(base_constraints)
    s.add(constr)
    if s.check() == unsat:
        impossible_options.append(letter)

# According to the problem, exactly one option CANNOT be accurate
if len(impossible_options) == 1:
    print("STATUS: sat")
    print(f"answer:{impossible_options[0]}")
elif len(impossible_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple impossible options found {impossible_options}")
else:
    print("STATUS: unsat")
    print("Refine: No impossible options found")