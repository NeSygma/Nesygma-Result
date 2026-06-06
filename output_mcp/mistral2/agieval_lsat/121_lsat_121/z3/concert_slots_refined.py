from z3 import *

solver = Solver()

# Declare symbolic variables for the slots (1 to 6)
slots = [Int(f"slot_{i}") for i in range(1, 7)]

# Each slot must be assigned to exactly one band (1-6)
solver.add(Distinct(slots))

# Assign each band to a slot (1-6)
# We will use a permutation of the slots to represent the order of bands
bands = ["Uneasy", "Vegemite", "Wellspring", "Xpert", "Yardsign", "Zircon"]
band_order = [Int(f"band_{band}") for band in bands]

# Each band must be assigned to exactly one slot
solver.add(Distinct(band_order))
for i in range(6):
    solver.add(And(band_order[i] >= 1, band_order[i] <= 6))

# Constraints from the problem statement
# 1. Vegemite performs in an earlier slot than Zircon
solver.add(band_order[bands.index("Vegemite")] < band_order[bands.index("Zircon")])

# 2. Wellspring and Zircon each perform in an earlier slot than Xpert
solver.add(band_order[bands.index("Wellspring")] < band_order[bands.index("Xpert")])
solver.add(band_order[bands.index("Zircon")] < band_order[bands.index("Xpert")])

# 3. Uneasy performs in one of the last three slots
solver.add(Or([
    band_order[bands.index("Uneasy")] == 4,
    band_order[bands.index("Uneasy")] == 5,
    band_order[bands.index("Uneasy")] == 6
]))

# 4. Yardsign performs in one of the first three slots
solver.add(Or([
    band_order[bands.index("Yardsign")] == 1,
    band_order[bands.index("Yardsign")] == 2,
    band_order[bands.index("Yardsign")] == 3
]))

# Additional constraint: Wellspring performs immediately before Xpert
solver.add(band_order[bands.index("Xpert")] == band_order[bands.index("Wellspring")] + 1)

# Now evaluate the multiple choice options
found_options = []

# Option A: Uneasy performs in slot five
solver.push()
solver.add(band_order[bands.index("Uneasy")] == 5)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: Vegemite performs in slot three
solver.push()
solver.add(band_order[bands.index("Vegemite")] == 3)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: Wellspring performs in slot three
solver.push()
solver.add(band_order[bands.index("Wellspring")] == 3)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: Zircon performs in slot two
solver.push()
solver.add(band_order[bands.index("Zircon")] == 2)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: Zircon performs in slot four
solver.push()
solver.add(band_order[bands.index("Zircon")] == 4)
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