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

# Verify the result
# We want to find which option MUST be true given the condition.
# This means for all models where (Constraints AND Condition) is true, Option must be true.
# Equivalently, there is no model where (Constraints AND Condition AND Not Option) is true.

for letter, opt_constr in options.items():
    solver.push()
    solver.add(condition)
    solver.add(Not(opt_constr))
    res = solver.check()
    if res == unsat:
        print(f"Option {letter} MUST be true.")
    else:
        print(f"Option {letter} is NOT necessarily true (counterexample found).")
        # print(solver.model())
    solver.pop()