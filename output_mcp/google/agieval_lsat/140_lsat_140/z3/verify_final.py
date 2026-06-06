from z3 import *

# Define the members
members = ['G', 'K', 'P', 'S', 'T', 'V']
pos = {m: Int(f'pos_{m}') for m in members}

solver = Solver()

# Each member performs exactly one solo (1-6)
for m in members:
    solver.add(pos[m] >= 1, pos[m] <= 6)
solver.add(Distinct([pos[m] for m in members]))

# Constraints
solver.add(pos['G'] != 4)
solver.add(pos['P'] < pos['K'])
solver.add(pos['V'] < pos['K'])
solver.add(pos['K'] < pos['G'])
solver.add(Xor(pos['S'] > pos['P'], pos['S'] > pos['T']))

# Question condition
condition = pos['P'] < pos['S']

# Options
options = {
    "A": pos['P'] == 1,
    "B": pos['P'] == 2,
    "C": pos['V'] < pos['S'],
    "D": pos['P'] < pos['T'],
    "E": pos['S'] < pos['K']
}

# Check each option
found_options = []
for letter, opt_constr in options.items():
    solver.push()
    solver.add(condition)
    solver.add(opt_constr)
    if solver.check() == sat:
        # Check if it's *necessarily* true
        solver.pop()
        solver.push()
        solver.add(condition)
        solver.add(Not(opt_constr))
        if solver.check() == unsat:
            found_options.append(letter)
        solver.pop()
    else:
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