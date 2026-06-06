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

# We are looking for the earliest slot in which Wellspring could perform
# So we test slots in ascending order and stop at the first valid one
found_options = []
for slot in range(1, 7):
    solver.push()
    solver.add(wellspring == slot)
    if solver.check() == sat:
        found_options.append(str(slot))
        solver.pop()
        break  # Stop at the earliest valid slot
    solver.pop()

# Map the slot number to the answer choice
slot_to_choice = {2: "A", 3: "B", 4: "C", 5: "D", 6: "E"}
answer_letter = slot_to_choice.get(int(found_options[0]), "unknown") if found_options else None

if answer_letter:
    print("STATUS: sat")
    print(f"answer:{answer_letter}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")