from z3 import *

solver = Solver()

# Declare symbolic variables for the slots (1 to 6)
# Each band is assigned to a unique slot
Uneasy = Int('Uneasy')
Vegemite = Int('Vegemite')
Wellspring = Int('Wellspring')
Xpert = Int('Xpert')
Yardsign = Int('Yardsign')
Zircon = Int('Zircon')

# Each band is assigned to a unique slot from 1 to 6
solver.add(Distinct([Uneasy, Vegemite, Wellspring, Xpert, Yardsign, Zircon]))
solver.add(Uneasy >= 1, Uneasy <= 6)
solver.add(Vegemite >= 1, Vegemite <= 6)
solver.add(Wellspring >= 1, Wellspring <= 6)
solver.add(Xpert >= 1, Xpert <= 6)
solver.add(Yardsign >= 1, Yardsign <= 6)
solver.add(Zircon >= 1, Zircon <= 6)

# Constraints from the problem statement
# 1. Vegemite performs in an earlier slot than Zircon
solver.add(Vegemite < Zircon)

# 2. Wellspring and Zircon each perform in an earlier slot than Xpert
solver.add(Wellspring < Xpert)
solver.add(Zircon < Xpert)

# 3. Uneasy performs in one of the last three slots (4, 5, or 6)
solver.add(Or(Uneasy == 4, Uneasy == 5, Uneasy == 6))

# 4. Yardsign performs in one of the first three slots (1, 2, or 3)
solver.add(Or(Yardsign == 1, Yardsign == 2, Yardsign == 3))

# Additional constraint: Zircon performs immediately before Wellspring
# This means Wellspring = Zircon + 1 and no other band is between them
solver.add(Wellspring == Zircon + 1)

# Now, evaluate each option to see which one must be true
found_options = []

# Option A: Uneasy performs in slot five
solver.push()
solver.add(Uneasy == 5)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: Vegemite performs in slot one
solver.push()
solver.add(Vegemite == 1)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: Xpert performs in slot five
solver.push()
solver.add(Xpert == 5)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: Yardsign performs in slot two
solver.push()
solver.add(Yardsign == 2)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: Zircon performs in slot three
solver.push()
solver.add(Zircon == 3)
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