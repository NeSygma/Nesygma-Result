from z3 import *

solver = Solver()

# Declare symbolic variables for the slots (1 to 6)
slots = [1, 2, 3, 4, 5, 6]

# Bands
bands = ['Uneasy', 'Vegemite', 'Wellspring', 'Xpert', 'Yardsign', 'Zircon']

# Assign each band to a unique slot
band_to_slot = {band: Int(f'{band}_slot') for band in bands}

# Each slot must be assigned exactly one band
for slot in slots:
    solver.add(Or([band_to_slot[band] == slot for band in bands]))
    solver.add(AtMost(*[band_to_slot[band] == slot for band in bands], 1))

# Each band must be assigned to exactly one slot
for band in bands:
    solver.add(Or([band_to_slot[band] == slot for slot in slots]))
    solver.add(AtMost(*[band_to_slot[band] == slot for slot in slots], 1))

# Constraints from the problem statement
# 1. Vegemite performs in an earlier slot than Zircon
solver.add(band_to_slot['Vegemite'] < band_to_slot['Zircon'])

# 2. Wellspring and Zircon each perform in an earlier slot than Xpert
solver.add(band_to_slot['Wellspring'] < band_to_slot['Xpert'])
solver.add(band_to_slot['Zircon'] < band_to_slot['Xpert'])

# 3. Uneasy performs in one of the last three slots
solver.add(Or([band_to_slot['Uneasy'] == slot for slot in [4, 5, 6]]))

# 4. Yardsign performs in one of the first three slots
solver.add(Or([band_to_slot['Yardsign'] == slot for slot in [1, 2, 3]]))

# Additional constraint: Vegemite performs in slot three
solver.add(band_to_slot['Vegemite'] == 3)

# Additional constraints to refine the model:
# Xpert must be after Wellspring and Zircon, and after Vegemite (slot 3)
# So Xpert must be in slot 4, 5, or 6
solver.add(band_to_slot['Xpert'] > 3)

# Uneasy must be in one of the last three slots (4, 5, 6)
# If Xpert is in slot 4, Uneasy must be in 5 or 6
# If Xpert is in slot 5, Uneasy must be in 4 or 6
# If Xpert is in slot 6, Uneasy must be in 4 or 5

# Yardsign must be in one of the first three slots (1, 2, 3)
# Since Vegemite is in slot 3, Yardsign must be in 1 or 2
solver.add(Or([band_to_slot['Yardsign'] == slot for slot in [1, 2]]))

# Wellspring must be earlier than Xpert and Zircon
# Since Vegemite is in slot 3, Wellspring must be in 1 or 2
solver.add(Or([band_to_slot['Wellspring'] == slot for slot in [1, 2]]))

# Zircon must be after Vegemite (slot 3) and before Xpert
# So Zircon must be in slot 4 or 5
solver.add(band_to_slot['Zircon'] > 3)
solver.add(band_to_slot['Zircon'] < band_to_slot['Xpert'])

# Now evaluate the multiple choice options
found_options = []

# Option A: Uneasy performs in an earlier slot than Xpert
solver.push()
solver.add(band_to_slot['Uneasy'] < band_to_slot['Xpert'])
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: Wellspring performs in an earlier slot than Zircon
solver.push()
solver.add(band_to_slot['Wellspring'] < band_to_slot['Zircon'])
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: Xpert performs in an earlier slot than Uneasy
solver.push()
solver.add(band_to_slot['Xpert'] < band_to_slot['Uneasy'])
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: Yardsign performs in an earlier slot than Wellspring
solver.push()
solver.add(band_to_slot['Yardsign'] < band_to_slot['Wellspring'])
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: Zircon performs in an earlier slot than Uneasy
solver.push()
solver.add(band_to_slot['Zircon'] < band_to_slot['Uneasy'])
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