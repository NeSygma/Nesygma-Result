from z3 import *

# Singers
singers = ['K', 'L', 'T', 'W', 'Y', 'Z']
# Positions 0-5
# pos_of[singer] = position index
pos_of = {s: Int(f'pos_{s}') for s in singers}

solver = Solver()

# Domain constraints
for s in singers:
    solver.add(pos_of[s] >= 0, pos_of[s] <= 5)

# All positions distinct
solver.add(Distinct([pos_of[s] for s in singers]))

# Recorded: K, L
# Not recorded: T, W, Y, Z
is_recorded = lambda s: Or(s == 'K', s == 'L')

# 1. The fourth audition (index 3) cannot be recorded.
# So, pos_of[K] != 3 and pos_of[L] != 3
solver.add(pos_of['K'] != 3)
solver.add(pos_of['L'] != 3)

# 2. The fifth audition (index 4) must be recorded.
# So, pos_of[K] == 4 or pos_of[L] == 4
solver.add(Or(pos_of['K'] == 4, pos_of['L'] == 4))

# 3. Waite's audition must take place earlier than the two recorded auditions.
solver.add(pos_of['W'] < pos_of['K'])
solver.add(pos_of['W'] < pos_of['L'])

# 4. Kammer's audition must take place earlier than Trillo's audition.
solver.add(pos_of['K'] < pos_of['T'])

# 5. Zinn's audition must take place earlier than Yoshida's audition.
solver.add(pos_of['Z'] < pos_of['Y'])

# Define options
# (A) Kammer, Trillo, Zinn, Waite, Lugo, Yoshida
# (B) Waite, Kammer, Yoshida, Zinn, Lugo, Trillo
# (C) Waite, Lugo, Kammer, Trillo, Zinn, Yoshida
# (D) Waite, Zinn, Kammer, Trillo, Lugo, Yoshida
# (E) Zinn, Yoshida, Waite, Lugo, Kammer, Trillo

def check_option(order):
    # order is a list of singers in order 1st to 6th
    constraints = []
    for i, s in enumerate(order):
        constraints.append(pos_of[s] == i)
    return And(constraints)

options = [
    ("A", ['K', 'T', 'Z', 'W', 'L', 'Y']),
    ("B", ['W', 'K', 'Y', 'Z', 'L', 'T']),
    ("C", ['W', 'L', 'K', 'T', 'Z', 'Y']),
    ("D", ['W', 'Z', 'K', 'T', 'L', 'Y']),
    ("E", ['Z', 'Y', 'W', 'L', 'K', 'T'])
]

found_options = []
for letter, order in options:
    solver.push()
    solver.add(check_option(order))
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