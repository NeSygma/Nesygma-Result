from z3 import *

# Create solver
solver = Solver()

# Declare variables for each house's position (1-7)
houses = ['J', 'K', 'L', 'M', 'N', 'O', 'P']
pos = {h: Int(f'pos_{h}') for h in houses}

# All positions must be distinct and between 1 and 7
for h in houses:
    solver.add(pos[h] >= 1, pos[h] <= 7)
solver.add(Distinct([pos[h] for h in houses]))

# Time slot constraints
# Morning: positions 1, 2
# Afternoon: positions 3, 4, 5
# Evening: positions 6, 7

# Rule 1: J must be shown in the evening (position 6 or 7)
solver.add(Or(pos['J'] == 6, pos['J'] == 7))

# Rule 2: K cannot be shown in the morning (position 1 or 2)
solver.add(And(pos['K'] != 1, pos['K'] != 2))

# Rule 3: L must be shown after K and before M
solver.add(pos['K'] < pos['L'])
solver.add(pos['L'] < pos['M'])

# Now test each answer choice
# Each choice gives a specific order from first (position 1) to seventh (position 7)
# We need to encode that the order matches the given sequence

# Define the options as constraints
opt_a_constr = And(
    pos['K'] == 1, pos['O'] == 2, pos['L'] == 3, pos['M'] == 4, 
    pos['N'] == 5, pos['J'] == 6, pos['P'] == 7
)

opt_b_constr = And(
    pos['N'] == 1, pos['L'] == 2, pos['P'] == 3, pos['K'] == 4, 
    pos['M'] == 5, pos['O'] == 6, pos['J'] == 7
)

opt_c_constr = And(
    pos['O'] == 1, pos['P'] == 2, pos['K'] == 3, pos['L'] == 4, 
    pos['N'] == 5, pos['M'] == 6, pos['J'] == 7
)

opt_d_constr = And(
    pos['O'] == 1, pos['P'] == 2, pos['M'] == 3, pos['N'] == 4, 
    pos['K'] == 5, pos['L'] == 6, pos['J'] == 7
)

opt_e_constr = And(
    pos['P'] == 1, pos['O'] == 2, pos['K'] == 3, pos['J'] == 4, 
    pos['L'] == 5, pos['N'] == 6, pos['M'] == 7
)

# Test each option
found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), 
                       ("C", opt_c_constr), ("D", opt_d_constr), 
                       ("E", opt_e_constr)]:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
    solver.pop()

# Output results
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")