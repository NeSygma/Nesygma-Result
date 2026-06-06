from z3 import *

# Singers
singers = ['K', 'L', 'T', 'W', 'Y', 'Z']
# Positions 1-6
pos = {s: Int(f'pos_{s}') for s in singers}

solver = Solver()

# 1. All positions are distinct and between 1 and 6
solver.add(Distinct([pos[s] for s in singers]))
for s in singers:
    solver.add(pos[s] >= 1, pos[s] <= 6)

# 2. Recorded: K, L. Not recorded: T, W, Y, Z.
# 4th audition cannot be recorded (K and L cannot be at 4)
solver.add(pos['K'] != 4)
solver.add(pos['L'] != 4)

# 3. 5th audition must be recorded (K or L must be at 5)
solver.add(Or(pos['K'] == 5, pos['L'] == 5))

# 4. Waite's audition must take place earlier than the two recorded auditions
solver.add(pos['W'] < pos['K'])
solver.add(pos['W'] < pos['L'])

# 5. Kammer's audition must take place earlier than Trillo's audition
solver.add(pos['K'] < pos['T'])

# 6. Zinn's audition must take place earlier than Yoshida's audition
solver.add(pos['Z'] < pos['Y'])

# Test each option for the 6th position
options = [('A', 'K'), ('B', 'L'), ('C', 'T'), ('D', 'W'), ('E', 'Z')]
found_options = []

for letter, singer in options:
    solver.push()
    solver.add(pos[singer] == 6)
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