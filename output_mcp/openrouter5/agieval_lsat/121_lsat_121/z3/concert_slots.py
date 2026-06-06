from z3 import *

solver = Solver()

# Slots 1-6, each band gets a unique slot
slots = [Int(f'slot_{i}') for i in range(6)]
# bands: 0=Uneasy, 1=Vegemite, 2=Wellspring, 3=Xpert, 4=Yardsign, 5=Zircon
band_names = ['Uneasy', 'Vegemite', 'Wellspring', 'Xpert', 'Yardsign', 'Zircon']

# Each slot is between 1 and 6
for s in slots:
    solver.add(s >= 1, s <= 6)

# All slots distinct
solver.add(Distinct(slots))

# Helper: slot_of(band_index) returns the Z3 variable for that band's slot
def slot_of(band_idx):
    return slots[band_idx]

# Constraints:
# 1. Vegemite (1) performs earlier than Zircon (5)
solver.add(slot_of(1) < slot_of(5))

# 2. Wellspring (2) and Zircon (5) each perform earlier than Xpert (3)
solver.add(slot_of(2) < slot_of(3))
solver.add(slot_of(5) < slot_of(3))

# 3. Uneasy (0) performs in one of the last three slots (4,5,6)
solver.add(Or([slot_of(0) == i for i in [4,5,6]]))

# 4. Yardsign (4) performs in one of the first three slots (1,2,3)
solver.add(Or([slot_of(4) == i for i in [1,2,3]]))

# Additional condition: Wellspring (2) performs immediately before Xpert (3)
solver.add(slot_of(2) + 1 == slot_of(3))

# Now evaluate each option
# Option A: Uneasy performs in slot five
opt_a = (slot_of(0) == 5)

# Option B: Vegemite performs in slot three
opt_b = (slot_of(1) == 3)

# Option C: Wellspring performs in slot three
opt_c = (slot_of(2) == 3)

# Option D: Zircon performs in slot two
opt_d = (slot_of(5) == 2)

# Option E: Zircon performs in slot four
opt_e = (slot_of(5) == 4)

found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
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