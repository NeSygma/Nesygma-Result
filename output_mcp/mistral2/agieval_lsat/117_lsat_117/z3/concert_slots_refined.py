from z3 import *

solver = Solver()

# Declare variables for each band's slot
uneasy = Int('uneasy')
vegemite = Int('vegemite')
wellspring = Int('wellspring')
xpert = Int('xpert')
yardsign = Int('yardsign')
zircon = Int('zircon')

# All slots are between 1 and 6
solver.add(uneasy >= 1, uneasy <= 6)
solver.add(vegemite >= 1, vegemite <= 6)
solver.add(wellspring >= 1, wellspring <= 6)
solver.add(xpert >= 1, xpert <= 6)
solver.add(yardsign >= 1, yardsign <= 6)
solver.add(zircon >= 1, zircon <= 6)

# All slots are distinct
solver.add(Distinct(uneasy, vegemite, wellspring, xpert, yardsign, zircon))

# Constraints
solver.add(vegemite < zircon)
solver.add(And(wellspring < xpert, zircon < xpert))
solver.add(uneasy >= 4)
solver.add(yardsign <= 3)
solver.add(zircon < yardsign)

# Answer choices: Wellspring in slot 2, 3, 4, 5, or 6
found_options = []
for letter, slot in [("A", 2), ("B", 3), ("C", 4), ("D", 5), ("E", 6)]:
    solver.push()
    solver.add(wellspring == slot)
    if solver.check() == sat:
        found_options.append(letter)
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