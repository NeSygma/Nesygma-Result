from z3 import *

solver = Solver()

# Movies: horror, mystery, romance, scifi, western
movies = ['horror', 'mystery', 'romance', 'scifi', 'western']
screen = {m: Int(f'screen_{m}') for m in movies}
time = {m: Int(f'time_{m}') for m in movies}

# Domains
for m in movies:
    solver.add(screen[m] >= 1, screen[m] <= 3)
    solver.add(time[m] >= 7, time[m] <= 9)
    solver.add(Or(time[m] == 7, time[m] == 8, time[m] == 9))

# Screens 1 and 2 show two movies each, one at 7 and one at 9.
# Screen 3 shows exactly one movie at 8.
for scr in [1, 2, 3]:
    count_on_screen = Sum([If(screen[m] == scr, 1, 0) for m in movies])
    if scr == 3:
        solver.add(count_on_screen == 1)
    else:
        solver.add(count_on_screen == 2)

for scr in [1, 2]:
    count_at_7 = Sum([If(And(screen[m] == scr, time[m] == 7), 1, 0) for m in movies])
    count_at_9 = Sum([If(And(screen[m] == scr, time[m] == 9), 1, 0) for m in movies])
    solver.add(count_at_7 == 1)
    solver.add(count_at_9 == 1)

# Screen 3: exactly one movie at 8
count_at_8_on_3 = Sum([If(And(screen[m] == 3, time[m] == 8), 1, 0) for m in movies])
solver.add(count_at_8_on_3 == 1)

# Consistency: screen 3 => time 8; screens 1,2 => time != 8
for m in movies:
    solver.add(Implies(screen[m] == 3, time[m] == 8))
    solver.add(Implies(Or(screen[m] == 1, screen[m] == 2), time[m] != 8))

# Conditions:
solver.add(time['western'] < time['horror'])
solver.add(screen['scifi'] != 3)
solver.add(screen['romance'] != 2)
solver.add(screen['horror'] != screen['mystery'])

# Additional condition: sci-fi and romance on same screen
solver.add(screen['scifi'] == screen['romance'])

# Let's first check if the base constraints are satisfiable
print("Checking base constraints...")
if solver.check() == sat:
    m = solver.model()
    print("SAT - here's a model:")
    for mv in movies:
        print(f"  {mv}: screen={m[screen[mv]]}, time={m[time[mv]]}")
else:
    print("UNSAT - base constraints unsatisfiable")
    exit()

# Now let's check each option more carefully.
# The problem asks: which MUST be true? So we need to check if an option is NECESSARILY true
# under the given conditions. That means: if we add the NEGATION of the option, the system
# should become UNSAT (i.e., the option is forced).

# Let's check each option by testing if its negation is consistent.
# If negating an option leads to UNSAT, then that option MUST be true.

must_be_true = []
for letter, constr in [("A", time['western'] == 7), 
                        ("B", time['scifi'] == 9),
                        ("C", time['mystery'] == 8),
                        ("D", time['romance'] == 9),
                        ("E", time['horror'] == 8)]:
    solver.push()
    solver.add(Not(constr))  # negate the option
    if solver.check() == unsat:
        must_be_true.append(letter)
    solver.pop()

print(f"\nOptions that MUST be true: {must_be_true}")

if len(must_be_true) == 1:
    print("STATUS: sat")
    print(f"answer:{must_be_true[0]}")
elif len(must_be_true) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {must_be_true}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")