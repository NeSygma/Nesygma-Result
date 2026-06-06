from z3 import *

# Slots:
# 0: screen 1, 7pm
# 1: screen 1, 9pm
# 2: screen 2, 7pm
# 3: screen 2, 9pm
# 4: screen 3, 8pm

# Time values: 7pm=0, 8pm=1, 9pm=2
# Screen values: 1, 2, 3

slot_time = [0, 2, 0, 2, 1]
slot_screen = [1, 1, 2, 2, 3]

movies = ['horror', 'mystery', 'romance', 'scifi', 'western']
H, M, R, S, W = 0, 1, 2, 3, 4

slot = [Int(f'slot_{m}') for m in movies]

solver = Solver()

for m in range(5):
    solver.add(slot[m] >= 0, slot[m] <= 4)

solver.add(Distinct(slot))

# Western before horror: time(W) < time(H)
# Use Or-loop pattern since slot[W] is symbolic
solver.add(Or([And(slot[W] == i, slot[H] == j, slot_time[i] < slot_time[j]) for i in range(5) for j in range(5)]))

# Sci-fi not on screen 3
solver.add(Or([And(slot[S] == i, slot_screen[i] != 3) for i in range(5)]))

# Romance not on screen 2
solver.add(Or([And(slot[R] == i, slot_screen[i] != 2) for i in range(5)]))

# Horror and mystery on different screens
solver.add(Or([And(slot[H] == i, slot[M] == j, slot_screen[i] != slot_screen[j]) for i in range(5) for j in range(5)]))

# Now evaluate each option.
options = {
    "A": ("scifi", "horror"),
    "B": ("scifi", "mystery"),
    "C": ("scifi", "western"),
    "D": ("western", "horror"),
    "E": ("western", "mystery")
}

movie_index = {"horror": H, "mystery": M, "romance": R, "scifi": S, "western": W}

found_options = []

for letter, (first, second) in options.items():
    solver.push()
    solver.add(slot[movie_index[first]] == 2)
    solver.add(slot[movie_index[second]] == 3)
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