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

# Test each option
found_options = []

# Option A: Uneasy in slot 5
opt_a_constr = (slot_Uneasy == 5)
# Option B: Vegemite in slot 5
opt_b_constr = (slot_Vegemite == 5)
# Option C: Wellspring in slot 5
opt_c_constr = (slot_Wellspring == 5)
# Option D: Xpert in slot 5
opt_d_constr = (slot_Xpert == 5)
# Option E: Zircon in slot 5
opt_e_constr = (slot_Zircon == 5)

for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
    solver.push()
    solver.add(constr)
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