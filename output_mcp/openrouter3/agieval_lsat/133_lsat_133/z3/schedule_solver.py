from z3 import *

# Define movies and screens
movies = ["horror", "mystery", "romance", "sci_fi", "western"]
screens = [1, 2, 3]
times = [7, 8, 9]  # PM

# Create variables: screen assignment and time for each movie
screen = {m: Int(f"screen_{m}") for m in movies}
time = {m: Int(f"time_{m}") for m in movies}

solver = Solver()

# Base constraints
# 1. Each movie on exactly one screen (1, 2, or 3)
for m in movies:
    solver.add(Or([screen[m] == s for s in screens]))

# 2. Each movie has exactly one time slot
for m in movies:
    solver.add(Or([time[m] == t for t in times]))

# 3. Screen 3 shows exactly one movie at 8 PM
# Count movies on screen 3
screen3_movies = [If(screen[m] == 3, 1, 0) for m in movies]
solver.add(Sum(screen3_movies) == 1)
# The movie on screen 3 must be at 8 PM
for m in movies:
    solver.add(Implies(screen[m] == 3, time[m] == 8))

# 4. Screens 1 and 2 show two movies each
screen1_movies = [If(screen[m] == 1, 1, 0) for m in movies]
screen2_movies = [If(screen[m] == 2, 1, 0) for m in movies]
solver.add(Sum(screen1_movies) == 2)
solver.add(Sum(screen2_movies) == 2)

# 5. On screens 1 and 2: one movie at 7 PM, one at 9 PM
# For screen 1
screen1_7 = [If(And(screen[m] == 1, time[m] == 7), 1, 0) for m in movies]
screen1_9 = [If(And(screen[m] == 1, time[m] == 9), 1, 0) for m in movies]
solver.add(Sum(screen1_7) == 1)
solver.add(Sum(screen1_9) == 1)

# For screen 2
screen2_7 = [If(And(screen[m] == 2, time[m] == 7), 1, 0) for m in movies]
screen2_9 = [If(And(screen[m] == 2, time[m] == 9), 1, 0) for m in movies]
solver.add(Sum(screen2_7) == 1)
solver.add(Sum(screen2_9) == 1)

# 6. Western begins before horror film
solver.add(time["western"] < time["horror"])

# 7. Sci-fi not on screen 3
solver.add(screen["sci_fi"] != 3)

# 8. Romance not on screen 2
solver.add(screen["romance"] != 2)

# 9. Horror and mystery on different screens
solver.add(screen["horror"] != screen["mystery"])

# Additional condition: sci-fi and romance on same screen
solver.add(screen["sci_fi"] == screen["romance"])

# Now test each answer choice
# Answer choices are about what MUST be true
# We need to check: if the base constraints + sci-fi/romance same screen are satisfied,
# which of these statements is ALWAYS true?

# Let's define the answer choices as constraints that would be true if the statement holds
# We need to check: for each choice, is it necessarily true in ALL models satisfying constraints?

# Approach: For each choice, check if its negation is compatible with constraints
# If negation leads to UNSAT, then the choice MUST be true

# Define the statements:
# (A) The western begins at 7 P.M. -> time["western"] == 7
# (B) The sci-fi film begins at 9 P.M. -> time["sci_fi"] == 9
# (C) The mystery begins at 8 P.M. -> time["mystery"] == 8
# (D) The romance begins at 9 P.M. -> time["romance"] == 9
# (E) The horror film begins at 8 P.M. -> time["horror"] == 8

# We'll test each choice by checking if its negation is satisfiable
# If negation is UNSAT, then the choice MUST be true

found_options = []

# Test (A): western at 7 PM
solver.push()
solver.add(Not(time["western"] == 7))
if solver.check() == unsat:
    found_options.append("A")
solver.pop()

# Test (B): sci-fi at 9 PM
solver.push()
solver.add(Not(time["sci_fi"] == 9))
if solver.check() == unsat:
    found_options.append("B")
solver.pop()

# Test (C): mystery at 8 PM
solver.push()
solver.add(Not(time["mystery"] == 8))
if solver.check() == unsat:
    found_options.append("C")
solver.pop()

# Test (D): romance at 9 PM
solver.push()
solver.add(Not(time["romance"] == 9))
if solver.check() == unsat:
    found_options.append("D")
solver.pop()

# Test (E): horror at 8 PM
solver.push()
solver.add(Not(time["horror"] == 8))
if solver.check() == unsat:
    found_options.append("E")
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