from z3 import *

solver = Solver()

# Position variables for each article (1-7)
pos = {}
for a in ['G', 'H', 'J', 'Q', 'R', 'S', 'Y']:
    pos[a] = Int(f'pos_{a}')

# All positions are distinct and in range 1-7
articles = ['G', 'H', 'J', 'Q', 'R', 'S', 'Y']
for a in articles:
    solver.add(pos[a] >= 1, pos[a] <= 7)
solver.add(Distinct([pos[a] for a in articles]))

# Topic groups
finance = ['G', 'H', 'J']
nutrition = ['Q', 'R', 'S']
# wildlife = ['Y']  (only one, no consecutive issue)

# Constraint 1: Consecutive articles cannot cover the same topic
# No two finance articles can be adjacent
for i in range(len(finance)):
    for j in range(i+1, len(finance)):
        a, b = finance[i], finance[j]
        solver.add(Abs(pos[a] - pos[b]) != 1)

# No two nutrition articles can be adjacent
for i in range(len(nutrition)):
    for j in range(i+1, len(nutrition)):
        a, b = nutrition[i], nutrition[j]
        solver.add(Abs(pos[a] - pos[b]) != 1)

# Constraint 2: S can be earlier than Q only if Q is third
# If S < Q, then Q == 3
solver.add(Implies(pos['S'] < pos['Q'], pos['Q'] == 3))

# Constraint 3: S must be earlier than Y
solver.add(pos['S'] < pos['Y'])

# Constraint 4: J < G < R
solver.add(pos['J'] < pos['G'])
solver.add(pos['G'] < pos['R'])

# Test each option
found_options = []

# (A) G is second
solver.push()
solver.add(pos['G'] == 2)
if solver.check() == sat:
    found_options.append('A')
solver.pop()

# (B) H is second
solver.push()
solver.add(pos['H'] == 2)
if solver.check() == sat:
    found_options.append('B')
solver.pop()

# (C) S is second
solver.push()
solver.add(pos['S'] == 2)
if solver.check() == sat:
    found_options.append('C')
solver.pop()

# (D) R is third
solver.push()
solver.add(pos['R'] == 3)
if solver.check() == sat:
    found_options.append('D')
solver.pop()

# (E) Y is third
solver.push()
solver.add(pos['Y'] == 3)
if solver.check() == sat:
    found_options.append('E')
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