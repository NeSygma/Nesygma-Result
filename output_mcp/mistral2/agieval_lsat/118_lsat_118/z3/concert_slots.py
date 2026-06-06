from z3 import *

solver = Solver()

# Declare symbolic variables for the slots (1 to 6)
slots = [Int(f'slot_{i}') for i in range(1, 7)]

# Each slot must be assigned a unique band
bands = ['Uneasy', 'Vegemite', 'Wellspring', 'Xpert', 'Yardsign', 'Zircon']
band_vars = {band: Int(band) for band in bands}

# Add constraints for unique assignments
solver.add(Distinct(list(band_vars.values())))

# Each slot must be assigned exactly one band
for slot in slots:
    solver.add(Or([band_vars[band] == slot for band in bands]))

# Each band must be assigned to exactly one slot
for band in bands:
    solver.add(Or([band_vars[band] == slot for slot in slots]))

# Constraints from the problem statement
# 1. Vegemite performs in an earlier slot than Zircon
solver.add(band_vars['Vegemite'] < band_vars['Zircon'])

# 2. Wellspring and Zircon each perform in an earlier slot than Xpert
solver.add(band_vars['Wellspring'] < band_vars['Xpert'])
solver.add(band_vars['Zircon'] < band_vars['Xpert'])

# 3. Uneasy performs in one of the last three slots
solver.add(Or([band_vars['Uneasy'] == slots[i] for i in range(3, 6)]))

# 4. Yardsign performs in one of the first three slots
solver.add(Or([band_vars['Yardsign'] == slots[i] for i in range(0, 3)]))

# Additional constraint: Vegemite performs in slot three
solver.add(band_vars['Vegemite'] == 3)

# Now evaluate the multiple choice options
found_options = []

# Option A: Uneasy performs in an earlier slot than Xpert
solver.push()
solver.add(band_vars['Uneasy'] < band_vars['Xpert'])
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: Wellspring performs in an earlier slot than Zircon
solver.push()
solver.add(band_vars['Wellspring'] < band_vars['Zircon'])
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: Xpert performs in an earlier slot than Uneasy
solver.push()
solver.add(band_vars['Xpert'] < band_vars['Uneasy'])
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: Yardsign performs in an earlier slot than Wellspring
solver.push()
solver.add(band_vars['Yardsign'] < band_vars['Wellspring'])
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: Zircon performs in an earlier slot than Uneasy
solver.push()
solver.add(band_vars['Zircon'] < band_vars['Uneasy'])
if solver.check() == sat:
    found_options.append("E")
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