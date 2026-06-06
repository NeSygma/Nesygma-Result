from z3 import *

solver = Solver()

# Positions 1-7
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
solver.add(And(pos['K'] != 1, pos['K'] != 2))

# Rule 3: L must be after K and before M
solver.add(pos['L'] > pos['K'])
solver.add(pos['M'] > pos['L'])

# Time-of-day constraints (not strictly necessary but help reasoning)
# Morning: positions 1-2, Afternoon: 3-5, Evening: 6-7

# Option A: K is shown at some time after J is shown.
opt_a = (pos['K'] > pos['J'])

# Option B: L is shown at some time after J is shown.
opt_b = (pos['L'] > pos['J'])

# Option C: P is shown at some time after J is shown.
opt_c = (pos['P'] > pos['J'])

# Option D: Both N and O are shown at some time after M is shown.
opt_d = And(pos['N'] > pos['M'], pos['O'] > pos['M'])

# Option E: Both N and P are shown at some time after K is shown.
opt_e = And(pos['N'] > pos['K'], pos['P'] > pos['K'])

found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
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