from z3 import *
solver = Solver()
# Define integer variables for each band's slot (1-6)
Uneasy = Int('Uneasy')
Vegemite = Int('Vegemite')
Wellspring = Int('Wellspring')
Xpert = Int('Xpert')
Yardsign = Int('Yardsign')
Zircon = Int('Zircon')
# Domain constraints: slots 1 through 6
for var in [Uneasy, Vegemite, Wellspring, Xpert, Yardsign, Zircon]:
    solver.add(var >= 1, var <= 6)
# All slots distinct
solver.add(Distinct([Uneasy, Vegemite, Wellspring, Xpert, Yardsign, Zircon]))
# Base constraints
solver.add(Vegemite < Zircon)
solver.add(Wellspring < Xpert)
solver.add(Zircon < Xpert)
solver.add(Uneasy >= 4)  # Uneasy in last three slots (4,5,6)
solver.add(Yardsign <= 3)  # Yardsign in first three slots (1,2,3)
# Additional condition: Wellspring immediately before Xpert
solver.add(Xpert == Wellspring + 1)
# Option constraints
opt_a_constr = Uneasy == 5
opt_b_constr = Vegemite == 3
opt_c_constr = Wellspring == 3
opt_d_constr = Zircon == 2
opt_e_constr = Zircon == 4

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