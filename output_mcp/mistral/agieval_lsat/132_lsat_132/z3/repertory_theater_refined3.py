from z3 import *

# Movie types
movies = ["horror", "mystery", "romance", "sci-fi", "western"]

# Screens and times
# Screen 1: 7pm and 9pm
# Screen 2: 7pm and 9pm
# Screen 3: 8pm only

solver = Solver()

# Decision variables
screen = {m: Int(f"screen_{m}") for m in movies}
time = {m: Int(f"time_{m}") for m in movies}

# Each movie is on exactly one screen (1, 2, or 3)
for m in movies:
    solver.add(Or(screen[m] == 1, screen[m] == 2, screen[m] == 3))

# Each movie is at exactly one time (7, 8, or 9)
for m in movies:
    solver.add(Or(time[m] == 7, time[m] == 8, time[m] == 9))

# Screen 3 only shows at 8pm
for m in movies:
    solver.add(Implies(screen[m] == 3, time[m] == 8))

# Screens 1 and 2 each have exactly one movie at 7pm and one at 9pm
# Screen 3 has exactly one movie at 8pm
solver.add(Sum([If(And(screen[m] == 1, time[m] == 7), 1, 0) for m in movies]) == 1)
solver.add(Sum([If(And(screen[m] == 1, time[m] == 9), 1, 0) for m in movies]) == 1)
solver.add(Sum([If(And(screen[m] == 2, time[m] == 7), 1, 0) for m in movies]) == 1)
solver.add(Sum([If(And(screen[m] == 2, time[m] == 9), 1, 0) for m in movies]) == 1)
solver.add(Sum([If(And(screen[m] == 3, time[m] == 8), 1, 0) for m in movies]) == 1)

# Constraint 1: Western begins before horror
# Time slots: 7 < 8 < 9
solver.add(time["western"] < time["horror"])

# Constraint 2: Sci-fi is not on screen 3
solver.add(screen["sci-fi"] != 3)

# Constraint 3: Romance is not on screen 2
solver.add(screen["romance"] != 2)

# Constraint 4: Horror and mystery are on different screens
solver.add(screen["horror"] != screen["mystery"])

# Now, let's evaluate each multiple choice option
# Each option specifies what movies are on screen 1 at 7pm and 9pm

impossible_options = []

# Option A: screen 1 has sci-fi at 7pm, horror at 9pm
solver.push()
solver.add(And(
    screen["sci-fi"] == 1, time["sci-fi"] == 7,
    screen["horror"] == 1, time["horror"] == 9
))
if solver.check() == unsat:
    impossible_options.append("A")
    print("Option A is impossible")
else:
    print("Option A is possible")
solver.pop()

# Option B: screen 1 has sci-fi at 7pm, mystery at 9pm
solver.push()
solver.add(And(
    screen["sci-fi"] == 1, time["sci-fi"] == 7,
    screen["mystery"] == 1, time["mystery"] == 9
))
if solver.check() == unsat:
    impossible_options.append("B")
    print("Option B is impossible")
else:
    print("Option B is possible")
solver.pop()

# Option C: screen 1 has western at 7pm, horror at 9pm
solver.push()
solver.add(And(
    screen["western"] == 1, time["western"] == 7,
    screen["horror"] == 1, time["horror"] == 9
))
if solver.check() == unsat:
    impossible_options.append("C")
    print("Option C is impossible")
else:
    print("Option C is possible")
solver.pop()

# Option D: screen 1 has western at 7pm, mystery at 9pm
solver.push()
solver.add(And(
    screen["western"] == 1, time["western"] == 7,
    screen["mystery"] == 1, time["mystery"] == 9
))
if solver.check() == unsat:
    impossible_options.append("D")
    print("Option D is impossible")
else:
    print("Option D is possible")
solver.pop()

# Option E: screen 1 has western at 7pm, sci-fi at 9pm
solver.push()
solver.add(And(
    screen["western"] == 1, time["western"] == 7,
    screen["sci-fi"] == 1, time["sci-fi"] == 9
))
if solver.check() == unsat:
    impossible_options.append("E")
    print("Option E is impossible")
else:
    print("Option E is possible")
solver.pop()

if len(impossible_options) == 1:
    print("STATUS: sat")
    print(f"answer:{impossible_options[0]}")
elif len(impossible_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple impossible options found {impossible_options}")
else:
    print("STATUS: unsat")
    print("Refine: No impossible options found")