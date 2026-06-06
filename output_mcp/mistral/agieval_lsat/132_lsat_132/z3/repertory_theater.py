from z3 import *

# Movie types
movies = ["horror", "mystery", "romance", "sci-fi", "western"]

# Screens and times
# Screen 1: 7pm and 9pm
# Screen 2: 7pm and 9pm  
# Screen 3: 8pm only

# We'll model:
# - screen[m] = screen number for movie m
# - time[m] = time slot for movie m (7, 8, or 9)

solver = Solver()

# Decision variables
screen = {m: Int(f"screen_{m}") for m in movies}
time = {m: Int(f"time_{m}") for m in movies}

# Each movie is on exactly one screen
for m in movies:
    solver.add(Or(screen[m] == 1, screen[m] == 2, screen[m] == 3))

# Each movie is at exactly one time
for m in movies:
    solver.add(Or(time[m] == 7, time[m] == 8, time[m] == 9))

# Screen 3 only shows at 8pm
for m in movies:
    solver.add(Implies(screen[m] == 3, time[m] == 8))

# Screens 1 and 2 show one movie at 7pm and one at 9pm
# So across all movies, there must be exactly one 7pm and one 9pm on screen 1,
# and exactly one 7pm and one 9pm on screen 2
# Screen 3 has exactly one 8pm

# Count movies per screen per time
screen1_7pm = Bool("screen1_7pm")
screen1_9pm = Bool("screen1_9pm")
screen2_7pm = Bool("screen2_7pm")
screen2_9pm = Bool("screen2_9pm")
screen3_8pm = Bool("screen3_8pm")

# Helper: movie m is on screen s at time t
solver.add(screen1_7pm == And(screen["horror"] == 1, time["horror"] == 7, 
                              Or(screen["mystery"] == 1, screen["romance"] == 1, screen["sci-fi"] == 1, screen["western"] == 1) == False))
# This approach is getting messy. Let me use a cleaner method.

# Better approach: Use sums to count movies per screen per time
solver.add(Sum([If(And(screen[m] == 1, time[m] == 7), 1, 0) for m in movies]) == 1)
solver.add(Sum([If(And(screen[m] == 1, time[m] == 9), 1, 0) for m in movies]) == 1)
solver.add(Sum([If(And(screen[m] == 2, time[m] == 7), 1, 0) for m in movies]) == 1)
solver.add(Sum([If(And(screen[m] == 2, time[m] == 9), 1, 0) for m in movies]) == 1)
solver.add(Sum([If(And(screen[m] == 3, time[m] == 8), 1, 0) for m in movies]) == 1)

# Constraint 1: Western begins before horror
# This means time[western] < time[horror]
# Time slots: 7 < 8 < 9
solver.add(Or(
    And(time["western"] == 7, time["horror"] == 8),
    And(time["western"] == 7, time["horror"] == 9),
    And(time["western"] == 8, time["horror"] == 9)
))

# Constraint 2: Sci-fi is not on screen 3
solver.add(screen["sci-fi"] != 3)

# Constraint 3: Romance is not on screen 2
solver.add(screen["romance"] != 2)

# Constraint 4: Horror and mystery are on different screens
solver.add(screen["horror"] != screen["mystery"])

# Additional constraint: All movies must be assigned to different screens?
# No, multiple movies can be on the same screen (screens 1 and 2 have 2 movies each)
# But each movie is on exactly one screen, which we already encoded

# Now, let's evaluate each multiple choice option
# Each option specifies what movies are on screen 1 at 7pm and 9pm

# For each option, we need to check if it's possible

found_options = []

# Option A: screen 1 has sci-fi at 7pm, horror at 9pm
solver.push()
solver.add(And(
    screen["sci-fi"] == 1, time["sci-fi"] == 7,
    screen["horror"] == 1, time["horror"] == 9
))
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: screen 1 has sci-fi at 7pm, mystery at 9pm
solver.push()
solver.add(And(
    screen["sci-fi"] == 1, time["sci-fi"] == 7,
    screen["mystery"] == 1, time["mystery"] == 9
))
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: screen 1 has western at 7pm, horror at 9pm
solver.push()
solver.add(And(
    screen["western"] == 1, time["western"] == 7,
    screen["horror"] == 1, time["horror"] == 9
))
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: screen 1 has western at 7pm, mystery at 9pm
solver.push()
solver.add(And(
    screen["western"] == 1, time["western"] == 7,
    screen["mystery"] == 1, time["mystery"] == 9
))
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: screen 1 has western at 7pm, sci-fi at 9pm
solver.push()
solver.add(And(
    screen["western"] == 1, time["western"] == 7,
    screen["sci-fi"] == 1, time["sci-fi"] == 9
))
if solver.check() == sat:
    found_options.append("E")
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