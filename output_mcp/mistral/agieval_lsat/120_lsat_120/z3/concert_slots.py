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

# Assignment: assignment[i] = band assigned to slot i (0-based index for slots 1-6)
assignment = [Int(f"slot_{i}") for i in range(6)]

# Each slot must be assigned a unique band (permutation)
solver.add(Distinct(assignment))

# Constraints:
# 1. Vegemite performs earlier than Zircon
# Compute indices for Vegemite and Zircon
veg_index = Sum([If(assignment[i] == Vegemite, 1, 0) * i for i in range(6)])
zirc_index = Sum([If(assignment[i] == Zircon, 1, 0) * i for i in range(6)])
solver.add(veg_index < zirc_index)

# 2. Wellspring and Zircon each perform earlier than Xpert
# Compute indices for Wellspring and Xpert
well_index = Sum([If(assignment[i] == Wellspring, 1, 0) * i for i in range(6)])
xpert_index = Sum([If(assignment[i] == Xpert, 1, 0) * i for i in range(6)])
solver.add(well_index < xpert_index)
solver.add(zirc_index < xpert_index)

# 3. Uneasy performs in one of the last three slots (indices 3,4,5 in 0-based)
uneasy_index = Sum([If(assignment[i] == Uneasy, 1, 0) * i for i in range(6)])
solver.add(Or(uneasy_index == 3, uneasy_index == 4, uneasy_index == 5))

# 4. Yardsign performs in one of the first three slots (indices 0,1,2 in 0-based)
yardsign_index = Sum([If(assignment[i] == Yardsign, 1, 0) * i for i in range(6)])
solver.add(Or(yardsign_index == 0, yardsign_index == 1, yardsign_index == 2))

# Now, evaluate the multiple-choice options
# We need to check for each option whether it is possible that slot 0 (slot one) is assigned to any of the bands listed in that option

# Define the options as constraints on slot 0
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