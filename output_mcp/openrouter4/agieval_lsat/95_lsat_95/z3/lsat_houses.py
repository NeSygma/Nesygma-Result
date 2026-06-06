from z3 import *

solver = Solver()

# Houses: J, K, L, M, N, O, P
# Positions 1..7
# Morning: 1,2; Afternoon: 3,4,5; Evening: 6,7

houses = ['J', 'K', 'L', 'M', 'N', 'O', 'P']
pos = {h: Int(f'pos_{h}') for h in houses}

# Domain: each position is between 1 and 7
for h in houses:
    solver.add(pos[h] >= 1, pos[h] <= 7)

# All distinct positions
solver.add(Distinct([pos[h] for h in houses]))

# Rule 1: J must be shown in the evening (positions 6 or 7)
solver.add(Or(pos['J'] == 6, pos['J'] == 7))

# Rule 2: K cannot be shown in the morning (positions 1 or 2)
solver.add(pos['K'] != 1, pos['K'] != 2)

# Rule 3: L must be shown at some time after K and before M
solver.add(pos['L'] > pos['K'])
solver.add(pos['L'] < pos['M'])

# Now evaluate each option. For "must be true", we check if Not(option) is unsat.
# This means the option holds in all valid models.

options = {
    "A": pos['K'] >= 6,  # K is shown in the evening (pos 6 or 7)
    "B": Or(pos['L'] == 3, pos['L'] == 4, pos['L'] == 5),  # L is in the afternoon
    "C": Or(pos['L'] == 6, pos['L'] == 7),  # L is in the evening
    "D": Or(pos['M'] == 1, pos['M'] == 2),  # M is in the morning
    "E": Or(pos['M'] == 3, pos['M'] == 4, pos['M'] == 5),  # M is in the afternoon
}

found_options = []
for letter, constr in options.items():
    solver.push()
    solver.add(Not(constr))
    if solver.check() == unsat:
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