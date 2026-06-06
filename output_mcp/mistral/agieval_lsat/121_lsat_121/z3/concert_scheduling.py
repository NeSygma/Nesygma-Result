from z3 import *

# BENCHMARK_MODE: ON (model-finding mode)
BENCHMARK_MODE = True

# Declare symbolic variables for each band's slot
Uneasy = Int('Uneasy')
Vegemite = Int('Vegemite')
Wellspring = Int('Wellspring')
Xpert = Int('Xpert')
Yardsign = Int('Yardsign')
Zircon = Int('Zircon')

# Slots are 1 through 6
solver = Solver()

# Each band performs in exactly one slot (1-6)
solver.add(Uneasy >= 1, Uneasy <= 6)
solver.add(Vegemite >= 1, Vegemite <= 6)
solver.add(Wellspring >= 1, Wellspring <= 6)
solver.add(Xpert >= 1, Xpert <= 6)
solver.add(Yardsign >= 1, Yardsign <= 6)
solver.add(Zircon >= 1, Zircon <= 6)

# All bands perform in distinct slots
solver.add(Distinct(Uneasy, Vegemite, Wellspring, Xpert, Yardsign, Zircon))

# Vegemite performs in an earlier slot than Zircon
solver.add(Vegemite < Zircon)

# Wellspring and Zircon each perform in an earlier slot than Xpert
solver.add(Wellspring < Xpert)
solver.add(Zircon < Xpert)

# Uneasy performs in one of the last three slots
solver.add(Uneasy >= 4)

# Yardsign performs in one of the first three slots
solver.add(Yardsign <= 3)

# Wellspring performs immediately before Xpert
solver.add(Xpert == Wellspring + 1)

# Evaluate each option
found_options = []

# Option A: Uneasy performs in slot five
solver.push()
solver.add(Uneasy == 5)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: Vegemite performs in slot three
solver.push()
solver.add(Vegemite == 3)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: Wellspring performs in slot three
solver.push()
solver.add(Wellspring == 3)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: Zircon performs in slot two
solver.push()
solver.add(Zircon == 2)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: Zircon performs in slot four
solver.push()
solver.add(Zircon == 4)
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