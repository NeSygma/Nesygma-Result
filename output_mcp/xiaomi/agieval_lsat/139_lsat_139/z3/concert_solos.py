from z3 import *

solver = Solver()

# Define the six members and their position variables (1-6)
members = ['G', 'K', 'P', 'S', 'T', 'V']
pos = {m: Int(f'pos_{m}') for m in members}

# Each member performs exactly one solo, positions 1-6, all distinct
for m in members:
    solver.add(pos[m] >= 1, pos[m] <= 6)
solver.add(Distinct([pos[m] for m in members]))

# Constraint 1: The guitarist does not perform the fourth solo.
solver.add(pos['G'] != 4)

# Constraint 2: The percussionist performs a solo at some time before the keyboard player does.
solver.add(pos['P'] < pos['K'])

# Constraint 3: The keyboard player performs a solo at some time after the violinist does
# and at some time before the guitarist does.
solver.add(pos['V'] < pos['K'])
solver.add(pos['K'] < pos['G'])

# Constraint 4: The saxophonist performs a solo at some time after either the percussionist does
# or the trumpeter does, but not both.
# "after either P or T but not both" means:
# (S > P XOR S > T) which is (S > P and S <= T) or (S <= P and S > T)
solver.add(Or(
    And(pos['S'] > pos['P'], pos['S'] <= pos['T']),
    And(pos['S'] <= pos['P'], pos['S'] > pos['T'])
))

# Define each option as a constraint on the ordering
# Option A: violinist, percussionist, saxophonist, guitarist, trumpeter, keyboard player
opt_a_constr = And(
    pos['V'] == 1, pos['P'] == 2, pos['S'] == 3,
    pos['G'] == 4, pos['T'] == 5, pos['K'] == 6
)

# Option B: percussionist, violinist, keyboard player, trumpeter, saxophonist, guitarist
opt_b_constr = And(
    pos['P'] == 1, pos['V'] == 2, pos['K'] == 3,
    pos['T'] == 4, pos['S'] == 5, pos['G'] == 6
)

# Option C: violinist, trumpeter, saxophonist, percussionist, keyboard player, guitarist
opt_c_constr = And(
    pos['V'] == 1, pos['T'] == 2, pos['S'] == 3,
    pos['P'] == 4, pos['K'] == 5, pos['G'] == 6
)

# Option D: keyboard player, trumpeter, violinist, saxophonist, guitarist, percussionist
opt_d_constr = And(
    pos['K'] == 1, pos['T'] == 2, pos['V'] == 3,
    pos['S'] == 4, pos['G'] == 5, pos['P'] == 6
)

# Option E: guitarist, violinist, keyboard player, percussionist, saxophonist, trumpeter
opt_e_constr = And(
    pos['G'] == 1, pos['V'] == 2, pos['K'] == 3,
    pos['P'] == 4, pos['S'] == 5, pos['T'] == 6
)

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