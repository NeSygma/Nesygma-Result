from z3 import *

# Define the houses and positions
houses = ['J', 'K', 'L', 'M', 'N', 'O', 'P']
positions = list(range(1, 8))  # 1 to 7

# Create a mapping from house to position variable
pos = {h: Int(f'pos_{h}') for h in houses}

solver = Solver()

# Each house must be assigned a unique position
solver.add(Distinct([pos[h] for h in houses]))

# Position bounds: each position between 1 and 7
for h in houses:
    solver.add(pos[h] >= 1)
    solver.add(pos[h] <= 7)

# Time slots: morning (1-2), afternoon (3-5), evening (6-7)
# Rule 1: J must be shown in the evening
solver.add(Or(pos['J'] == 6, pos['J'] == 7))

# Rule 2: K cannot be shown in the morning
solver.add(Or(pos['K'] >= 3))

# Rule 3: L must be shown after K and before M
solver.add(pos['L'] > pos['K'])
solver.add(pos['L'] < pos['M'])

# Base constraints are now added.

# Define the options as constraints using Z3 logical operators
opt_a_constr = (pos['K'] == 6)  # K is shown in the evening
opt_b_constr = And(pos['L'] >= 3, pos['L'] <= 5)  # L is shown in the afternoon
opt_c_constr = Or(pos['L'] == 6, pos['L'] == 7)  # L is shown in the evening
opt_d_constr = Or(pos['M'] == 1, pos['M'] == 2)  # M is shown in the morning
opt_e_constr = And(pos['M'] >= 3, pos['M'] <= 5)  # M is shown in the afternoon

# Use the exact skeleton provided
found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
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