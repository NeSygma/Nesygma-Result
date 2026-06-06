from z3 import *

# Define slots: 0:(1,7), 1:(1,9), 2:(2,7), 3:(2,9), 4:(3,8)
slot_screen = [1,1,2,2,3]
slot_time = [7,9,7,9,8]

movies = ['H','M','R','S','W']  # horror, mystery, romance, sci-fi, western
# Create Int variable for each movie representing slot index 0..4
slots = {m: Int(f'slot_{m}') for m in movies}
solver = Solver()
# each slot in range
for m in movies:
    solver.add(slots[m] >= 0, slots[m] <= 4)
# all distinct
solver.add(Distinct([slots[m] for m in movies]))
# Western before horror
solver.add(slot_time[slots['W']] < slot_time[slots['H']])
# Sci-fi not on screen3
solver.add(slot_screen[slots['S']] != 3)
# Romance not on screen2
solver.add(slot_screen[slots['R']] != 2)
# Horror and mystery different screens
solver.add(slot_screen[slots['H']] != slot_screen[slots['M']])

# Base constraints added

# Options for screen2 list (slot 2 then slot 3)
options = {
    'A': ('S','H'),
    'B': ('S','M'),
    'C': ('S','W'),
    'D': ('W','H'),
    'E': ('W','M')
}

found_sat = []
for letter, (first, second) in options.items():
    solver.push()
    # enforce that first movie is at slot 2 and second at slot 3
    solver.add(slots[first] == 2)
    solver.add(slots[second] == 3)
    if solver.check() == sat:
        found_sat.append(letter)
    solver.pop()

all_letters = set(options.keys())
impossible = all_letters - set(found_sat)
if len(impossible) == 1:
    ans = impossible.pop()
    print("STATUS: sat")
    print(f"answer:{ans}")
elif len(found_sat) == 1:
    # fallback if only one possible option (unlikely for this question)
    print("STATUS: sat")
    print(f"answer:{found_sat[0]}")
else:
    print("STATUS: unsat")
    print(f"Refine: found_sat={found_sat}, impossible={list(impossible)}")