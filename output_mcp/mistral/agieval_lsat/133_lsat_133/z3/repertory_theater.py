from z3 import *

# Declare movies and times
movies = ["horror", "mystery", "romance", "sci-fi", "western"]
times = [7, 8, 9]  # 7 PM, 8 PM, 9 PM
screens = [1, 2, 3]

# Create symbolic variables
screen = {m: Int(f"screen_{m}") for m in movies}
time = {m: Int(f"time_{m}") for m in movies}

# Create solver
solver = Solver()

# Helper: All movies have distinct screens (each movie shown exactly once)
solver.add(Distinct(list(screen.values())))

# Helper: All movies have distinct times (each movie shown at one time)
solver.add(Distinct(list(time.values())))

# Screen 3 only shows the 8 PM movie
for m in movies:
    solver.add(Implies(screen[m] == 3, time[m] == 8))

# Screens 1 and 2 show movies at 7 PM and 9 PM only
for m in movies:
    solver.add(Implies(Or(screen[m] == 1, screen[m] == 2), Or(time[m] == 7, time[m] == 9)))

# The western begins at some time before the horror film
solver.add(time["western"] < time["horror"])

# The sci-fi film is not shown on screen 3
solver.add(screen["sci-fi"] != 3)

# The romance is not shown on screen 2
solver.add(screen["romance"] != 2)

# The horror film and the mystery are shown on different screens
solver.add(screen["horror"] != screen["mystery"])

# Additional constraint for the question: sci-fi and romance are shown on the same screen
solver.add(screen["sci-fi"] == screen["romance"])

# Base constraints are set; now evaluate answer choices

# Define answer choice constraints
answer_choices = {
    "A": time["western"] == 7,
    "B": time["sci-fi"] == 9,
    "C": time["mystery"] == 8,
    "D": time["romance"] == 9,
    "E": time["horror"] == 8,
}

found_options = []
for letter, constr in answer_choices.items():
    solver.push()
    solver.add(Not(constr))  # Check if the negation is unsat (i.e., the choice must be true)
    if solver.check() == unsat:
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