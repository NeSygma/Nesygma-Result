from z3 import *

# Let's rethink. The problem says:
# - 5 movies: horror, mystery, romance, sci-fi, western
# - Screens 1 and 2 show two movies each: one at 7pm, one at 9pm
# - Screen 3 shows exactly one movie at 8pm
# - Western begins before horror
# - Sci-fi not on screen 3
# - Romance not on screen 2
# - Horror and mystery on different screens

# The question: which CANNOT be an accurate list of movies on screen 2 (7pm first, then 9pm)?
# So we need to find which option is IMPOSSIBLE.

# Let's model more carefully. Each movie gets a screen (1,2,3) and a time.
# But the time is determined by screen: screen 1 or 2 -> time is either 7pm or 9pm.
# Screen 3 -> time is 8pm.

# Let's use a simpler encoding: each movie gets a slot.
# Slots: (1,7pm), (1,9pm), (2,7pm), (2,9pm), (3,8pm)
# That's 5 slots for 5 movies, a bijection.

# Slots:
# 0: screen 1, 7pm
# 1: screen 1, 9pm
# 2: screen 2, 7pm
# 3: screen 2, 9pm
# 4: screen 3, 8pm

# For each movie, assign a slot.
# Then constraints:
# - Western before horror: time(western) < time(horror). Times: 7pm < 8pm < 9pm.
#   So we need to map slots to time ordering.
#   Slot 0 (1,7pm) = time 0
#   Slot 1 (1,9pm) = time 2
#   Slot 2 (2,7pm) = time 0
#   Slot 3 (2,9pm) = time 2
#   Slot 4 (3,8pm) = time 1
# - Sci-fi not on screen 3: slot != 4
# - Romance not on screen 2: slot != 2 and slot != 3
# - Horror and mystery on different screens

movies = ['horror', 'mystery', 'romance', 'scifi', 'western']
H, M, R, S, W = 0, 1, 2, 3, 4

slot = [Int(f'slot_{m}') for m in movies]

solver = Solver()

# Domain: each slot 0..4
for m in range(5):
    solver.add(slot[m] >= 0, slot[m] <= 4)

# All different (bijection)
solver.add(Distinct(slot))

# Time mapping
# slot_time[0] = 0 (7pm)
# slot_time[1] = 2 (9pm)
# slot_time[2] = 0 (7pm)
# slot_time[3] = 2 (9pm)
# slot_time[4] = 1 (8pm)
def slot_time(s):
    return If(s == 0, 0, If(s == 1, 2, If(s == 2, 0, If(s == 3, 2, 1))))

# Screen mapping
# slot_screen[0] = 1
# slot_screen[1] = 1
# slot_screen[2] = 2
# slot_screen[3] = 2
# slot_screen[4] = 3
def slot_screen(s):
    return If(s == 0, 1, If(s == 1, 1, If(s == 2, 2, If(s == 3, 2, 3))))

# Western before horror: time(W) < time(H)
solver.add(slot_time(slot[W]) < slot_time(slot[H]))

# Sci-fi not on screen 3
solver.add(slot_screen(slot[S]) != 3)

# Romance not on screen 2
solver.add(slot_screen(slot[R]) != 2)

# Horror and mystery on different screens
solver.add(slot_screen(slot[H]) != slot_screen(slot[M]))

# Now evaluate each option.
# Each option lists two movies for screen 2, 7pm first then 9pm.
# So first movie is in slot 2 (screen 2, 7pm), second movie is in slot 3 (screen 2, 9pm).

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
    # first movie in slot 2 (screen 2, 7pm)
    solver.add(slot[movie_index[first]] == 2)
    # second movie in slot 3 (screen 2, 9pm)
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