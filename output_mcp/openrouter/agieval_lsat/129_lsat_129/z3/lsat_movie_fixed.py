from z3 import *

# Slots: index -> (screen, time)
slot_screen = [1, 1, 2, 2, 3]
slot_time   = [7, 9, 7, 9, 8]

movies = ['H','M','R','S','W']  # horror, mystery, romance, sci-fi, western
slots = {m: Int(f'slot_{m}') for m in movies}
solver = Solver()
# domain constraints
for m in movies:
    solver.add(slots[m] >= 0, slots[m] <= 4)
# all distinct slots
solver.add(Distinct([slots[m] for m in movies]))
# Western before horror (time)
solver.add(Or([And(slots['W']==i, slots['H']==j, slot_time[i] < slot_time[j])
               for i in range(5) for j in range(5)]))
# Sci-fi not on screen 3
solver.add(Or([And(slots['S']==i, slot_screen[i] != 3) for i in range(5)]))
# Romance not on screen 2
solver.add(Or([And(slots['R']==i, slot_screen[i] != 2) for i in range(5)]))
# Horror and mystery on different screens
solver.add(Or([And(slots['H']==i, slots['M']==j, slot_screen[i] != slot_screen[j])
               for i in range(5) for j in range(5)]))

# Options for screen 2 (slot 2 then slot 3)
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
    solver.add(slots[first] == 2)   # 7pm on screen2
    solver.add(slots[second] == 3)  # 9pm on screen2
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
    # fallback if only one possible (unlikely)
    print("STATUS: sat")
    print(f"answer:{found_sat[0]}")
else:
    print("STATUS: unsat")
    print(f"Refine: found_sat={found_sat}, impossible={list(impossible)}")