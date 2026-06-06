from z3 import *

solver = Solver()

# Declare symbolic variables for the order of houses (0 to 6)
# Each variable represents the time slot (0=first, 1=second, ..., 6=seventh)
# The value assigned to each house is its position in the sequence.
houses = ['J', 'K', 'L', 'M', 'N', 'O', 'P']
positions = {h: Int(f'pos_{h}') for h in houses}

# All positions must be distinct and in the range 0 to 6
solver.add(Distinct(list(positions.values())))
for h in houses:
    solver.add(positions[h] >= 0, positions[h] <= 6)

# Morning: positions 0 and 1
# Afternoon: positions 2, 3, 4
# Evening: positions 5 and 6

# Rule 1: J must be shown in the evening (positions 5 or 6)
solver.add(Or(positions['J'] == 5, positions['J'] == 6))

# Rule 2: K cannot be shown in the morning (positions 0 or 1)
solver.add(Not(Or(positions['K'] == 0, positions['K'] == 1)))

# Rule 3: L must be shown after K and before M
# This means: K < L < M in terms of positions
solver.add(positions['K'] < positions['L'])
solver.add(positions['L'] < positions['M'])

# Additional constraint: P is shown in the afternoon (positions 2, 3, or 4)
solver.add(Or(positions['P'] == 2, positions['P'] == 3, positions['P'] == 4))

# Base constraints are set. Now evaluate each option.

# Define the options as constraints
# (A) J is shown seventh (position 6)
opt_a_constr = (positions['J'] == 6)

# (B) K is shown third (position 2)
opt_b_constr = (positions['K'] == 2)

# (C) N is shown first (position 0)
opt_c_constr = (positions['N'] == 0)

# (D) M is shown in the afternoon (positions 2, 3, or 4)
opt_d_constr = Or(positions['M'] == 2, positions['M'] == 3, positions['M'] == 4)

# (E) O is shown in the morning (positions 0 or 1)
opt_e_constr = Or(positions['O'] == 0, positions['O'] == 1)

# Evaluate each option
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