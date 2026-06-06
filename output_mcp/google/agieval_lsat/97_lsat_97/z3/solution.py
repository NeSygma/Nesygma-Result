from z3 import *

# Houses
houses = ['J', 'K', 'L', 'M', 'N', 'O', 'P']
pos = {h: Int(f'pos_{h}') for h in houses}

solver = Solver()

# 1. Positions are 1-7 and distinct
solver.add(Distinct([pos[h] for h in houses]))
for h in houses:
    solver.add(pos[h] >= 1, pos[h] <= 7)

# 2. Rules
# J must be shown in the evening (6 or 7)
solver.add(Or(pos['J'] == 6, pos['J'] == 7))

# K cannot be shown in the morning (K > 2)
solver.add(pos['K'] > 2)

# L must be shown at some time after K is shown and at some time before M is shown (K < L < M)
solver.add(pos['K'] < pos['L'])
solver.add(pos['L'] < pos['M'])

# Condition: P is shown in the afternoon (3, 4, or 5)
solver.add(Or(pos['P'] == 3, pos['P'] == 4, pos['P'] == 5))

# Options
# (A) J is shown seventh.
# (B) K is shown third.
# (C) N is shown first.
# (D) M is shown in the afternoon.
# (E) O is shown in the morning.
options = {
    'A': pos['J'] == 7,
    'B': pos['K'] == 3,
    'C': pos['N'] == 1,
    'D': And(pos['M'] >= 3, pos['M'] <= 5),
    'E': Or(pos['O'] == 1, pos['O'] == 2)
}

# Check which option MUST be true
# An option must be true if NOT(option) is unsatisfiable
found_options = []
for label, constraint in options.items():
    solver.push()
    solver.add(Not(constraint))
    if solver.check() == unsat:
        found_options.append(label)
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