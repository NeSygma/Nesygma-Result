from z3 import *

solver = Solver()

# Movies: horror(0), mystery(1), romance(2), sci-fi(3), western(4)
# Screens: 1, 2, 3
# Times: 7pm=7, 8pm=8, 9pm=9

# Each movie gets a screen and a time
screen = [Int(f'screen_{i}') for i in range(5)]
time = [Int(f'time_{i}') for i in range(5)]

# Screen assignments: 1, 2, or 3
for i in range(5):
    solver.add(Or(screen[i] == 1, screen[i] == 2, screen[i] == 3))

# Time assignments based on screen
for i in range(5):
    solver.add(Implies(screen[i] == 1, Or(time[i] == 7, time[i] == 9)))
    solver.add(Implies(screen[i] == 2, Or(time[i] == 7, time[i] == 9)))
    solver.add(Implies(screen[i] == 3, time[i] == 8))

# Screen 1 shows exactly 2 movies (one at 7pm, one at 9pm)
solver.add(Sum([If(screen[i] == 1, 1, 0) for i in range(5)]) == 2)
solver.add(Sum([If(And(screen[i] == 1, time[i] == 7), 1, 0) for i in range(5)]) == 1)
solver.add(Sum([If(And(screen[i] == 1, time[i] == 9), 1, 0) for i in range(5)]) == 1)

# Screen 2 shows exactly 2 movies (one at 7pm, one at 9pm)
solver.add(Sum([If(screen[i] == 2, 1, 0) for i in range(5)]) == 2)
solver.add(Sum([If(And(screen[i] == 2, time[i] == 7), 1, 0) for i in range(5)]) == 1)
solver.add(Sum([If(And(screen[i] == 2, time[i] == 9), 1, 0) for i in range(5)]) == 1)

# Screen 3 shows exactly 1 movie at 8pm
solver.add(Sum([If(screen[i] == 3, 1, 0) for i in range(5)]) == 1)

# Condition 1: Western begins before horror
# western=4, horror=0
solver.add(time[4] < time[0])

# Condition 2: Sci-fi not on screen 3
# sci-fi=3
solver.add(screen[3] != 3)

# Condition 3: Romance not on screen 2
# romance=2
solver.add(screen[2] != 2)

# Condition 4: Horror and mystery on different screens
# horror=0, mystery=1
solver.add(screen[0] != screen[1])

# Now test each option for screen 1
# Option A: screen 1 has sci-fi(3) at 7pm and horror(0) at 9pm
opt_a = And(screen[3] == 1, time[3] == 7, screen[0] == 1, time[0] == 9)

# Option B: screen 1 has sci-fi(3) at 7pm and mystery(1) at 9pm
opt_b = And(screen[3] == 1, time[3] == 7, screen[1] == 1, time[1] == 9)

# Option C: screen 1 has western(4) at 7pm and horror(0) at 9pm
opt_c = And(screen[4] == 1, time[4] == 7, screen[0] == 1, time[0] == 9)

# Option D: screen 1 has western(4) at 7pm and mystery(1) at 9pm
opt_d = And(screen[4] == 1, time[4] == 7, screen[1] == 1, time[1] == 9)

# Option E: screen 1 has western(4) at 7pm and sci-fi(3) at 9pm
opt_e = And(screen[4] == 1, time[4] == 7, screen[3] == 1, time[3] == 9)

found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
        m = solver.model()
        print(f"Option {letter} is SAT:")
        for i in range(5):
            names = ["horror", "mystery", "romance", "sci-fi", "western"]
            print(f"  {names[i]}: screen={m[screen[i]]}, time={m[time[i]]}")
    else:
        print(f"Option {letter} is UNSAT")
    solver.pop()

print(f"\nFound options: {found_options}")

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    # The question asks which CANNOT be accurate. So we need the one that is NOT in found_options.
    all_options = ["A", "B", "C", "D", "E"]
    cannot_be = [o for o in all_options if o not in found_options]
    if len(cannot_be) == 1:
        print("STATUS: sat")
        print(f"answer:{cannot_be[0]}")
    else:
        print("STATUS: unsat")
        print(f"Refine: Multiple impossible options {cannot_be}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")