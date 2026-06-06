from z3 import *

solver = Solver()

# Movies: H, M, R, S, W
h, m, r, s, w = Ints('h m r s w')

# Slots 1..5
slots = [h, m, r, s, w]
for var in slots:
    solver.add(var >= 1, var <= 5)

# All different
solver.add(Distinct([h, m, r, s, w]))

# time_of_slot[i-1] for i in 1..5
time_of_slot = [7, 9, 7, 9, 8]
screen_of_slot = [1, 1, 2, 2, 3]

# Western before horror: time(s_w) < time(s_h)
solver.add(Or([And(w == i, h == j, time_of_slot[i-1] < time_of_slot[j-1]) for i in range(1,6) for j in range(1,6)]))

# Sci-fi not on screen 3: screen(s_s) != 3
solver.add(Or([And(s == i, screen_of_slot[i-1] != 3) for i in range(1,6)]))

# Romance not on screen 2: screen(s_r) != 2
solver.add(Or([And(r == i, screen_of_slot[i-1] != 2) for i in range(1,6)]))

# Horror and mystery on different screens: screen(s_h) != screen(s_m)
solver.add(Or([And(h == i, m == j, screen_of_slot[i-1] != screen_of_slot[j-1]) for i in range(1,6) for j in range(1,6)]))

# Additional condition: sci-fi and romance on same screen
solver.add(Or([And(s == i, r == j, screen_of_slot[i-1] == screen_of_slot[j-1]) for i in range(1,6) for j in range(1,6)]))

# Now check each option
options = {
    "A": lambda: Or([And(w == i, time_of_slot[i-1] == 7) for i in range(1,6)]),
    "B": lambda: Or([And(s == i, time_of_slot[i-1] == 9) for i in range(1,6)]),
    "C": lambda: Or([And(m == i, time_of_slot[i-1] == 8) for i in range(1,6)]),
    "D": lambda: Or([And(r == i, time_of_slot[i-1] == 9) for i in range(1,6)]),
    "E": lambda: Or([And(h == i, time_of_slot[i-1] == 8) for i in range(1,6)])
}

found = []
for letter, constr in options.items():
    solver.push()
    solver.add(constr())
    if solver.check() == sat:
        found.append(letter)
    solver.pop()

if len(found) == 1:
    print("STATUS: sat")
    print(f"answer:{found[0]}")
elif len(found) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")