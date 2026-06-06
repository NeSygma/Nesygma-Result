from z3 import *

# Declare slot variables for each band
Uneasy = Int('Uneasy')
Vegemite = Int('Vegemite')
Wellspring = Int('Wellspring')
Xpert = Int('Xpert')
Yardsign = Int('Yardsign')
Zircon = Int('Zircon')

bands = [Uneasy, Vegemite, Wellspring, Xpert, Yardsign, Zircon]
solver = Solver()

# Domain constraints: slots 1..6
for b in bands:
    solver.add(b >= 1, b <= 6)
# All distinct slots
solver.add(Distinct(bands))

# Base constraints from problem
solver.add(Vegemite < Zircon)               # Vegemite earlier than Zircon
solver.add(Wellspring < Xpert)              # Wellspring earlier than Xpert
solver.add(Zircon < Xpert)                  # Zircon earlier than Xpert
solver.add(Uneasy >= 4)                     # Uneasy in last three slots (4,5,6)
solver.add(Yardsign <= 3)                   # Yardsign in first three slots (1,2,3)

# Additional condition: Zircon immediately before Wellspring
solver.add(Zircon + 1 == Wellspring)

# Define option constraints
opt_a_constr = Uneasy == 5
opt_b_constr = Vegemite == 1
opt_c_constr = Xpert == 5
opt_d_constr = Yardsign == 2
opt_e_constr = Zircon == 3

found_options = []
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