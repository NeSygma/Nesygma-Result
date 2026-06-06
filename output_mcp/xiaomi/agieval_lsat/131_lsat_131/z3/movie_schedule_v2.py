from z3 import *

solver = Solver()

# Movies: horror, mystery, romance, sci-fi, western
movies = ['horror', 'mystery', 'romance', 'sci-fi', 'western']

# Screen assignment: 1, 2, or 3
screen = {m: Int(f'screen_{m}') for m in movies}

# Time assignment: 7, 8, or 9
time = {m: Int(f'time_{m}') for m in movies}

# Screen domains
for m in movies:
    solver.add(Or(screen[m] == 1, screen[m] == 2, screen[m] == 3))

# Time domains
for m in movies:
    solver.add(Or(time[m] == 7, time[m] == 8, time[m] == 9))

# Exactly 2 movies on screen 1
solver.add(Sum([If(screen[m] == 1, 1, 0) for m in movies]) == 2)
# Exactly 2 movies on screen 2
solver.add(Sum([If(screen[m] == 2, 1, 0) for m in movies]) == 2)
# Exactly 1 movie on screen 3
solver.add(Sum([If(screen[m] == 3, 1, 0) for m in movies]) == 1)

# Screen 1 movies: one at 7, one at 9
solver.add(Sum([If(And(screen[m] == 1, time[m] == 7), 1, 0) for m in movies]) == 1)
solver.add(Sum([If(And(screen[m] == 1, time[m] == 9), 1, 0) for m in movies]) == 1)

# Screen 2 movies: one at 7, one at 9
solver.add(Sum([If(And(screen[m] == 2, time[m] == 7), 1, 0) for m in movies]) == 1)
solver.add(Sum([If(And(screen[m] == 2, time[m] == 9), 1, 0) for m in movies]) == 1)

# Screen 3 movie: at 8
for m in movies:
    solver.add(Implies(screen[m] == 3, time[m] == 8))

# All movies have distinct (screen, time) pairs
for i in range(len(movies)):
    for j in range(i+1, len(movies)):
        mi, mj = movies[i], movies[j]
        solver.add(Not(And(screen[mi] == screen[mj], time[mi] == time[mj])))

# Condition 1: Western begins before horror
solver.add(time['western'] < time['horror'])

# Condition 2: Sci-fi not on screen 3
solver.add(screen['sci-fi'] != 3)

# Condition 3: Romance not on screen 2
solver.add(screen['romance'] != 2)

# Condition 4: Horror and mystery on different screens
solver.add(screen['horror'] != screen['mystery'])

# Additional condition: Romance begins before western
solver.add(time['romance'] < time['western'])

# Check which options MUST be true
# For each option, check if its negation is unsatisfiable (i.e., it must be true)
must_be_true = []
for letter, constr in [("A", screen['horror'] == 1), 
                        ("B", time['mystery'] == 7), 
                        ("C", screen['mystery'] == 2), 
                        ("D", time['sci-fi'] == 9), 
                        ("E", screen['sci-fi'] == 2)]:
    solver.push()
    solver.add(Not(constr))
    if solver.check() == unsat:
        must_be_true.append(letter)
    solver.pop()

print(f"Must be true options: {must_be_true}")

if len(must_be_true) == 1:
    print("STATUS: sat")
    print(f"answer:{must_be_true[0]}")
elif len(must_be_true) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple must-be-true options found {must_be_true}")
else:
    print("STATUS: unsat")
    print("Refine: No must-be-true options found")