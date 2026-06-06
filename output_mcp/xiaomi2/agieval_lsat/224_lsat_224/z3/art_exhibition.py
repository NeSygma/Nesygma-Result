from z3 import *

solver = Solver()

# Paintings: FO, FW, GO, GW, HO, HW, IO, IW
# For each painting: wall (1-4) and position (0=lower, 1=upper)
paintings = ['FO', 'FW', 'GO', 'GW', 'HO', 'HW', 'IO', 'IW']

wall = {p: Int(f'wall_{p}') for p in paintings}
pos = {p: Int(f'pos_{p}') for p in paintings}

# Domain constraints
for p in paintings:
    solver.add(And(wall[p] >= 1, wall[p] <= 4))
    solver.add(Or(pos[p] == 0, pos[p] == 1))

# All 8 (wall, pos) pairs must be distinct (bijection to 8 slots)
all_pairs = [(wall[p], pos[p]) for p in paintings]
for i in range(len(paintings)):
    for j in range(i+1, len(paintings)):
        solver.add(Or(
            wall[paintings[i]] != wall[paintings[j]],
            pos[paintings[i]] != pos[paintings[j]]
        ))

# Constraint 1: No wall has only watercolors. Each wall has at least one oil.
oils = ['FO', 'GO', 'HO', 'IO']
for w in range(1, 5):
    solver.add(Or([wall[o] == w for o in oils]))

# Constraint 2: No wall has work of only one student.
# Same-student pairs must be on different walls.
solver.add(wall['FO'] != wall['FW'])
solver.add(wall['GO'] != wall['GW'])
solver.add(wall['HO'] != wall['HW'])
solver.add(wall['IO'] != wall['IW'])

# Constraint 3: No wall has both Franz and Isaacs.
franz = ['FO', 'FW']
isaacs = ['IO', 'IW']
for f in franz:
    for i in isaacs:
        solver.add(wall[f] != wall[i])

# Constraint 4: Greene's watercolor is upper on the wall where Franz's oil is.
solver.add(wall['GW'] == wall['FO'])
solver.add(pos['GW'] == 1)
solver.add(pos['FO'] == 0)

# Constraint 5: Isaacs's oil is lower on wall 4.
solver.add(wall['IO'] == 4)
solver.add(pos['IO'] == 0)

# Define answer choice constraints
opt_a = And(pos['FO'] == 0, pos['FW'] == 0, pos['GO'] == 0, pos['GW'] == 0)
opt_b = And(pos['FO'] == 1, pos['FW'] == 1, pos['GO'] == 1, pos['GW'] == 1)
opt_c = And(pos['FO'] == 1, pos['FW'] == 1, pos['HO'] == 1, pos['HW'] == 1)
opt_d = And(pos['GO'] == 0, pos['GW'] == 0, pos['HO'] == 0, pos['HW'] == 0)
opt_e = And(pos['GO'] == 1, pos['GW'] == 1, pos['HO'] == 1, pos['HW'] == 1)

found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(constr)
    result = solver.check()
    if result == sat:
        found_options.append(letter)
        m = solver.model()
        print(f"Option {letter} is SAT:")
        for p in paintings:
            print(f"  {p}: wall={m[wall[p]]}, pos={'upper' if m[pos[p]]==1 else 'lower'}")
    else:
        print(f"Option {letter} is {result}")
    solver.pop()

print()
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")