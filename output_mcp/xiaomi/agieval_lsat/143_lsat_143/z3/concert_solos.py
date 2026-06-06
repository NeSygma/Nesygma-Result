from z3 import *

solver = Solver()

# Define the six band members and their solo positions (1-6)
members = ['G', 'K', 'P', 'S', 'T', 'V']
# G = guitarist, K = keyboard, P = percussionist, S = saxophonist, T = trumpeter, V = violinist

pos = {m: Int(f'pos_{m}') for m in members}

# Each member performs exactly one solo, positions 1-6, all distinct
for m in members:
    solver.add(pos[m] >= 1, pos[m] <= 6)
solver.add(Distinct([pos[m] for m in members]))

# Given condition: violinist performs the fourth solo
solver.add(pos['V'] == 4)

# Constraint 1: The guitarist does not perform the fourth solo
solver.add(pos['G'] != 4)

# Constraint 2: The percussionist performs a solo at some time before the keyboard player does
solver.add(pos['P'] < pos['K'])

# Constraint 3: The keyboard player performs a solo at some time after the violinist does
#               and at some time before the guitarist does
solver.add(pos['K'] > pos['V'])
solver.add(pos['K'] < pos['G'])

# Constraint 4: The saxophonist performs a solo at some time after either the percussionist
#               does or the trumpeter does, but not both
solver.add(Or(
    And(pos['S'] > pos['P'], Not(pos['S'] > pos['T'])),
    And(pos['S'] > pos['T'], Not(pos['S'] > pos['P']))
))
# More precisely: (S after P XOR S after T)
# "after" means strictly later: S > P or S > T
# "not both" means XOR
solver.add(Xor(pos['S'] > pos['P'], pos['S'] > pos['T']))

# Now evaluate each option
# (A) The percussionist performs a solo at some time before the violinist does.
opt_a = pos['P'] < pos['V']

# (B) The trumpeter performs a solo at some time before the violinist does.
opt_b = pos['T'] < pos['V']

# (C) The trumpeter performs a solo at some time before the guitarist does.
opt_c = pos['T'] < pos['G']

# (D) The saxophonist performs a solo at some time before the violinist does.
opt_d = pos['S'] < pos['V']

# (E) The trumpeter performs a solo at some time before the saxophonist does.
opt_e = pos['T'] < pos['S']

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