from z3 import *

solver = Solver()

# Movie IDs: 0=horror, 1=mystery, 2=romance, 3=sci-fi, 4=western
slot = [Int(f'slot_{m}') for m in range(5)]  # slot[m] = slot index for movie m

# Slot definitions: index 0..4
slot_screen = [1, 1, 2, 2, 3]   # screen for each slot index
slot_time   = [7, 9, 7, 9, 8]   # time for each slot index

# Time variables for western and horror (to compare easily)
time_w = Int('time_w')
time_h = Int('time_h')

# Base constraints
# 1. All slots distinct
solver.add(Distinct(slot))

# 2. Each slot index between 0 and 4
for m in range(5):
    solver.add(slot[m] >= 0, slot[m] <= 4)

# 3. Sci-fi not on screen 3
solver.add(Or([And(slot[3] == i, slot_screen[i] != 3) for i in range(5)]))

# 4. Romance not on screen 2
solver.add(Or([And(slot[2] == i, slot_screen[i] != 2) for i in range(5)]))

# 5. Horror and mystery on different screens
# Not both in screen1 (slots 0,1)
solver.add(Not(And(Or(slot[0]==0, slot[0]==1), Or(slot[1]==0, slot[1]==1))))
# Not both in screen2 (slots 2,3)
solver.add(Not(And(Or(slot[0]==2, slot[0]==3), Or(slot[1]==2, slot[1]==3))))

# 6. Western before horror: time_w < time_h
solver.add(Or([And(slot[4] == i, time_w == slot_time[i]) for i in range(5)]))
solver.add(Or([And(slot[0] == i, time_h == slot_time[i]) for i in range(5)]))
solver.add(time_w < time_h)

# Now test each option for screen 2
# Screen 2 slots: slot2 (index 2) = 7 PM, slot3 (index 3) = 9 PM
# Options: (letter, movie1, movie2) where movie1 is at 7 PM, movie2 at 9 PM
options = [
    ("A", 3, 0),  # sci-fi, horror
    ("B", 3, 1),  # sci-fi, mystery
    ("C", 3, 4),  # sci-fi, western
    ("D", 4, 0),  # western, horror
    ("E", 4, 1),  # western, mystery
]

impossible_options = []
for letter, movie1, movie2 in options:
    solver.push()
    # movie1 at slot2 (index 2), movie2 at slot3 (index 3)
    solver.add(slot[movie1] == 2)
    solver.add(slot[movie2] == 3)
    if solver.check() == unsat:
        impossible_options.append(letter)
    solver.pop()

if len(impossible_options) == 1:
    print("STATUS: sat")
    print(f"answer:{impossible_options[0]}")
elif len(impossible_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {impossible_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")