from z3 import *

solver = Solver()

# Declare position variables for each house
houses = ['J', 'K', 'L', 'M', 'N', 'O', 'P']
pos = {h: Int(f'pos_{h}') for h in houses}

# All positions between 1 and 7
for h in houses:
    solver.add(pos[h] >= 1, pos[h] <= 7)

# All distinct
solver.add(Distinct([pos[h] for h in houses]))

# Constraint 1: J in evening (positions 6 or 7)
solver.add(Or(pos['J'] == 6, pos['J'] == 7))

# Constraint 2: K not in morning (positions 1 or 2)
solver.add(Not(Or(pos['K'] == 1, pos['K'] == 2)))

# Constraint 3: L after K and before M
solver.add(pos['L'] > pos['K'])
solver.add(pos['L'] < pos['M'])

# Now test each option: we want the pair that CANNOT be shown consecutively in either order.
# For each pair, we check if there exists a schedule where they are consecutive.
# If unsat, then they cannot be consecutive.

found_options = []
options = [
    ("A", ("J", "K")),
    ("B", ("J", "M")),
    ("C", ("J", "O")),
    ("D", ("J", "P")),
    ("E", ("M", "P"))
]

for letter, (house1, house2) in options:
    solver.push()
    # Add constraint that they are consecutive in either order
    solver.add(Or(pos[house1] == pos[house2] + 1, pos[house2] == pos[house1] + 1))
    result = solver.check()
    if result == unsat:
        found_options.append(letter)
    solver.pop()

# According to the problem, exactly one pair cannot be consecutive.
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")