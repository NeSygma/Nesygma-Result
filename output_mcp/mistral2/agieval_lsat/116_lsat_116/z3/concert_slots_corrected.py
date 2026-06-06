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

# 1. Vegemite performs in an earlier slot than Zircon
# Find the positions of Vegemite and Zircon
vegemite_pos = Int('vegemite_pos')
zircon_pos = Int('zircon_pos')
solver.add(Or(
    And(slot1 == VEGEMITE, vegemite_pos == 1),
    And(slot2 == VEGEMITE, vegemite_pos == 2),
    And(slot3 == VEGEMITE, vegemite_pos == 3),
    And(slot4 == VEGEMITE, vegemite_pos == 4),
    And(slot5 == VEGEMITE, vegemite_pos == 5),
    And(slot6 == VEGEMITE, vegemite_pos == 6)
))
solver.add(Or(
    And(slot1 == ZIRCON, zircon_pos == 1),
    And(slot2 == ZIRCON, zircon_pos == 2),
    And(slot3 == ZIRCON, zircon_pos == 3),
    And(slot4 == ZIRCON, zircon_pos == 4),
    And(slot5 == ZIRCON, zircon_pos == 5),
    And(slot6 == ZIRCON, zircon_pos == 6)
))
solver.add(vegemite_pos < zircon_pos)

# 2. Wellspring and Zircon each perform in an earlier slot than Xpert
wellspring_pos = Int('wellspring_pos')
xpert_pos = Int('xpert_pos')
solver.add(Or(
    And(slot1 == WELLSPRING, wellspring_pos == 1),
    And(slot2 == WELLSPRING, wellspring_pos == 2),
    And(slot3 == WELLSPRING, wellspring_pos == 3),
    And(slot4 == WELLSPRING, wellspring_pos == 4),
    And(slot5 == WELLSPRING, wellspring_pos == 5),
    And(slot6 == WELLSPRING, wellspring_pos == 6)
))
solver.add(Or(
    And(slot1 == XPERT, xpert_pos == 1),
    And(slot2 == XPERT, xpert_pos == 2),
    And(slot3 == XPERT, xpert_pos == 3),
    And(slot4 == XPERT, xpert_pos == 4),
    And(slot5 == XPERT, xpert_pos == 5),
    And(slot6 == XPERT, xpert_pos == 6)
))
solver.add(wellspring_pos < xpert_pos)

# Zircon earlier than Xpert
solver.add(Or(
    And(slot1 == ZIRCON, zircon_pos == 1),
    And(slot2 == ZIRCON, zircon_pos == 2),
    And(slot3 == ZIRCON, zircon_pos == 3),
    And(slot4 == ZIRCON, zircon_pos == 4),
    And(slot5 == ZIRCON, zircon_pos == 5),
    And(slot6 == ZIRCON, zircon_pos == 6)
))
solver.add(zircon_pos < xpert_pos)

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