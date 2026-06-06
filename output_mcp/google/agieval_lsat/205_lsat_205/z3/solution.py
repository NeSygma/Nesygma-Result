from z3 import *

# Singers
singers = ['K', 'L', 'T', 'W', 'Y', 'Z']
pos = {s: Int(s) for s in singers}

solver = Solver()

# Positions are 1-6
for s in singers:
    solver.add(pos[s] >= 1, pos[s] <= 6)

# All positions are distinct
solver.add(Distinct([pos[s] for s in singers]))

# Condition 1: 4th audition cannot be recorded (K, L)
solver.add(pos['K'] != 4)
solver.add(pos['L'] != 4)

# Condition 2: 5th audition must be recorded (K, L)
solver.add(Or(pos['K'] == 5, pos['L'] == 5))

# Condition 3: W < K and W < L
solver.add(pos['W'] < pos['K'])
solver.add(pos['W'] < pos['L'])

# Condition 4: K < T
solver.add(pos['K'] < pos['T'])

# Condition 5: Z < Y
solver.add(pos['Z'] < pos['Y'])

# Question constraint: K is immediately before Y
solver.add(pos['Y'] == pos['K'] + 1)

# Test options
options = [
    ("A", pos['K'] == 2),
    ("B", pos['T'] == 4),
    ("C", pos['W'] == 3),
    ("D", pos['Y'] == 6),
    ("E", pos['Z'] == 2)
]

found_options = []
for letter, constr in options:
    solver.push()
    solver.add(constr)
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