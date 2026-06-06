from z3 import *

# Create solver
solver = Solver()

# Declare position variables for each house (1-7)
houses = ['J', 'K', 'L', 'M', 'N', 'O', 'P']
pos = {h: Int(f'pos_{h}') for h in houses}

# Base constraints
# 1. All positions are between 1 and 7
for h in houses:
    solver.add(pos[h] >= 1, pos[h] <= 7)

# 2. All positions are distinct (each house shown at different time)
solver.add(Distinct([pos[h] for h in houses]))

# 3. J must be shown in the evening (positions 6 or 7)
solver.add(Or(pos['J'] == 6, pos['J'] == 7))

# 4. K cannot be shown in the morning (positions 1 or 2)
solver.add(Or(pos['K'] == 3, pos['K'] == 4, pos['K'] == 5, pos['K'] == 6, pos['K'] == 7))

# 5. L must be shown after K and before M: K < L < M
solver.add(pos['K'] < pos['L'])
solver.add(pos['L'] < pos['M'])

# Now test each answer choice using the required skeleton
found_options = []

# Option A: K is shown at some time after J is shown
opt_a_constr = pos['K'] > pos['J']

# Option B: L is shown at some time after J is shown
opt_b_constr = pos['L'] > pos['J']

# Option C: P is shown at some time after J is shown
opt_c_constr = pos['P'] > pos['J']

# Option D: Both N and O are shown at some time after M is
opt_d_constr = And(pos['N'] > pos['M'], pos['O'] > pos['M'])

# Option E: Both N and P are shown at some time after K is
opt_e_constr = And(pos['N'] > pos['K'], pos['P'] > pos['K'])

for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), 
                      ("D", opt_d_constr), ("E", opt_e_constr)]:
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