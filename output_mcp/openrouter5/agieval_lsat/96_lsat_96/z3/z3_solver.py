from z3 import *

solver = Solver()

# 7 houses: J, K, L, M, N, O, P
# Positions 0-6: 0=morning1, 1=morning2, 2=afternoon1, 3=afternoon2, 4=afternoon3, 5=evening1, 6=evening2
houses = ['J', 'K', 'L', 'M', 'N', 'O', 'P']
pos = {h: Int(f'pos_{h}') for h in houses}

# Each position is between 0 and 6
for h in houses:
    solver.add(pos[h] >= 0, pos[h] <= 6)

# All positions distinct
solver.add(Distinct([pos[h] for h in houses]))

# J must be shown in the evening (positions 5 and 6)
solver.add(Or(pos['J'] == 5, pos['J'] == 6))

# K cannot be shown in the morning (positions 0 and 1)
solver.add(Not(Or(pos['K'] == 0, pos['K'] == 1)))

# L must be shown at some time after K and before M
solver.add(pos['L'] > pos['K'])
solver.add(pos['L'] < pos['M'])

# Now evaluate each option
found_options = []

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