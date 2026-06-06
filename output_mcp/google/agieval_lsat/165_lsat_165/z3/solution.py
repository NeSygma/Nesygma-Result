from z3 import *

# Accomplices
names = ['P', 'Q', 'R', 'S', 'T', 'V', 'W']
pos = {name: Int(name) for name in names}

solver = Solver()

# 1. Positions are 1 to 7
for name in names:
    solver.add(pos[name] >= 1, pos[name] <= 7)

# 2. All distinct
solver.add(Distinct([pos[name] for name in names]))

# 3. Constraints
solver.add(pos['P'] == 4)
solver.add(pos['W'] == pos['V'] + 1)
solver.add(pos['Q'] < pos['R'])
solver.add(Abs(pos['S'] - pos['T']) != 1)

# 4. Question condition: Q is immediately before R
solver.add(pos['R'] == pos['Q'] + 1)

# Test each option for Stanton's position
options = {
    "A": 1,
    "B": 2,
    "C": 3,
    "D": 5,
    "E": 7
}

found_options = []
for label, p in options.items():
    solver.push()
    solver.add(pos['S'] == p)
    if solver.check() == sat:
        # This position is possible for Stanton
        pass
    else:
        # This position is impossible for Stanton
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