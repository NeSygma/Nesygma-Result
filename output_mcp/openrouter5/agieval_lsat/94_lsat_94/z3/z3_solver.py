from z3 import *

solver = Solver()

# Houses: J, K, L, M, N, O, P (7 houses)
houses = ['J', 'K', 'L', 'M', 'N', 'O', 'P']

# Each house gets a position from 1 to 7 (order of showing)
pos = {h: Int(f'pos_{h}') for h in houses}

# Domain constraints: each position is between 1 and 7
for h in houses:
    solver.add(pos[h] >= 1, pos[h] <= 7)

# All positions are distinct
solver.add(Distinct([pos[h] for h in houses]))

# Time-of-day constraints:
# Morning: positions 1, 2
# Afternoon: positions 3, 4, 5
# Evening: positions 6, 7

# Rule 1: J must be shown in the evening (positions 6 or 7)
solver.add(Or(pos['J'] == 6, pos['J'] == 7))

# Rule 2: K cannot be shown in the morning (cannot be positions 1 or 2)
solver.add(And(pos['K'] != 1, pos['K'] != 2))

# Rule 3: L must be shown at some time after K and before M
solver.add(pos['L'] > pos['K'])
solver.add(pos['L'] < pos['M'])

# Now evaluate each option: "X and Y cannot be shown consecutively in either order"
# That means there is NO valid schedule where X and Y are adjacent (|pos[X] - pos[Y]| == 1)
# We test: can X and Y be consecutive? If sat, they CAN be consecutive (so NOT the answer).
# If unsat, they CANNOT be consecutive (so IS the answer).

options = [
    ("A", pos['J'], pos['K']),
    ("B", pos['J'], pos['M']),
    ("C", pos['J'], pos['O']),
    ("D", pos['J'], pos['P']),
    ("E", pos['M'], pos['P']),
]

found_options = []
for letter, p1, p2 in options:
    solver.push()
    # They are consecutive: |p1 - p2| == 1
    solver.add(Or(p1 - p2 == 1, p2 - p1 == 1))
    if solver.check() == sat:
        # They CAN be consecutive -> not the answer
        pass
    else:
        # They CANNOT be consecutive -> this is the answer
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