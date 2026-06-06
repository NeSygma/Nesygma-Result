from z3 import *

# Declare variables for each band representing their slot (1..6)
Uneasy = Int('Uneasy')
Vegemite = Int('Vegemite')
Wellspring = Int('Wellspring')
Xpert = Int('Xpert')
Yardsign = Int('Yardsign')
Zircon = Int('Zircon')

bands = [Uneasy, Vegemite, Wellspring, Xpert, Yardsign, Zircon]
solver = Solver()

# Domain constraints: each slot between 1 and 6
for b in bands:
    solver.add(b >= 1, b <= 6)

# All slots distinct
solver.add(Distinct(bands))

# Base ordering constraints
solver.add(Vegemite < Zircon)               # Vegemite earlier than Zircon
solver.add(Wellspring < Xpert)               # Wellspring earlier than Xpert
solver.add(Zircon < Xpert)                   # Zircon earlier than Xpert
solver.add(Uneasy >= 4)                      # Uneasy in last three slots (4,5,6)
solver.add(Yardsign <= 3)                    # Yardsign in first three slots (1,2,3)

# Additional condition for the question: Wellspring immediately before Xpert
solver.add(Xpert == Wellspring + 1)

# Define option constraints
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