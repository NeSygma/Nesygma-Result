from z3 import *

# Movies
movies = ["horror", "mystery", "romance", "sci_fi", "western"]
movie_to_idx = {m: i for i, m in enumerate(movies)}

# We'll model the schedule as a mapping from (screen, time) to movie
# But since we have discrete screens and times, we can use arrays
# Let's create variables for each screen and time slot
# Screen 1: time 7 and 9
# Screen 2: time 7 and 9  
# Screen 3: time 8

# We'll use a list of variables for each slot
# Each slot can have at most one movie
screen1_7 = Int('screen1_7')  # movie index at screen 1, 7 PM
screen1_9 = Int('screen1_9')  # movie index at screen 1, 9 PM
screen2_7 = Int('screen2_7')  # movie index at screen 2, 7 PM
screen2_9 = Int('screen2_9')  # movie index at screen 2, 9 PM
screen3_8 = Int('screen3_8')  # movie index at screen 3, 8 PM

solver = Solver()

# Each slot must have a valid movie index (0-4)
for var in [screen1_7, screen1_9, screen2_7, screen2_9, screen3_8]:
    solver.add(var >= 0, var <= 4)

# All movies must be assigned exactly once
all_slots = [screen1_7, screen1_9, screen2_7, screen2_9, screen3_8]
solver.add(Distinct(all_slots))

# Map movie names to indices
horror = 0
mystery = 1
romance = 2
sci_fi = 3
western = 4

# Constraint 1: Western begins before horror film
# We need to find the times of western and horror
# Western time: if western is in screen1_7, time=7; screen1_9, time=9; etc.
western_time = If(western == screen1_7, 7,
           If(western == screen1_9, 9,
           If(western == screen2_7, 7,
           If(western == screen2_9, 9,
           If(western == screen3_8, 8, 0)))))

horror_time = If(horror == screen1_7, 7,
         If(horror == screen1_9, 9,
         If(horror == screen2_7, 7,
         If(horror == screen2_9, 9,
         If(horror == screen3_8, 8, 0)))))

solver.add(western_time < horror_time)

# Constraint 2: Sci-fi not on screen 3
solver.add(sci_fi != screen3_8)

# Constraint 3: Romance not on screen 2
solver.add(romance != screen2_7)
solver.add(romance != screen2_9)

# Constraint 4: Horror and mystery on different screens
# Check if they are on the same screen
horror_screen = If(horror == screen1_7, 1,
           If(horror == screen1_9, 1,
           If(horror == screen2_7, 2,
           If(horror == screen2_9, 2,
           If(horror == screen3_8, 3, 0)))))

mystery_screen = If(mystery == screen1_7, 1,
           If(mystery == screen1_9, 1,
           If(mystery == screen2_7, 2,
           If(mystery == screen2_9, 2,
           If(mystery == screen3_8, 3, 0)))))

solver.add(horror_screen != mystery_screen)

# Now test each option for screen 1
# Option A: sci-fi, horror (7 PM first, then 9 PM)
opt_a = And(screen1_7 == sci_fi, screen1_9 == horror)

# Option B: sci-fi, mystery
opt_b = And(screen1_7 == sci_fi, screen1_9 == mystery)

# Option C: western, horror
opt_c = And(screen1_7 == western, screen1_9 == horror)

# Option D: western, mystery
opt_d = And(screen1_7 == western, screen1_9 == mystery)

# Option E: western, sci-fi
opt_e = And(screen1_7 == western, screen1_9 == sci_fi)

# Test each option
found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
    solver.pop()

# Print results
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")