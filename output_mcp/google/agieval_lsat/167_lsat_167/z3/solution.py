from z3 import *

# Accomplices
names = ['P', 'Q', 'R', 'S', 'T', 'V', 'W']
# Positions 1-7
pos = {name: Int(name) for name in names}

solver = Solver()

# 1. Positions are 1-7
for name in names:
    solver.add(pos[name] >= 1, pos[name] <= 7)

# 2. All positions are distinct
solver.add(Distinct([pos[name] for name in names]))

# 3. Constraints
solver.add(pos['P'] == 4)
solver.add(pos['Q'] < pos['R'])
solver.add(pos['W'] == pos['V'] + 1)
solver.add(Not(Or(pos['S'] == pos['T'] + 1, pos['S'] == pos['T'] - 1)))

# Question constraint: W is immediately before Q
solver.add(pos['Q'] == pos['W'] + 1)

# Test each option for "who is sixth"
options = {
    'A': 'Q',
    'B': 'R',
    'C': 'S',
    'D': 'V',
    'E': 'W'
}

found_options = []
for label, name in options.items():
    solver.push()
    solver.add(pos[name] == 6)
    if solver.check() == sat:
        found_options.append(label)
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