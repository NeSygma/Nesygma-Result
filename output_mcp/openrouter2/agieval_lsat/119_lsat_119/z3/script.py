from z3 import *

solver = Solver()
# Variables for each band's slot
Uneasy = Int('Uneasy')
Vegemite = Int('Vegemite')
Wellspring = Int('Wellspring')
Xpert = Int('Xpert')
Yardsign = Int('Yardsign')
Zircon = Int('Zircon')

# Domain constraints: slots 1..6
for var in [Uneasy, Vegemite, Wellspring, Xpert, Yardsign, Zircon]:
    solver.add(var >= 1, var <= 6)

# All distinct
solver.add(Distinct([Uneasy, Vegemite, Wellspring, Xpert, Yardsign, Zircon]))

# Constraints
solver.add(Vegemite < Zircon)
solver.add(Wellspring < Xpert)
solver.add(Zircon < Xpert)
# Uneasy in last three slots
solver.add(Or(Uneasy == 4, Uneasy == 5, Uneasy == 6))
# Yardsign in first three slots
solver.add(Or(Yardsign == 1, Yardsign == 2, Yardsign == 3))
# Zircon immediately before Wellspring
solver.add(Zircon + 1 == Wellspring)

# Option constraints
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