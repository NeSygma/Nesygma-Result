from z3 import *

# BENCHMARK_MODE: ON (model-finding mode)
BENCHMARK_MODE = True

# Declare the houses as symbolic constants
Houses = ['J', 'K', 'L', 'M', 'N', 'O', 'P']

# Create a solver
solver = Solver()

# Position variables: pos[i] is the position (0-6) of house i
pos = {h: Int(f'pos_{h}') for h in Houses}

# Each position 0-6 must be assigned to exactly one house
solver.add(Distinct(list(pos.values())))
for i in range(7):
    solver.add(Or([pos[h] == i for h in Houses]))

# Time slot constraints:
# Morning: positions 0, 1
# Afternoon: positions 2, 3, 4
# Evening: positions 5, 6

# Rule 1: J must be shown in the evening (positions 5 or 6)
solver.add(Or(pos['J'] == 5, pos['J'] == 6))

# Rule 2: K cannot be shown in the morning (positions 0 or 1)
solver.add(Not(Or(pos['K'] == 0, pos['K'] == 1)))

# Rule 3: L must be shown after K and before M
# pos[K] < pos[L] < pos[M]
solver.add(pos['K'] < pos['L'])
solver.add(pos['L'] < pos['M'])

# Base constraints are now set. Now evaluate each multiple-choice option.

# Define the options as pairs of houses
options = [
    ("A", ['J', 'K']),
    ("B", ['J', 'M']),
    ("C", ['J', 'O']),
    ("D", ['J', 'P']),
    ("E", ['M', 'P'])
]

found_options = []

for letter, pair in options:
    solver.push()
    h1, h2 = pair
    # Check if the pair can be consecutive in either order
    # i.e., pos[h1] == pos[h2] + 1 or pos[h2] == pos[h1] + 1
    solver.add(Or(
        pos[h1] == pos[h2] + 1,
        pos[h2] == pos[h1] + 1
    ))
    
    if solver.check() == sat:
        found_options.append(letter)
    solver.pop()

# Determine the result
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")