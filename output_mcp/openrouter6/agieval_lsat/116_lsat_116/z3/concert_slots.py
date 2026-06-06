from z3 import *

solver = Solver()

# Define variables for each band's slot (1 to 6)
Uneasy = Int('Uneasy')
Vegemite = Int('Vegemite')
Wellspring = Int('Wellspring')
Xpert = Int('Xpert')
Yardsign = Int('Yardsign')
Zircon = Int('Zircon')

# All slots are between 1 and 6
bands = [Uneasy, Vegemite, Wellspring, Xpert, Yardsign, Zircon]
for band in bands:
    solver.add(band >= 1, band <= 6)

# All bands perform in distinct slots
solver.add(Distinct(bands))

# Constraint 1: Vegemite performs in an earlier slot than Zircon
solver.add(Vegemite < Zircon)

# Constraint 2: Wellspring and Zircon each perform in an earlier slot than Xpert
solver.add(Wellspring < Xpert)
solver.add(Zircon < Xpert)

# Constraint 3: Uneasy performs in one of the last three slots (4,5,6)
solver.add(Or([Uneasy == 4, Uneasy == 5, Uneasy == 6]))

# Constraint 4: Yardsign performs in one of the first three slots (1,2,3)
solver.add(Or([Yardsign == 1, Yardsign == 2, Yardsign == 3]))

# Now test each option: which band CANNOT be in slot 5?
# We'll test by adding the constraint that the band is in slot 5.
# If the solver returns unsat, that band cannot be in slot 5.

found_options = []
options = [
    ("A", Uneasy),
    ("B", Vegemite),
    ("C", Wellspring),
    ("D", Xpert),
    ("E", Zircon)
]

for letter, band in options:
    solver.push()
    solver.add(band == 5)
    result = solver.check()
    if result == unsat:
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