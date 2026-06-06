from z3 import *

solver = Solver()

houses = ['J','K','L','M','N','O','P']
pos = {h: Int(f'pos_{h}') for h in houses}
for h in houses:
    solver.add(pos[h] >= 1, pos[h] <= 7)
solver.add(Distinct([pos[h] for h in houses]))
# constraints
solver.add(Or(pos['J'] == 6, pos['J'] == 7))
solver.add(Not(Or(pos['K'] == 1, pos['K'] == 2))
solver.add(pos['K'] < pos['L'], pos['L'] < pos['M'])
solver.add(Or(pos['P'] == 3, pos['P'] == 4, pos['P'] == 5))

# options
opt_a = (pos['J'] == 7)
opt_b = (pos['K'] == 3)
opt_c = (pos['N'] == 1)
opt_d = Or(pos['M'] == 3, pos['M'] == 4, pos['M'] == 5)
opt_e = Or(pos['O'] == 1, pos['O'] == 2)
options = [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]

forced = []
for letter, constr in options:
    solver.push()
    # add negation of option; if unsat, then option forced true
    solver.add(Not(constr))
    if solver.check() == unsat:
        forced.append(letter)
    solver.pop()

if len(forced) == 1:
    print("STATUS: sat")
    print(f"answer:{forced[0]}")
elif len(forced) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple forced options {forced}")
else:
    print("STATUS: unsat")
    print("Refine: No forced option found")