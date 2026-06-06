from z3 import *

# Bands
bands = ['U', 'V', 'W', 'X', 'Y', 'Z']
# Slots 1-6
# pos[band] = slot number
pos = {b: Int(b) for b in bands}

solver = Solver()

# Each band in one slot 1-6
for b in bands:
    solver.add(pos[b] >= 1, pos[b] <= 6)

# Each band in a unique slot
solver.add(Distinct([pos[b] for b in bands]))

# Constraints
solver.add(pos['V'] < pos['Z'])
solver.add(pos['W'] < pos['X'])
solver.add(pos['Z'] < pos['X'])
solver.add(pos['U'] >= 4)
solver.add(pos['Y'] <= 3)

# Given condition
solver.add(pos['V'] == 3)

# Options
options = {
    "A": pos['U'] < pos['X'],
    "B": pos['W'] < pos['Z'],
    "C": pos['X'] < pos['U'],
    "D": pos['Y'] < pos['W'],
    "E": pos['Z'] < pos['U']
}

found_options = []
for letter, constr in options.items():
    solver.push()
    # We want to check if the option MUST be true.
    # This is equivalent to checking if the negation is unsatisfiable.
    solver.add(Not(constr))
    if solver.check() == unsat:
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