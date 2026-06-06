from z3 import *

solver = Solver()

# Houses: J, K, L, M, N, O, P
# Positions: 1-7 (1,2 = morning; 3,4,5 = afternoon; 6,7 = evening)
houses = ['J', 'K', 'L', 'M', 'N', 'O', 'P']
pos = {h: Int(f'pos_{h}') for h in houses}

# Each house has a unique position 1-7
for h in houses:
    solver.add(pos[h] >= 1, pos[h] <= 7)
solver.add(Distinct([pos[h] for h in houses]))

# Rule 1: J must be shown in the evening (positions 6 or 7)
solver.add(Or(pos['J'] == 6, pos['J'] == 7))

# Rule 2: K cannot be shown in the morning (not positions 1 or 2)
solver.add(pos['K'] != 1, pos['K'] != 2)

# Rule 3: L must be shown after K and before M
solver.add(pos['L'] > pos['K'])
solver.add(pos['L'] < pos['M'])

# Additional constraint: P is shown in the afternoon (positions 3, 4, or 5)
solver.add(Or(pos['P'] == 3, pos['P'] == 4, pos['P'] == 5))

# Define the answer options
opt_a_constr = Or(pos['J'] == 7)  # J is shown seventh
opt_b_constr = Or(pos['K'] == 3)  # K is shown third
opt_c_constr = Or(pos['N'] == 1)  # N is shown first
opt_d_constr = Or(pos['M'] == 3, pos['M'] == 4, pos['M'] == 5)  # M is shown in the afternoon
opt_e_constr = Or(pos['O'] == 1, pos['O'] == 2)  # O is shown in the morning

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