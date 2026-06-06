from z3 import *

# Create solver
solver = Solver()

# Declare variables for each band's slot
Uneasy = Int('Uneasy')
Vegemite = Int('Vegemite')
Wellspring = Int('Wellspring')
Xpert = Int('Xpert')
Yardsign = Int('Yardsign')
Zircon = Int('Zircon')

# All slots are between 1 and 6
solver.add(Uneasy >= 1, Uneasy <= 6)
solver.add(Vegemite >= 1, Vegemite <= 6)
solver.add(Wellspring >= 1, Wellspring <= 6)
solver.add(Xpert >= 1, Xpert <= 6)
solver.add(Yardsign >= 1, Yardsign <= 6)
solver.add(Zircon >= 1, Zircon <= 6)

# All bands have distinct slots
solver.add(Distinct([Uneasy, Vegemite, Wellspring, Xpert, Yardsign, Zircon]))

# Base constraints from problem
# 1. Vegemite performs in an earlier slot than Zircon
solver.add(Vegemite < Zircon)

# 2. Wellspring and Zircon each perform in an earlier slot than Xpert
solver.add(Wellspring < Xpert)
solver.add(Zircon < Xpert)

# 3. Uneasy performs in one of the last three slots (4,5,6)
solver.add(Or([Uneasy == 4, Uneasy == 5, Uneasy == 6]))

# 4. Yardsign performs in one of the first three slots (1,2,3)
solver.add(Or([Yardsign == 1, Yardsign == 2, Yardsign == 3]))

# Additional constraint from question: Zircon performs in an earlier slot than Yardsign
solver.add(Zircon < Yardsign)

# Now find the minimum possible slot for Wellspring
# We'll check each possible slot from 1 to 6 in order
min_wellspring = None
for slot in range(1, 7):
    solver.push()
    solver.add(Wellspring == slot)
    if solver.check() == sat:
        min_wellspring = slot
        solver.pop()
        break
    solver.pop()

if min_wellspring is not None:
    # Now check which option matches this minimum
    # Options: (A)two (B)three (C)four (D)five (E)six
    option_map = {2: "A", 3: "B", 4: "C", 5: "D", 6: "E"}
    
    if min_wellspring in option_map:
        print("STATUS: sat")
        print(f"answer:{option_map[min_wellspring]}")
    else:
        print("STATUS: unsat")
        print(f"Refine: Minimum slot {min_wellspring} not in options")
else:
    print("STATUS: unsat")
    print("Refine: No valid slot found for Wellspring")