from z3 import *

solver = Solver()
# Variables: slot numbers for each band
Uneasy = Int('Uneasy')
Vegemite = Int('Vegemite')
Wellspring = Int('Wellspring')
Xpert = Int('Xpert')
Yardsign = Int('Yardsign')
Zircon = Int('Zircon')
bands = [Uneasy, Vegemite, Wellspring, Xpert, Yardsign, Zircon]
# Domain constraints
for b in bands:
    solver.add(b >= 1, b <= 6)
# All distinct
solver.add(Distinct(bands))
# Base constraints
solver.add(Vegemite < Zircon)               # Vegemite earlier than Zircon
solver.add(Wellspring < Xpert)              # Wellspring earlier than Xpert
solver.add(Zircon < Xpert)                  # Zircon earlier than Xpert
solver.add(Uneasy >= 4)                     # Uneasy in last three slots (4,5,6)
solver.add(Yardsign <= 3)                   # Yardsign in first three slots (1,2,3)
# Additional condition: Zircon immediately before Wellspring
solver.add(Zircon + 1 == Wellspring)

# Define option constraints
opt_a = Uneasy == 5
opt_b = Vegemite == 1
opt_c = Xpert == 5
opt_d = Yardsign == 2
opt_e = Zircon == 3

options = [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]
found_options = []
for letter, constr in options:
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