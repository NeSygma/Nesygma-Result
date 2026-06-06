from z3 import *

# Create a solver
solver = Solver()

# Declare variables for each band's slot (1-6)
uneasy = Int('uneasy')
vegemite = Int('vegemite')
wellspring = Int('wellspring')
xpert = Int('xpert')
yardsign = Int('yardsign')
zircon = Int('zircon')

# Each band is assigned to a unique slot (1-6)
slots = [uneasy, vegemite, wellspring, xpert, yardsign, zircon]
solver.add(Distinct(slots))
for slot in slots:
    solver.add(slot >= 1, slot <= 6)

# Constraints:
# 1. Vegemite performs earlier than Zircon
solver.add(vegemite < zircon)
# 2. Wellspring and Zircon perform earlier than Xpert
solver.add(wellspring < xpert)
solver.add(zircon < xpert)
# 3. Uneasy performs in one of the last three slots
solver.add(uneasy >= 4)
# 4. Yardsign performs in one of the first three slots
solver.add(yardsign <= 3)

# Base constraints are now added. Now evaluate each answer choice.

# Define the options as constraints for slot 1
# Option A: Yardsign is in slot 1
opt_a_constr = (yardsign == 1)
# Option B: Vegemite or Wellspring is in slot 1
opt_b_constr = Or(vegemite == 1, wellspring == 1)
# Option C: Vegemite or Yardsign is in slot 1
opt_c_constr = Or(vegemite == 1, yardsign == 1)
# Option D: Vegemite, Wellspring, or Yardsign is in slot 1
opt_d_constr = Or(vegemite == 1, wellspring == 1, yardsign == 1)
# Option E: Vegemite, Wellspring, Yardsign, or Zircon is in slot 1
opt_e_constr = Or(vegemite == 1, wellspring == 1, yardsign == 1, zircon == 1)

# Evaluate each option
found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
    solver.pop()

# Output the result
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")