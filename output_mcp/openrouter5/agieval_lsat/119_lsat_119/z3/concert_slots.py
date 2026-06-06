from z3 import *

solver = Solver()

# Slots 1-6, each band gets one slot
slots = [1, 2, 3, 4, 5, 6]

# Variables for each band's slot
Uneasy, Vegemite, Wellspring, Xpert, Yardsign, Zircon = Ints('Uneasy Vegemite Wellspring Xpert Yardsign Zircon')
bands = [Uneasy, Vegemite, Wellspring, Xpert, Yardsign, Zircon]

# Each band gets a slot from 1 to 6
for b in bands:
    solver.add(b >= 1, b <= 6)

# All slots are distinct
solver.add(Distinct(bands))

# Constraints:
# Vegemite performs in an earlier slot than Zircon.
solver.add(Vegemite < Zircon)

# Wellspring and Zircon each perform in an earlier slot than Xpert.
solver.add(Wellspring < Xpert)
solver.add(Zircon < Xpert)

# Uneasy performs in one of the last three slots (4, 5, or 6).
solver.add(Or([Uneasy == i for i in [4, 5, 6]]))

# Yardsign performs in one of the first three slots (1, 2, or 3).
solver.add(Or([Yardsign == i for i in [1, 2, 3]]))

# Additional condition: Zircon performs immediately before Wellspring.
solver.add(Zircon + 1 == Wellspring)

# Now evaluate each option
# (A) Uneasy performs in slot five.
opt_a = (Uneasy == 5)

# (B) Vegemite performs in slot one.
opt_b = (Vegemite == 1)

# (C) Xpert performs in slot five.
opt_c = (Xpert == 5)

# (D) Yardsign performs in slot two.
opt_d = (Yardsign == 2)

# (E) Zircon performs in slot three.
opt_e = (Zircon == 3)

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