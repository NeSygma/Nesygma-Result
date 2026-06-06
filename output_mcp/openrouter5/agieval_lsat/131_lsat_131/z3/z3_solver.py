from z3 import *

solver = Solver()

movies = ['horror', 'mystery', 'romance', 'scifi', 'western']

screen = {m: Int(f'screen_{m}') for m in movies}
time = {m: Int(f'time_{m}') for m in movies}

# Domains
for m in movies:
    solver.add(screen[m] >= 1, screen[m] <= 3)
    solver.add(time[m] >= 7, time[m] <= 9)
    solver.add(Or(time[m] == 7, time[m] == 8, time[m] == 9))

# Screen 3 only at 8pm
for m in movies:
    solver.add(Implies(screen[m] == 3, time[m] == 8))
    # If time is 8, must be on screen 3 (since only screen 3 shows at 8)
    solver.add(Implies(time[m] == 8, screen[m] == 3))

# Screens 1 and 2: exactly two movies each, one at 7 and one at 9
for scr in [1, 2]:
    solver.add(Sum([If(screen[m] == scr, 1, 0) for m in movies]) == 2)
    solver.add(Sum([If(And(screen[m] == scr, time[m] == 7), 1, 0) for m in movies]) == 1)
    solver.add(Sum([If(And(screen[m] == scr, time[m] == 9), 1, 0) for m in movies]) == 1)

# Screen 3: exactly one movie
solver.add(Sum([If(screen[m] == 3, 1, 0) for m in movies]) == 1)

# Given conditions
solver.add(time['western'] < time['horror'])
solver.add(screen['scifi'] != 3)
solver.add(screen['romance'] != 2)
solver.add(screen['horror'] != screen['mystery'])

# Additional condition: romance begins before western
solver.add(time['romance'] < time['western'])

# Let's first check if the base constraints are satisfiable
print("Checking base constraints...")
if solver.check() == sat:
    m = solver.model()
    print("SAT - here's a model:")
    for mv in movies:
        print(f"  {mv}: screen={m[screen[mv]]}, time={m[time[mv]]}")
else:
    print("UNSAT - base constraints inconsistent")
    exit()

# Now let's check each option more carefully.
# The question asks: which MUST be true? So we need to check if an option is NECESSARILY true.
# Approach: For each option, check if its negation is consistent with the constraints.
# If the negation is UNSAT, then the option MUST be true.

must_be_true = []
for letter, constr in [("A", screen['horror'] == 1), 
                        ("B", time['mystery'] == 7),
                        ("C", screen['mystery'] == 2),
                        ("D", time['scifi'] == 9),
                        ("E", screen['scifi'] == 2)]:
    solver.push()
    solver.add(Not(constr))
    res = solver.check()
    if res == unsat:
        must_be_true.append(letter)
    solver.pop()

print(f"Options that MUST be true: {must_be_true}")

if len(must_be_true) == 1:
    print("STATUS: sat")
    print(f"answer:{must_be_true[0]}")
elif len(must_be_true) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options must be true {must_be_true}")
else:
    print("STATUS: unsat")
    print("Refine: No options must be true")