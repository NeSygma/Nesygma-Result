from z3 import *

# Define singers and positions
singers = ['K','L','T','W','Y','Z']  # Kammer, Lugo, Trillo, Waite, Yoshida, Zinn
pos = {s: Int(s) for s in singers}
solver = Solver()
# Domain constraints: positions 1..6
for v in pos.values():
    solver.add(v >= 1, v <= 6)
# All different positions
solver.add(Distinct([pos[s] for s in singers]))
# Recorded auditions: Kammer (K) and Lugo (L)
# Fourth audition cannot be recorded
solver.add(pos['K'] != 4, pos['L'] != 4)
# Fifth audition must be recorded (so either K or L is at position 5)
solver.add(Or(pos['K'] == 5, pos['L'] == 5))
# Waite (W) earlier than both recorded auditions
solver.add(pos['W'] < pos['K'])
solver.add(pos['W'] < pos['L'])
# Kammer earlier than Trillo
solver.add(pos['K'] < pos['T'])
# Zinn earlier than Yoshida
solver.add(pos['Z'] < pos['Y'])

# Map answer letters to the singer that would be second
option_map = {
    "A": 'K',  # Kammer
    "B": 'L',  # Lugo
    "C": 'T',  # Trillo
    "D": 'W',  # Waite
    "E": 'Z'   # Zinn
}

found_options = []
for letter, singer in option_map.items():
    solver.push()
    solver.add(pos[singer] == 2)  # enforce this singer as second audition
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