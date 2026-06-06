from z3 import *

# Define movie variables
movies = ['H', 'M', 'R', 'S', 'W']  # Horror, Mystery, Romance, Sci-fi, Western
screen = {m: Int(f'screen_{m}') for m in movies}
time = {m: Int(f'time_{m}') for m in movies}

solver = Solver()

# Base constraints: screen and time domains
for m in movies:
    solver.add(screen[m] >= 1, screen[m] <= 3)
    solver.add(Or(time[m] == 7, time[m] == 8, time[m] == 9))

# Time must be consistent with screen
for m in movies:
    # If screen is 3, time must be 8; if screen is 1 or 2, time must be 7 or 9
    solver.add(Implies(screen[m] == 3, time[m] == 8))
    solver.add(Implies(Or(screen[m] == 1, screen[m] == 2), Or(time[m] == 7, time[m] == 9)))

# Count movies per screen
count1 = Sum([If(screen[m] == 1, 1, 0) for m in movies])
count2 = Sum([If(screen[m] == 2, 1, 0) for m in movies])
count3 = Sum([If(screen[m] == 3, 1, 0) for m in movies])
solver.add(count1 == 2, count2 == 2, count3 == 1)

# For screens 1 and 2, ensure one movie at 7 and one at 9
for s in [1, 2]:
    # At least one movie on screen s with time 7
    solver.add(Sum([If(And(screen[m] == s, time[m] == 7), 1, 0) for m in movies]) >= 1)
    # At least one movie on screen s with time 9
    solver.add(Sum([If(And(screen[m] == s, time[m] == 9), 1, 0) for m in movies]) >= 1)

# Given conditions
# 1. Western begins before horror
solver.add(time['W'] < time['H'])
# 2. Sci-fi not on screen 3
solver.add(screen['S'] != 3)
# 3. Romance not on screen 2
solver.add(screen['R'] != 2)
# 4. Horror and mystery on different screens
solver.add(screen['H'] != screen['M'])

# Premise: Sci-fi and romance on same screen
solver.add(screen['S'] == screen['R'])

# Define options as constraints
opt_a_constr = (time['W'] == 7)
opt_b_constr = (time['S'] == 9)
opt_c_constr = (time['M'] == 8)
opt_d_constr = (time['R'] == 9)
opt_e_constr = (time['H'] == 8)

# Evaluate each option using the exact skeleton
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