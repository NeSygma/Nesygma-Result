from z3 import *

# Bands
bands = ['U', 'V', 'W', 'X', 'Y', 'Z']
# Slots 1-6
# pos[band] = slot number
pos = {b: Int(f'pos_{b}') for b in bands}

solver = Solver()

# Each band in exactly one slot 1-6
for b in bands:
    solver.add(pos[b] >= 1, pos[b] <= 6)
solver.add(Distinct([pos[b] for b in bands]))

# Constraints
# 1. Vegemite performs in an earlier slot than Zircon.
solver.add(pos['V'] < pos['Z'])
# 2. Wellspring and Zircon each perform in an earlier slot than Xpert.
solver.add(pos['W'] < pos['X'])
solver.add(pos['Z'] < pos['X'])
# 3. Uneasy performs in one of the last three slots.
solver.add(pos['U'] >= 4)
# 4. Yardsign performs in one of the first three slots.
solver.add(pos['Y'] <= 3)

# Test each option: Which one CANNOT be in slot 5?
# We want to find the band for which pos[band] == 5 is UNSAT.
options = [('A', 'U'), ('B', 'V'), ('C', 'W'), ('D', 'X'), ('E', 'Z')]
valid_options = []

for letter, band in options:
    solver.push()
    solver.add(pos[band] == 5)
    if solver.check() == sat:
        # This band CAN be in slot 5
        pass
    else:
        # This band CANNOT be in slot 5
        valid_options.append(letter)
    solver.pop()

if len(valid_options) == 1:
    print("STATUS: sat")
    print(f"answer:{valid_options[0]}")
elif len(valid_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {valid_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")