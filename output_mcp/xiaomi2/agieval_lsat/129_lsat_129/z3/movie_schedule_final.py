from z3 import *

solver = Solver()

# Movies: 0=horror, 1=mystery, 2=romance, 3=sci-fi, 4=western
movies = [0, 1, 2, 3, 4]
names = {0: "horror", 1: "mystery", 2: "romance", 3: "sci-fi", 4: "western"}

screen = [Int(f'screen_{i}') for i in range(5)]
time = [Int(f'time_{i}') for i in range(5)]

for i in movies:
    solver.add(Or(screen[i] == 1, screen[i] == 2, screen[i] == 3))
    solver.add(Or(time[i] == 7, time[i] == 8, time[i] == 9))
    solver.add(Implies(screen[i] != 3, Or(time[i] == 7, time[i] == 9)))
    solver.add(Implies(screen[i] == 3, time[i] == 8))

solver.add(Sum([If(screen[i] == 1, 1, 0) for i in movies]) == 2)
solver.add(Sum([If(screen[i] == 2, 1, 0) for i in movies]) == 2)
solver.add(Sum([If(screen[i] == 3, 1, 0) for i in movies]) == 1)

solver.add(Sum([If(And(screen[i] == 1, time[i] == 7), 1, 0) for i in movies]) <= 1)
solver.add(Sum([If(And(screen[i] == 1, time[i] == 9), 1, 0) for i in movies]) <= 1)
solver.add(Sum([If(And(screen[i] == 2, time[i] == 7), 1, 0) for i in movies]) <= 1)
solver.add(Sum([If(And(screen[i] == 2, time[i] == 9), 1, 0) for i in movies]) <= 1)

# Constraints
solver.add(time[4] < time[0])  # Western before horror
solver.add(screen[3] != 3)     # Sci-fi not on screen 3
solver.add(screen[2] != 2)     # Romance not on screen 2
solver.add(screen[0] != screen[1])  # Horror and mystery different screens

# Test each option for screen 2 (7pm first, then 9pm)
options = {
    "A": And(screen[3] == 2, time[3] == 7, screen[0] == 2, time[0] == 9),
    "B": And(screen[3] == 2, time[3] == 7, screen[1] == 2, time[1] == 9),
    "C": And(screen[3] == 2, time[3] == 7, screen[4] == 2, time[4] == 9),
    "D": And(screen[4] == 2, time[4] == 7, screen[0] == 2, time[0] == 9),
    "E": And(screen[4] == 2, time[4] == 7, screen[1] == 2, time[1] == 9),
}

# The question asks which CANNOT be accurate - find the UNSAT option
impossible_options = []
possible_options = []

for letter, constr in options.items():
    solver.push()
    solver.add(constr)
    result = solver.check()
    if result == sat:
        possible_options.append(letter)
    else:
        impossible_options.append(letter)
    solver.pop()

print(f"Possible options: {possible_options}")
print(f"Impossible options: {impossible_options}")

if len(impossible_options) == 1:
    print("STATUS: sat")
    print(f"answer:{impossible_options[0]}")
elif len(impossible_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple impossible options {impossible_options}")
else:
    print("STATUS: unsat")
    print("Refine: No impossible options found")