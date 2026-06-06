from z3 import *

solver = Solver()

# Define position variables for each house
houses = ['J', 'K', 'L', 'M', 'N', 'O', 'P']
pos = {h: Int(f'pos_{h}') for h in houses}

# All positions are distinct and in 1..7
for h in houses:
    solver.add(pos[h] >= 1, pos[h] <= 7)
solver.add(Distinct([pos[h] for h in houses]))

# Time-of-day constraints (implicit in positions)
# J must be in evening (positions 6 or 7)
solver.add(Or(pos['J'] == 6, pos['J'] == 7))

# K cannot be in morning (positions 1 or 2)
solver.add(Or(pos['K'] >= 3, pos['K'] <= 2))  # Actually, K cannot be 1 or 2, so K >= 3
solver.add(pos['K'] >= 3)

# L after K and before M
solver.add(pos['L'] > pos['K'])
solver.add(pos['L'] < pos['M'])

# P in afternoon (positions 3,4,5)
solver.add(Or(pos['P'] == 3, pos['P'] == 4, pos['P'] == 5))

# Define option constraints
opt_a_constr = (pos['J'] == 7)
opt_b_constr = (pos['K'] == 3)
opt_c_constr = (pos['N'] == 1)
opt_d_constr = And(pos['M'] >= 3, pos['M'] <= 5)
opt_e_constr = (pos['O'] <= 2)

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