from z3 import *

# Singers
singers = ['K', 'L', 'T', 'W', 'Y', 'Z']
pos = {s: Int(f'pos_{s}') for s in singers}

solver = Solver()

# 1. Positions are 1-6 and distinct
solver.add(Distinct([pos[s] for s in singers]))
for s in singers:
    solver.add(pos[s] >= 1, pos[s] <= 6)

# 2. Conditions
# Kammer's audition and Lugo's audition will be recorded; the other four will not be.
# The fourth audition cannot be recorded.
# The fifth audition must be recorded.
# Waite's audition must take place earlier than the two recorded auditions.
# Kammer's audition must take place earlier than Trillo's audition.
# Zinn's audition must take place earlier than Yoshida's audition.

# Recorded: K, L
# Not recorded: T, W, Y, Z
# 4th is not recorded: pos[K] != 4, pos[L] != 4
# 5th is recorded: pos[K] == 5 or pos[L] == 5
# W < K and W < L
# K < T
# Z < Y

solver.add(pos['K'] != 4)
solver.add(pos['L'] != 4)
solver.add(Or(pos['K'] == 5, pos['L'] == 5))
solver.add(pos['W'] < pos['K'])
solver.add(pos['W'] < pos['L'])
solver.add(pos['K'] < pos['T'])
solver.add(pos['Z'] < pos['Y'])

# Test each option
options = {
    'A': 'K',
    'B': 'L',
    'C': 'T',
    'D': 'W',
    'E': 'Z'
}

# We want to find which one CANNOT be the second audition.
# So we check each option: if pos[singer] == 2 is UNSAT, that's our answer.

found_options = []
for label, singer in options.items():
    solver.push()
    solver.add(pos[singer] == 2)
    if solver.check() == unsat:
        found_options.append(label)
    solver.pop()

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
else:
    print("STATUS: unsat")
    print(f"Refine: Found {found_options}")