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

impossible = []
for letter, singer in option_map.items():
    solver.push()
    solver.add(pos[singer] == 2)
    if solver.check() == unsat:
        impossible.append(letter)
    solver.pop()

if len(impossible) == 1:
    print("STATUS: sat")
    print(f"answer:{impossible[0]}")
elif len(impossible) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple impossible options {impossible}")
else:
    print("STATUS: unsat")
    print("Refine: No impossible options found")