from z3 import *
solver = Solver()
# Define houses
houses = ['J','K','L','M','N','O','P']  # 'O' represents the house labeled 0
# Position variables for each house
pos_of_house = {h: Int(f'pos_{h}') for h in houses}
# Domain constraints
for h in houses:
    solver.add(pos_of_house[h] >= 1, pos_of_house[h] <= 7)
# All houses at distinct positions
solver.add(Distinct([pos_of_house[h] for h in houses]))
# Base constraints
# J must be shown in the evening (positions 6 or 7)
solver.add(Or(pos_of_house['J'] == 6, pos_of_house['J'] == 7))
# K cannot be shown in the morning (positions 1 or 2)
solver.add(Or(pos_of_house['K'] == 3, pos_of_house['K'] == 4, pos_of_house['K'] == 5, pos_of_house['K'] == 6, pos_of_house['K'] == 7))
# L must be shown after K and before M
solver.add(pos_of_house['L'] > pos_of_house['K'])
solver.add(pos_of_house['L'] < pos_of_house['M'])
# Helper to create option constraints

def option_constraints(seq):
    # seq is list of 7 house labels in order from first to seventh
    return And([pos_of_house[seq[i]] == i+1 for i in range(7)])

opt_a_constr = option_constraints(['K','O','L','M','N','J','P'])
opt_b_constr = option_constraints(['N','L','P','K','M','O','J'])
opt_c_constr = option_constraints(['O','P','K','L','N','M','J'])
opt_d_constr = option_constraints(['O','P','M','N','K','L','J'])
opt_e_constr = option_constraints(['P','O','K','J','L','N','M'])

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