from z3 import *

solver = Solver()

# Declare variables
slot_Uneasy = Int('slot_Uneasy')
slot_Vegemite = Int('slot_Vegemite')
slot_Wellspring = Int('slot_Wellspring')
slot_Xpert = Int('slot_Xpert')
slot_Yardsign = Int('slot_Yardsign')
slot_Zircon = Int('slot_Zircon')

# Domain constraints
slots = [slot_Uneasy, slot_Vegemite, slot_Wellspring, slot_Xpert, slot_Yardsign, slot_Zircon]
for s in slots:
    solver.add(s >= 1, s <= 6)

# All different
solver.add(Distinct(slots))

# Constraints
solver.add(slot_Vegemite < slot_Zircon)
solver.add(slot_Wellspring < slot_Xpert)
solver.add(slot_Zircon < slot_Xpert)
solver.add(And(slot_Uneasy >= 4, slot_Uneasy <= 6))
solver.add(And(slot_Yardsign >= 1, slot_Yardsign <= 3))

# Test each option: we want to find which band CANNOT be in slot 5
# So we look for the option that makes the constraints UNSAT
found_impossible = []

for letter, constr in [("A", slot_Uneasy == 5), ("B", slot_Vegemite == 5), 
                       ("C", slot_Wellspring == 5), ("D", slot_Xpert == 5), 
                       ("E", slot_Zircon == 5)]:
    solver.push()
    solver.add(constr)
    if solver.check() == unsat:
        found_impossible.append(letter)
    solver.pop()

if len(found_impossible) == 1:
    print("STATUS: sat")
    print(f"answer:{found_impossible[0]}")
elif len(found_impossible) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple impossible options found {found_impossible}")
else:
    print("STATUS: unsat")
    print("Refine: No impossible options found")