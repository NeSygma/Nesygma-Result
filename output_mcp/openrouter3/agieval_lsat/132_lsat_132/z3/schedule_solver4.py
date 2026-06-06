from z3 import *

# Movies
movies = ["horror", "mystery", "romance", "sci_fi", "western"]
movie_to_idx = {m: i for i, m in enumerate(movies)}

# We'll model each movie's screen and time
# For each movie, we need to know which screen it's on and what time
# But since screens determine times, we can just assign screens and derive times

# Variables: screen assignment for each movie
# Screen values: 1, 2, or 3
screen = [Int(f'screen_{m}') for m in movies]

solver = Solver()

# Each movie gets a screen 1, 2, or 3
for s in screen:
    solver.add(Or(s == 1, s == 2, s == 3))

# Map movie indices
horror = 0
mystery = 1
romance = 2
sci_fi = 3
western = 4

# Constraint: Screen 1 and 2 have exactly 2 movies each, screen 3 has exactly 1
# Count movies on each screen
screen1_count = Sum([If(screen[i] == 1, 1, 0) for i in range(5)])
screen2_count = Sum([If(screen[i] == 2, 1, 0) for i in range(5)])
screen3_count = Sum([If(screen[i] == 3, 1, 0) for i in range(5)])

solver.add(screen1_count == 2)
solver.add(screen2_count == 2)
solver.add(screen3_count == 1)

# Constraint: Western begins before horror film
# Time depends on screen and slot (7 PM, 9 PM for screens 1,2; 8 PM for screen 3)
# For screens 1 and 2, we need to know which slot (7 or 9 PM) each movie is in
# Let's add variables for the slot assignment for movies on screens 1 and 2
# slot = 0 for 7 PM, slot = 1 for 9 PM
slot = [Int(f'slot_{m}') for m in movies]

# Only movies on screens 1 or 2 have slot assignments (0 or 1)
# Movies on screen 3 have slot = 2 (meaning 8 PM)
for i in range(5):
    solver.add(If(screen[i] == 3, slot[i] == 2, Or(slot[i] == 0, slot[i] == 1)))

# For each screen, the two movies must have different slots
# Screen 1: movies with screen[i] == 1 must have different slots
screen1_movies = [i for i in range(5)]
screen2_movies = [i for i in range(5)]
screen3_movies = [i for i in range(5)]

# Actually, let's use a different approach: for each screen, the two movies must have different slots
# We can enforce this by saying: for any two movies on the same screen, their slots must be different
for i in range(5):
    for j in range(i+1, 5):
        solver.add(Implies(And(screen[i] == screen[j], screen[i] != 3), slot[i] != slot[j]))

# Now, time for each movie: 7 PM = 7, 9 PM = 9, 8 PM = 8
time = [Int(f'time_{m}') for m in movies]
for i in range(5):
    solver.add(If(screen[i] == 1, 
                  If(slot[i] == 0, time[i] == 7, time[i] == 9),
                  If(screen[i] == 2,
                    If(slot[i] == 0, time[i] == 7, time[i] == 9),
                    time[i] == 8)))

# Constraint: Western begins before horror film
solver.add(time[western] < time[horror])

# Constraint: Sci-fi not on screen 3
solver.add(screen[sci_fi] != 3)

# Constraint: Romance not on screen 2
solver.add(screen[romance] != 2)

# Constraint: Horror and mystery on different screens
solver.add(screen[horror] != screen[mystery])

# Now test each option for screen 1
# Option A: sci-fi, horror (7 PM first, then 9 PM)
# This means: sci-fi is on screen 1 at 7 PM, horror is on screen 1 at 9 PM
opt_a = And(screen[sci_fi] == 1, slot[sci_fi] == 0,
            screen[horror] == 1, slot[horror] == 1)

# Option B: sci-fi, mystery
opt_b = And(screen[sci_fi] == 1, slot[sci_fi] == 0,
            screen[mystery] == 1, slot[mystery] == 1)

# Option C: western, horror
opt_c = And(screen[western] == 1, slot[western] == 0,
            screen[horror] == 1, slot[horror] == 1)

# Option D: western, mystery
opt_d = And(screen[western] == 1, slot[western] == 0,
            screen[mystery] == 1, slot[mystery] == 1)

# Option E: western, sci-fi
opt_e = And(screen[western] == 1, slot[western] == 0,
            screen[sci_fi] == 1, slot[sci_fi] == 1)

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