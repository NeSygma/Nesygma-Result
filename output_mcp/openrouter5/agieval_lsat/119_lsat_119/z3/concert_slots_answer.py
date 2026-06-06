from z3 import *

solver = Solver()

# Variables for each band's slot
Uneasy, Vegemite, Wellspring, Xpert, Yardsign, Zircon = Ints('Uneasy Vegemite Wellspring Xpert Yardsign Zircon')
bands = [Uneasy, Vegemite, Wellspring, Xpert, Yardsign, Zircon]

# Each band gets a slot from 1 to 6
for b in bands:
    solver.add(b >= 1, b <= 6)

# All slots are distinct
solver.add(Distinct(bands))

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

# Now evaluate each option as "must be true" - check if the option holds in ALL models
# We do this by checking if the negation of the option is unsatisfiable
found_options = []
for letter, constr in [("A", Uneasy == 5), ("B", Vegemite == 1), ("C", Xpert == 5), ("D", Yardsign == 2), ("E", Zircon == 3)]:
    s2 = Solver()
    for c in solver.assertions():
        s2.add(c)
    s2.add(Not(constr))
    if s2.check() == unsat:
        found_options.append(letter)

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")