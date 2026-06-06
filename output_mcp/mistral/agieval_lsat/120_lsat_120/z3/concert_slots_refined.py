from z3 import *

# Define the bands as constants for clarity
Uneasy = 0
Vegemite = 1
Wellspring = 2
Xpert = 3
Yardsign = 4
Zircon = 5

# Create a solver
solver = Solver()

# Assignment: assignment[i] = band assigned to slot i (1-based index for slots 1-6)
# We'll use 0-based list indices for simplicity, but the constraints will refer to 1-based slot numbers
assignment = [Int(f"slot_{i+1}") for i in range(6)]

# Each slot must be assigned a unique band (permutation)
solver.add(Distinct(assignment))

# Constraints:
# 1. Vegemite performs earlier than Zircon
# Find the slot numbers for Vegemite and Zircon
veg_slot = Sum([If(assignment[i] == Vegemite, i+1, 0) for i in range(6)])
zirc_slot = Sum([If(assignment[i] == Zircon, i+1, 0) for i in range(6)])
solver.add(veg_slot > 0)
solver.add(zirc_slot > 0)
solver.add(veg_slot < zirc_slot)

# 2. Wellspring and Zircon each perform earlier than Xpert
well_slot = Sum([If(assignment[i] == Wellspring, i+1, 0) for i in range(6)])
xpert_slot = Sum([If(assignment[i] == Xpert, i+1, 0) for i in range(6)])
solver.add(well_slot > 0)
solver.add(xpert_slot > 0)
solver.add(well_slot < xpert_slot)
solver.add(zirc_slot < xpert_slot)

# 3. Uneasy performs in one of the last three slots (slots 4,5,6 in 1-based)
uneasy_slot = Sum([If(assignment[i] == Uneasy, i+1, 0) for i in range(6)])
solver.add(Or(uneasy_slot == 4, uneasy_slot == 5, uneasy_slot == 6))

# 4. Yardsign performs in one of the first three slots (slots 1,2,3 in 1-based)
yardsign_slot = Sum([If(assignment[i] == Yardsign, i+1, 0) for i in range(6)])
solver.add(Or(yardsign_slot == 1, yardsign_slot == 2, yardsign_slot == 3))

# Now, evaluate the multiple-choice options
# We need to check for each option whether it is possible that slot 1 is assigned to any of the bands listed in that option

# Define the options as constraints on slot 1
options = {
    "A": assignment[0] == Yardsign,
    "B": Or(assignment[0] == Vegemite, assignment[0] == Wellspring),
    "C": Or(assignment[0] == Vegemite, assignment[0] == Yardsign),
    "D": Or(assignment[0] == Vegemite, assignment[0] == Wellspring, assignment[0] == Yardsign),
    "E": Or(assignment[0] == Vegemite, assignment[0] == Wellspring, assignment[0] == Yardsign, assignment[0] == Zircon)
}

found_options = []
for letter, constr in options.items():
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