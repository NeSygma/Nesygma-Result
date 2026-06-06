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

# Assignment: assignment[i] = band assigned to slot i (0-based index for slots 0-5, representing slots 1-6)
assignment = [Int(f"slot_{i+1}") for i in range(6)]

# Each slot must be assigned a unique band (permutation)
solver.add(Distinct(assignment))

# Constraints:
# 1. Vegemite performs earlier than Zircon
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
# We need to check for each option whether it is a complete and accurate list of bands that could be in slot 1

# Define the options as sets of bands that could be in slot 1
options = {
    "A": [Yardsign],
    "B": [Vegemite, Wellspring],
    "C": [Vegemite, Yardsign],
    "D": [Vegemite, Wellspring, Yardsign],
    "E": [Vegemite, Wellspring, Yardsign, Zircon]
}

valid_options = []

for letter, allowed_bands in options.items():
    # Check if all bands in the option can be in slot 1
    all_can_be_in_slot1 = True
    for band in allowed_bands:
        solver.push()
        solver.add(assignment[0] == band)
        if solver.check() != sat:
            all_can_be_in_slot1 = False
        solver.pop()
    
    if not all_can_be_in_slot1:
        continue
    
    # Check if no other band can be in slot 1 (completeness)
    other_bands = [b for b in [Uneasy, Vegemite, Wellspring, Xpert, Yardsign, Zircon] if b not in allowed_bands]
    no_other_can_be_in_slot1 = True
    for band in other_bands:
        solver.push()
        solver.add(assignment[0] == band)
        if solver.check() == sat:
            no_other_can_be_in_slot1 = False
        solver.pop()
    
    if no_other_can_be_in_slot1:
        valid_options.append(letter)

if len(valid_options) == 1:
    print("STATUS: sat")
    print(f"answer:{valid_options[0]}")
elif len(valid_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {valid_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")