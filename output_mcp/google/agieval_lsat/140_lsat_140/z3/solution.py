from z3 import *

# Define the members
members = ['G', 'K', 'P', 'S', 'T', 'V']
# pos[m] is the position of member m (1-6)
pos = {m: Int(f'pos_{m}') for m in members}

solver = Solver()

# Each member performs exactly one solo (1-6)
for m in members:
    solver.add(pos[m] >= 1, pos[m] <= 6)
solver.add(Distinct([pos[m] for m in members]))

# Constraints
# 1. The guitarist does not perform the fourth solo.
solver.add(pos['G'] != 4)
# 2. The percussionist performs a solo at some time before the keyboard player does.
solver.add(pos['P'] < pos['K'])
# 3. The keyboard player performs a solo at some time after the violinist does
solver.add(pos['V'] < pos['K'])
# 4. and at some time before the guitarist does.
solver.add(pos['K'] < pos['G'])
# 5. The saxophonist performs a solo at some time after either the percussionist does or the trumpeter does, but not both.
# (S > P) XOR (S > T)
cond1 = pos['S'] > pos['P']
cond2 = pos['S'] > pos['T']
solver.add(Xor(cond1, cond2))

# Question condition: If the percussionist performs a solo at some time before the saxophonist does
condition = pos['P'] < pos['S']

# Options
options = {
    "A": pos['P'] == 1,
    "B": pos['P'] == 2,
    "C": pos['V'] < pos['S'],
    "D": pos['P'] < pos['T'],
    "E": pos['S'] < pos['K']
}

# Test each option: Must be true means (Condition -> Option) is a tautology
# Which is equivalent to: (Condition AND Not Option) is unsatisfiable
found_options = []
for letter, opt_constr in options.items():
    solver.push()
    solver.add(condition)
    solver.add(Not(opt_constr))
    if solver.check() == unsat:
        found_options.append(letter)
    solver.pop()

print(f"Valid options: {found_options}")