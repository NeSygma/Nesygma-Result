from z3 import *

solver = Solver()

# Houses: J, K, L, M, N, O, P
# Positions 1-7 (1-indexed)
# Morning: positions 1, 2
# Afternoon: positions 3, 4, 5
# Evening: positions 6, 7

houses = ['J', 'K', 'L', 'M', 'N', 'O', 'P']
pos = {h: Int(f'pos_{h}') for h in houses}

# All positions are between 1 and 7
for h in houses:
    solver.add(pos[h] >= 1, pos[h] <= 7)

# All houses have distinct positions
solver.add(Distinct([pos[h] for h in houses]))

# Rule 1: J must be shown in the evening (positions 6 or 7)
solver.add(Or(pos['J'] == 6, pos['J'] == 7))

# Rule 2: K cannot be shown in the morning (positions 1 or 2)
solver.add(And(pos['K'] != 1, pos['K'] != 2))

# Rule 3: L must be shown after K and before M
solver.add(pos['L'] > pos['K'])
solver.add(pos['L'] < pos['M'])

# Now check each answer option: which pair CANNOT be shown consecutively?
# "Cannot be shown consecutively in either order" means:
# For each option, we check if it's possible for those two houses to be consecutive.
# If it's NOT possible (unsat), then that pair CANNOT be shown consecutively.

options = {
    "A": ('J', 'K'),
    "B": ('J', 'M'),
    "C": ('J', 'O'),
    "D": ('J', 'P'),
    "E": ('M', 'P'),
}

found_options = []

for letter, (h1, h2) in options.items():
    solver.push()
    # Consecutive means |pos[h1] - pos[h2]| == 1
    solver.add(Or(pos[h1] - pos[h2] == 1, pos[h2] - pos[h1] == 1))
    if solver.check() == sat:
        found_options.append(letter)
    solver.pop()

# We want the pair that CANNOT be consecutive.
# So we look for options that are NOT in found_options.
cannot_be_consecutive = [letter for letter in options if letter not in found_options]

if len(cannot_be_consecutive) == 1:
    print("STATUS: sat")
    print(f"answer:{cannot_be_consecutive[0]}")
elif len(cannot_be_consecutive) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options cannot be consecutive {cannot_be_consecutive}")
else:
    print("STATUS: unsat")
    print("Refine: All options can be consecutive")