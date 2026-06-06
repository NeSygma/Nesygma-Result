from z3 import *

# Create solver
solver = Solver()

# Slot variables: slot[i] is the band in slot i (0-indexed: slot 1 is index 0, slot 6 is index 5)
# Bands: Uneasy, Vegemite, Wellspring, Xpert, Yardsign, Zircon
# We'll represent each band as an Int, and assign slot[i] = band

# Helper: enforce that band a is in an earlier slot than band b
def earlier(a, b):
    # Find the slot indices for a and b
    slot_a = [slot[i] for i in range(6) if slot[i] == a][0]
    slot_b = [slot[i] for i in range(6) if slot[i] == b][0]
    solver.add(slot_a < slot_b)

# Slot variables: slot[i] is the band in slot i (0 to 5)
slot = [Int(f'slot_{i}') for i in range(6)]

# Each slot has a unique band (0 to 5 represent the bands)
# Bands: Uneasy=0, Vegemite=1, Wellspring=2, Xpert=3, Yardsign=4, Zircon=5
solver.add(Distinct(slot))

# Vegemite performs in an earlier slot than Zircon
earlier(1, 5)

# Wellspring and Zircon each perform in an earlier slot than Xpert
earlier(2, 3)
earlier(5, 3)

# Uneasy performs in one of the last three slots (slots 4,5,6 -> indices 3,4,5)
solver.add(Or([slot[i] == 0 for i in range(3, 6)]))

# Yardsign performs in one of the first three slots (slots 1,2,3 -> indices 0,1,2)
solver.add(Or([slot[i] == 4 for i in range(0, 3)]))

# Now test each option for slot five (index 4)
found_options = []

# Option A: Uneasy in slot five (index 4)
solver.push()
solver.add(slot[4] == 0)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: Vegemite in slot five (index 4)
solver.push()
solver.add(slot[4] == 1)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: Wellspring in slot five (index 4)
solver.push()
solver.add(slot[4] == 2)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: Xpert in slot five (index 4)
solver.push()
solver.add(slot[4] == 3)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: Zircon in slot five (index 4)
solver.push()
solver.add(slot[4] == 5)
if solver.check() == sat:
    found_options.append("E")
solver.pop()

# Output result
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")