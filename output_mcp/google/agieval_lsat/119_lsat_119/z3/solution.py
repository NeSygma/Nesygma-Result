from z3 import *

# Bands
bands = ['U', 'V', 'W', 'X', 'Y', 'Z']
# Slots 1-6
# pos[band] = slot number
pos = {b: Int(f'pos_{b}') for b in bands}

solver = Solver()

# Each band in one slot
for b in bands:
    solver.add(pos[b] >= 1, pos[b] <= 6)

solver.add(Distinct([pos[b] for b in bands]))

# Constraints
# 1. V < Z
solver.add(pos['V'] < pos['Z'])
# 2. W < X
solver.add(pos['W'] < pos['X'])
# 3. Z < X
solver.add(pos['Z'] < pos['X'])
# 4. U in {4, 5, 6}
solver.add(Or(pos['U'] == 4, pos['U'] == 5, pos['U'] == 6))
# 5. Y in {1, 2, 3}
solver.add(Or(pos['Y'] == 1, pos['Y'] == 2, pos['Y'] == 3))

# Question condition: Z immediately before W
solver.add(pos['Z'] + 1 == pos['W'])

# Options
options = [
    ("A", pos['U'] == 5),
    ("B", pos['V'] == 1),
    ("C", pos['X'] == 5),
    ("D", pos['Y'] == 2),
    ("E", pos['Z'] == 3)
]

found_options = []
for letter, constr in options:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        # Check if it MUST be true (i.e., Not(constr) is unsat)
        solver.pop()
        solver.push()
        solver.add(Not(constr))
        if solver.check() == unsat:
            found_options.append(letter)
        solver.pop()
    else:
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