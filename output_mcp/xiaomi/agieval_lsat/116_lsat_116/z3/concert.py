from z3 import *

solver = Solver()

# Bands: Uneasy=0, Vegemite=1, Wellspring=2, Xpert=3, Yardsign=4, Zircon=5
# Variables: slot[b] = the slot number (1-6) assigned to band b
slot = [Int(f'slot_{b}') for b in range(6)]

# Each band assigned to exactly one slot from 1 to 6
for b in range(6):
    solver.add(slot[b] >= 1, slot[b] <= 6)

# All bands in distinct slots
solver.add(Distinct(slot))

# Constraint 1: Vegemite performs in an earlier slot than Zircon
solver.add(slot[1] < slot[5])

# Constraint 2: Wellspring and Zircon each perform in an earlier slot than Xpert
solver.add(slot[2] < slot[3])
solver.add(slot[5] < slot[3])

# Constraint 3: Uneasy performs in one of the last three slots (4, 5, or 6)
solver.add(Or(slot[0] == 4, slot[0] == 5, slot[0] == 6))

# Constraint 4: Yardsign performs in one of the first three slots (1, 2, or 3)
solver.add(Or(slot[4] == 1, slot[4] == 2, slot[4] == 3))

# Now test each option: which band CANNOT be in slot 5?
# We test if each band CAN be in slot 5. The one that CANNOT is the answer.

found_options = []

# (A) Uneasy in slot 5
solver.push()
solver.add(slot[0] == 5)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# (B) Vegemite in slot 5
solver.push()
solver.add(slot[1] == 5)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# (C) Wellspring in slot 5
solver.push()
solver.add(slot[2] == 5)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# (D) Xpert in slot 5
solver.push()
solver.add(slot[3] == 5)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# (E) Zircon in slot 5
solver.push()
solver.add(slot[5] == 5)
if solver.check() == sat:
    found_options.append("E")
solver.pop()

# The question asks which CANNOT be in slot 5.
# So we want the option that is NOT in found_options.
all_options = ["A", "B", "C", "D", "E"]
cannot_options = [o for o in all_options if o not in found_options]

if len(cannot_options) == 1:
    print("STATUS: sat")
    print(f"answer:{cannot_options[0]}")
elif len(cannot_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options cannot be in slot 5: {cannot_options}")
else:
    print("STATUS: unsat")
    print("Refine: All options can be in slot 5")

# Print details
print(f"\nBands that CAN be in slot 5: {found_options}")
print(f"Bands that CANNOT be in slot 5: {cannot_options}")