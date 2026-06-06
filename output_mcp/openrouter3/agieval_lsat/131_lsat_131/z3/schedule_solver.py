from z3 import *

# Create solver
solver = Solver()

# Define movies and screens
movies = ['H', 'M', 'R', 'S', 'W']
screens = [1, 2, 3]
times = [7, 8, 9]  # 7PM, 8PM, 9PM

# Create variables: screen assignment and start time for each movie
screen = {m: Int(f'screen_{m}') for m in movies}
start_time = {m: Int(f'stime_{m}') for m in movies}

# Domain constraints for screens
for m in movies:
    solver.add(screen[m] >= 1, screen[m] <= 3)

# Domain constraints for start times
for m in movies:
    solver.add(Or([start_time[m] == t for t in times]))

# Screen capacity constraints:
# Screen 1: exactly 2 movies at 7PM and 9PM
# Screen 2: exactly 2 movies at 7PM and 9PM  
# Screen 3: exactly 1 movie at 8PM

# For screen 3: exactly one movie at 8PM
screen3_movies = [m for m in movies]
solver.add(Sum([If(And(screen[m] == 3, start_time[m] == 8), 1, 0) for m in movies]) == 1)

# For screens 1 and 2: exactly 2 movies each, one at 7PM and one at 9PM
for s in [1, 2]:
    # Exactly 2 movies on this screen
    solver.add(Sum([If(screen[m] == s, 1, 0) for m in movies]) == 2)
    # One at 7PM
    solver.add(Sum([If(And(screen[m] == s, start_time[m] == 7), 1, 0) for m in movies]) == 1)
    # One at 9PM
    solver.add(Sum([If(And(screen[m] == s, start_time[m] == 9), 1, 0) for m in movies]) == 1)

# Condition 1: Western begins before horror film
solver.add(start_time['W'] < start_time['H'])

# Condition 2: Sci-fi not on screen 3
solver.add(screen['S'] != 3)

# Condition 3: Romance not on screen 2
solver.add(screen['R'] != 2)

# Condition 4: Horror and mystery on different screens
solver.add(screen['H'] != screen['M'])

# Additional condition: Romance begins before western
solver.add(start_time['R'] < start_time['W'])

# Now test each answer choice
# (A) The horror film is shown on screen 1
opt_a_constr = (screen['H'] == 1)

# (B) The mystery begins at 7 P.M.
opt_b_constr = (start_time['M'] == 7)

# (C) The mystery is shown on screen 2
opt_c_constr = (screen['M'] == 2)

# (D) The sci-fi film begins at 9 P.M.
opt_d_constr = (start_time['S'] == 9)

# (E) The sci-fi film is shown on screen 2
opt_e_constr = (screen['S'] == 2)

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