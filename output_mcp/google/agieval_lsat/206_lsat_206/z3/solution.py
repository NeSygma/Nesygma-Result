from z3 import *

# Singers
singers = ['K', 'L', 'T', 'W', 'Y', 'Z']
pos = {s: Int(f'pos_{s}') for s in singers}

solver = Solver()

# Positions are 1 to 6
for s in singers:
    solver.add(pos[s] >= 1, pos[s] <= 6)

# All positions are distinct
solver.add(Distinct([pos[s] for s in singers]))

# Condition 1: 4th audition cannot be recorded (K or L)
solver.add(pos['K'] != 4)
solver.add(pos['L'] != 4)

# Condition 2: 5th audition must be recorded (K or L)
solver.add(Or(pos['K'] == 5, pos['L'] == 5))

# Condition 3: W must be earlier than the two recorded auditions (K and L)
solver.add(pos['W'] < pos['K'])
solver.add(pos['W'] < pos['L'])

# Condition 4: K must be earlier than T
solver.add(pos['K'] < pos['T'])

# Condition 5: Z must be earlier than Y
solver.add(pos['Z'] < pos['Y'])

# Test options for Y's position
options = [
    ("A", 5),
    ("B", 4),
    ("C", 3),
    ("D", 2),
    ("E", 1)
]

found_options = []
for letter, p in options:
    solver.push()
    solver.add(pos['Y'] == p)
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