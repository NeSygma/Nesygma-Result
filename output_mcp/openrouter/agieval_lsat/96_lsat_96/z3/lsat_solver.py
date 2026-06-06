from z3 import *

solver = Solver()
# Variables for positions 1..7
houses = ['J','K','L','M','N','O','P']
pos = {h: Int(f'pos_{h}') for h in houses}
# Domain constraints
for h in houses:
    solver.add(pos[h] >= 1, pos[h] <= 7)
# All distinct
solver.add(Distinct([pos[h] for h in houses]))
# Base constraints
# J in evening (6 or 7)
solver.add(Or(pos['J'] == 6, pos['J'] == 7))
# K not in morning (not 1 or 2)
solver.add(Not(Or(pos['K'] == 1, pos['K'] == 2)))
# L after K and before M
solver.add(pos['K'] < pos['L'], pos['L'] < pos['M'])

# Define option constraints
opt_a = And(pos['K'] > pos['J'])
opt_b = And(pos['L'] > pos['J'])
opt_c = And(pos['P'] > pos['J'])
opt_d = And(pos['N'] > pos['M'], pos['O'] > pos['M'])
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