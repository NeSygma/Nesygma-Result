from z3 import *

solver = Solver()
# Define movie variables
movies = ['horror', 'mystery', 'romance', 'scifi', 'western']
# Create screen and time variables for each movie
screen = {m: Int(f'screen_{m}') for m in movies}
time = {m: Int(f'time_{m}') for m in movies}

# Domain constraints
for m in movies:
    solver.add(screen[m] >= 1, screen[m] <= 3)
    solver.add(time[m] >= 7, time[m] <= 9)

# Time 8 implies screen 3, and screen 3 implies time 8
for m in movies:
    solver.add(Implies(time[m] == 8, screen[m] == 3))
    solver.add(Implies(screen[m] == 3, time[m] == 8))

# Screen capacity constraints
solver.add(Sum([If(screen[m] == 1, 1, 0) for m in movies]) == 2)
solver.add(Sum([If(screen[m] == 2, 1, 0) for m in movies]) == 2)
solver.add(Sum([If(screen[m] == 3, 1, 0) for m in movies]) == 1)

# Time slot usage constraints
solver.add(Sum([If(time[m] == 7, 1, 0) for m in movies]) == 2)
solver.add(Sum([If(time[m] == 8, 1, 0) for m in movies]) == 1)
solver.add(Sum([If(time[m] == 9, 1, 0) for m in movies]) == 2)

# Additional constraints
solver.add(time['western'] < time['horror'])
solver.add(screen['scifi'] != 3)
solver.add(screen['romance'] != 2)
solver.add(screen['horror'] != screen['mystery'])

# Option constraints
opt_a_constr = And(screen['scifi'] == 1, time['scifi'] == 7,
                    screen['horror'] == 1, time['horror'] == 9)
opt_b_constr = And(screen['scifi'] == 1, time['scifi'] == 7,
                    screen['mystery'] == 1, time['mystery'] == 9)
opt_c_constr = And(screen['western'] == 1, time['western'] == 7,
                    screen['horror'] == 1, time['horror'] == 9)
opt_d_constr = And(screen['western'] == 1, time['western'] == 7,
                    screen['mystery'] == 1, time['mystery'] == 9)
opt_e_constr = And(screen['western'] == 1, time['western'] == 7,
                    screen['scifi'] == 1, time['scifi'] == 9)

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