from z3 import *

solver = Solver()

# Define position variables for each house
houses = ['J', 'K', 'L', 'M', 'N', 'O', 'P']
pos = {h: Int(f'pos_{h}') for h in houses}

# All positions are distinct and in 1..7
for h in houses:
    solver.add(pos[h] >= 1, pos[h] <= 7)
solver.add(Distinct([pos[h] for h in houses]))

# J must be in evening (positions 6 or 7)
solver.add(Or(pos['J'] == 6, pos['J'] == 7))

# K cannot be in morning (positions 1 or 2)
solver.add(pos['K'] >= 3)

# L after K and before M
solver.add(pos['L'] > pos['K'])
solver.add(pos['L'] < pos['M'])

# P in afternoon (positions 3,4,5)
solver.add(Or(pos['P'] == 3, pos['P'] == 4, pos['P'] == 5))

# Define option constraints (the statement we test for necessity)
opt_a = (pos['J'] == 7)
opt_b = (pos['K'] == 3)
opt_c = (pos['N'] == 1)
opt_d = And(pos['M'] >= 3, pos['M'] <= 5)
opt_e = (pos['O'] <= 2)

# For each option, check if its negation is unsatisfiable
necessary_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(Not(constr))
    if solver.check() == unsat:
        necessary_options.append(letter)
    solver.pop()

print(f"Necessary options: {necessary_options}")

if len(necessary_options) == 1:
    print("STATUS: sat")
    print(f"answer:{necessary_options[0]}")
elif len(necessary_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple necessary options found {necessary_options}")
else:
    print("STATUS: unsat")
    print("Refine: No necessary options found")