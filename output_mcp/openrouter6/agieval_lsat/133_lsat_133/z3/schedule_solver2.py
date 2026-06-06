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
    solver.add(Implies(screen[m] == 3, time[m] == 8))
    solver.add(Implies(Or(screen[m] == 1, screen[m] == 2), Or(time[m] == 7, time[m] == 9)))

# Count movies per screen
count1 = Sum([If(screen[m] == 1, 1, 0) for m in movies])
count2 = Sum([If(screen[m] == 2, 1, 0) for m in movies])
count3 = Sum([If(screen[m] == 3, 1, 0) for m in movies])
solver.add(count1 == 2, count2 == 2, count3 == 1)

# For screens 1 and 2, ensure one movie at 7 and one at 9
for s in [1, 2]:
    solver.add(Sum([If(And(screen[m] == s, time[m] == 7), 1, 0) for m in movies]) >= 1)
    solver.add(Sum([If(And(screen[m] == s, time[m] == 9), 1, 0) for m in movies]) >= 1)

# Given conditions
solver.add(time['W'] < time['H'])  # Western before horror
solver.add(screen['S'] != 3)       # Sci-fi not on screen 3
solver.add(screen['R'] != 2)       # Romance not on screen 2
solver.add(screen['H'] != screen['M'])  # Horror and mystery on different screens

# Premise: Sci-fi and romance on same screen
solver.add(screen['S'] == screen['R'])

# For "must be true" questions, we check if the NEGATION of each option leads to UNSAT
# If negation is UNSAT, then the option must be true
found_options = []

# Option A: Western begins at 7 PM
solver.push()
solver.add(Not(time['W'] == 7))
if solver.check() == unsat:
    found_options.append('A')
solver.pop()

# Option B: Sci-fi begins at 9 PM
solver.push()
solver.add(Not(time['S'] == 9))
if solver.check() == unsat:
    found_options.append('B')
solver.pop()

# Option C: Mystery begins at 8 PM
solver.push()
solver.add(Not(time['M'] == 8))
if solver.check() == unsat:
    found_options.append('C')
solver.pop()

# Option D: Romance begins at 9 PM
solver.push()
solver.add(Not(time['R'] == 9))
if solver.check() == unsat:
    found_options.append('D')
solver.pop()

# Option E: Horror begins at 8 PM
solver.push()
solver.add(Not(time['H'] == 8))
if solver.check() == unsat:
    found_options.append('E')
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