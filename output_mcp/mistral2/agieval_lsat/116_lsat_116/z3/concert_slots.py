from z3 import *

solver = Solver()

# Declare symbolic variables for the slots (1 to 6)
# Each variable represents the band assigned to that slot
slot1 = Int('slot1')
slot2 = Int('slot2')
slot3 = Int('slot3')
slot4 = Int('slot4')
slot5 = Int('slot5')
slot6 = Int('slot6')

# Bands are represented as integers for simplicity
# Assign unique integers to each band for clarity
UNEASY = 0
VEGEMITE = 1
WELLSPRING = 2
XPERT = 3
YARDSIGN = 4
ZIRCON = 5

# All bands must be assigned to exactly one slot
bands = [UNEASY, VEGEMITE, WELLSPRING, XPERT, YARDSIGN, ZIRCON]
slots = [slot1, slot2, slot3, slot4, slot5, slot6]

# Each slot must be assigned a unique band
solver.add(Distinct(slots))

# Each slot must be assigned a valid band
for s in slots:
    solver.add(Or(s == UNEASY, s == VEGEMITE, s == WELLSPRING, s == XPERT, s == YARDSIGN, s == ZIRCON))

# Constraints from the problem statement
# 1. Vegemite performs in an earlier slot than Zircon
solver.add(Or(
    And(slot1 == VEGEMITE, Or(slot2 == ZIRCON, slot3 == ZIRCON, slot4 == ZIRCON, slot5 == ZIRCON, slot6 == ZIRCON)),
    And(slot2 == VEGEMITE, Or(slot3 == ZIRCON, slot4 == ZIRCON, slot5 == ZIRCON, slot6 == ZIRCON)),
    And(slot3 == VEGEMITE, Or(slot4 == ZIRCON, slot5 == ZIRCON, slot6 == ZIRCON)),
    And(slot4 == VEGEMITE, Or(slot5 == ZIRCON, slot6 == ZIRCON)),
    And(slot5 == VEGEMITE, slot6 == ZIRCON)
))

# 2. Wellspring and Zircon each perform in an earlier slot than Xpert
solver.add(Or(
    And(slot1 == WELLSPRING, Or(slot2 == XPERT, slot3 == XPERT, slot4 == XPERT, slot5 == XPERT, slot6 == XPERT)),
    And(slot2 == WELLSPRING, Or(slot3 == XPERT, slot4 == XPERT, slot5 == XPERT, slot6 == XPERT)),
    And(slot3 == WELLSPRING, Or(slot4 == XPERT, slot5 == XPERT, slot6 == XPERT)),
    And(slot4 == WELLSPRING, Or(slot5 == XPERT, slot6 == XPERT)),
    And(slot5 == WELLSPRING, slot6 == XPERT)
))

solver.add(Or(
    And(slot1 == ZIRCON, Or(slot2 == XPERT, slot3 == XPERT, slot4 == XPERT, slot5 == XPERT, slot6 == XPERT)),
    And(slot2 == ZIRCON, Or(slot3 == XPERT, slot4 == XPERT, slot5 == XPERT, slot6 == XPERT)),
    And(slot3 == ZIRCON, Or(slot4 == XPERT, slot5 == XPERT, slot6 == XPERT)),
    And(slot4 == ZIRCON, Or(slot5 == XPERT, slot6 == XPERT)),
    And(slot5 == ZIRCON, slot6 == XPERT)
))

# 3. Uneasy performs in one of the last three slots
solver.add(Or(slot4 == UNEASY, slot5 == UNEASY, slot6 == UNEASY))

# 4. Yardsign performs in one of the first three slots
solver.add(Or(slot1 == YARDSIGN, slot2 == YARDSIGN, slot3 == YARDSIGN))

# Now, evaluate each option for slot5
found_options = []

# Option A: slot5 = UNEASY
solver.push()
solver.add(slot5 == UNEASY)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: slot5 = VEGEMITE
solver.push()
solver.add(slot5 == VEGEMITE)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: slot5 = WELLSPRING
solver.push()
solver.add(slot5 == WELLSPRING)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: slot5 = XPERT
solver.push()
solver.add(slot5 == XPERT)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: slot5 = ZIRCON
solver.push()
solver.add(slot5 == ZIRCON)
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