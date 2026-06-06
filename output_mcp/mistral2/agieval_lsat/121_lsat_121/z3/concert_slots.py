from z3 import *

solver = Solver()

# Declare symbolic variables for the slots (1 to 6)
slots = [Int(f"slot_{i}") for i in range(1, 7)]

# Each slot must be assigned to exactly one band (1-6)
solver.add(Distinct(slots))

# Assign each band to a slot (1-6)
# We will use the band names as keys and their slot assignments as values
band_to_slot = {
    "Uneasy": Int("Uneasy"),
    "Vegemite": Int("Vegemite"),
    "Wellspring": Int("Wellspring"),
    "Xpert": Int("Xpert"),
    "Yardsign": Int("Yardsign"),
    "Zircon": Int("Zircon"),
}

# Each band must be assigned to exactly one slot
for band in band_to_slot:
    solver.add(Or([band_to_slot[band] == s for s in slots]))

# Constraints from the problem statement
# 1. Vegemite performs in an earlier slot than Zircon
solver.add(band_to_slot["Vegemite"] < band_to_slot["Zircon"])

# 2. Wellspring and Zircon each perform in an earlier slot than Xpert
solver.add(band_to_slot["Wellspring"] < band_to_slot["Xpert"])
solver.add(band_to_slot["Zircon"] < band_to_slot["Xpert"])

# 3. Uneasy performs in one of the last three slots
solver.add(Or([
    band_to_slot["Uneasy"] == 4,
    band_to_slot["Uneasy"] == 5,
    band_to_slot["Uneasy"] == 6
]))

# 4. Yardsign performs in one of the first three slots
solver.add(Or([
    band_to_slot["Yardsign"] == 1,
    band_to_slot["Yardsign"] == 2,
    band_to_slot["Yardsign"] == 3
]))

# Additional constraint: Wellspring performs immediately before Xpert
solver.add(band_to_slot["Xpert"] == band_to_slot["Wellspring"] + 1)

# Now evaluate the multiple choice options
found_options = []

# Option A: Uneasy performs in slot five
solver.push()
solver.add(band_to_slot["Uneasy"] == 5)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: Vegemite performs in slot three
solver.push()
solver.add(band_to_slot["Vegemite"] == 3)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: Wellspring performs in slot three
solver.push()
solver.add(band_to_slot["Wellspring"] == 3)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: Zircon performs in slot two
solver.push()
solver.add(band_to_slot["Zircon"] == 2)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: Zircon performs in slot four
solver.push()
solver.add(band_to_slot["Zircon"] == 4)
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