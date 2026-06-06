from z3 import *

# Create solver
solver = Solver()

# Define bands as integers 1-6 representing slots
bands = ["Uneasy", "Vegemite", "Wellspring", "Xpert", "Yardsign", "Zircon"]
slot = {band: Int(f"slot_{band}") for band in bands}

# Base constraints: each band gets a unique slot from 1 to 6
for band in bands:
    solver.add(slot[band] >= 1, slot[band] <= 6)

# All bands must have different slots
solver.add(Distinct([slot[band] for band in bands]))

# Constraint 1: Vegemite performs in an earlier slot than Zircon
solver.add(slot["Vegemite"] < slot["Zircon"])

# Constraint 2: Wellspring and Zircon each perform in an earlier slot than Xpert
solver.add(slot["Wellspring"] < slot["Xpert"])
solver.add(slot["Zircon"] < slot["Xpert"])

# Constraint 3: Uneasy performs in one of the last three slots (4, 5, or 6)
solver.add(Or(slot["Uneasy"] == 4, slot["Uneasy"] == 5, slot["Uneasy"] == 6))

# Constraint 4: Yardsign performs in one of the first three slots (1, 2, or 3)
solver.add(Or(slot["Yardsign"] == 1, slot["Yardsign"] == 2, slot["Yardsign"] == 3))

# Now test each option: Which band CANNOT be in slot 5?
# We need to check for each band if there exists a valid assignment where that band is in slot 5
# If NO valid assignment exists for a band in slot 5, then that band CANNOT be in slot 5

found_options = []
for letter, band in [("A", "Uneasy"), ("B", "Vegemite"), ("C", "Wellspring"), ("D", "Xpert"), ("E", "Zircon")]:
    solver.push()
    # Add constraint that this band is in slot 5
    solver.add(slot[band] == 5)
    if solver.check() == sat:
        # This band CAN be in slot 5 (there exists a valid assignment)
        # We're looking for which CANNOT be in slot 5, so we don't add to found_options
        pass
    else:
        # This band CANNOT be in slot 5 (no valid assignment exists)
        found_options.append(letter)
    solver.pop()

# According to the problem, we're looking for which CANNOT be in slot 5
# So found_options should contain exactly one letter
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")