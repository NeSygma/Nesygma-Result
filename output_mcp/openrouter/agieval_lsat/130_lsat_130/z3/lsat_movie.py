from z3 import *

# Define movies
movies = ['H','M','R','S','W']
screen = {m: Int(f'screen_{m}') for m in movies}
time = {m: Int(f'time_{m}') for m in movies}

solver = Solver()

# Domain constraints
for m in movies:
    solver.add(Or(screen[m] == 1, screen[m] == 2, screen[m] == 3))
    solver.add(Or(time[m] == 7, time[m] == 8, time[m] == 9))

# Slot restrictions: screen 3 only at time 8
for m in movies:
    solver.add(Implies(screen[m] == 3, time[m] == 8))
    # If not screen 3, cannot be time 8
    solver.add(Implies(screen[m] != 3, time[m] != 8))

# Ensure each slot (1,7),(1,9),(2,7),(2,9),(3,8) is used exactly once
# Count each slot = 1
solver.add(Sum([If(And(screen[m]==1, time[m]==7), 1, 0) for m in movies]) == 1)
solver.add(Sum([If(And(screen[m]==1, time[m]==9), 1, 0) for m in movies]) == 1)
solver.add(Sum([If(And(screen[m]==2, time[m]==7), 1, 0) for m in movies]) == 1)
solver.add(Sum([If(And(screen[m]==2, time[m]==9), 1, 0) for m in movies]) == 1)
solver.add(Sum([If(And(screen[m]==3, time[m]==8), 1, 0) for m in movies]) == 1)

# Additional problem constraints
solver.add(time['W'] < time['H'])  # western before horror
solver.add(screen['S'] != 3)       # sci-fi not on screen 3
solver.add(screen['R'] != 2)       # romance not on screen 2
solver.add(screen['H'] != screen['M'])  # horror and mystery different screens

# Condition: western and sci-fi on same screen
solver.add(screen['W'] == screen['S'])

# Define option constraints
opt_a = (screen['H'] == 2)          # A
opt_b = (time['M'] == 9)            # B
opt_c = (screen['R'] == 3)          # C
opt_d = (time['S'] == 7)            # D
opt_e = (time['W'] == 8)            # E

found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
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