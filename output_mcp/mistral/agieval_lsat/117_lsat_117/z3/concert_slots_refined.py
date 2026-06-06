from z3 import *

# BENCHMARK_MODE: ON (model-finding mode)
BENCHMARK_MODE = True

# Declare symbolic variables for each band's slot (1 to 6)
Uneasy = Int('Uneasy')
Vegemite = Int('Vegemite')
Wellspring = Int('Wellspring')
Xpert = Int('Xpert')
Yardsign = Int('Yardsign')
Zircon = Int('Zircon')

# Slots are 1 to 6
solver = Solver()

# Each band is assigned to a unique slot
solver.add(Distinct([Uneasy, Vegemite, Wellspring, Xpert, Yardsign, Zircon]))
solver.add(Uneasy >= 1, Uneasy <= 6)
solver.add(Vegemite >= 1, Vegemite <= 6)
solver.add(Wellspring >= 1, Wellspring <= 6)
solver.add(Xpert >= 1, Xpert <= 6)
solver.add(Yardsign >= 1, Yardsign <= 6)
solver.add(Zircon >= 1, Zircon <= 6)

# Constraints from the problem
solver.add(Vegemite < Zircon)  # Vegemite performs earlier than Zircon
solver.add(Wellspring < Xpert)  # Wellspring performs earlier than Xpert
solver.add(Zircon < Xpert)      # Zircon performs earlier than Xpert
solver.add(Or(Uneasy == 4, Uneasy == 5, Uneasy == 6))  # Uneasy in last three slots
solver.add(Or(Yardsign == 1, Yardsign == 2, Yardsign == 3))  # Yardsign in first three slots

# Additional condition for this question: Zircon performs earlier than Yardsign
solver.add(Zircon < Yardsign)

# Now, find the earliest slot in which Wellspring could perform
# We will check from slot 1 to slot 6 and return the first valid option
found_options = []

# Check slots in order from earliest to latest
for slot in range(1, 7):
    solver.push()
    solver.add(Wellspring == slot)
    if solver.check() == sat:
        found_options.append(chr(ord('A') + slot - 2))  # A for slot 2, B for slot 3, etc.
        solver.pop()
        break  # Stop at the earliest valid slot
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