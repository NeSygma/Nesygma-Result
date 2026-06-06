from z3 import *

# Bands: Uneasy=0, Vegemite=1, Wellspring=2, Xpert=3, Yardsign=4, Zircon=5
# Slots: 1-6 (each band gets a unique slot)

solver = Solver()

# Each band assigned to a slot (1-6)
U = Int('U')  # Uneasy
V = Int('V')  # Vegemite
W = Int('W')  # Wellspring
X = Int('X')  # Xpert
Y = Int('Y')  # Yardsign
Z = Int('Z')  # Zircon

bands = [U, V, W, X, Y, Z]

# All slots between 1 and 6
for b in bands:
    solver.add(b >= 1, b <= 6)

# All bands in different slots
solver.add(Distinct(bands))

# Constraint 1: Vegemite performs earlier than Zircon
solver.add(V < Z)

# Constraint 2: Wellspring performs earlier than Xpert
solver.add(W < X)

# Constraint 3: Zircon performs earlier than Xpert
solver.add(Z < X)

# Constraint 4: Uneasy performs in one of the last three slots (4, 5, 6)
solver.add(U >= 4)

# Constraint 5: Yardsign performs in one of the first three slots (1, 2, 3)
solver.add(Y <= 3)

# Now test which bands can be in slot 1
# The question asks for a complete and accurate list of bands that COULD be in slot 1

band_names = {U: "Uneasy", V: "Vegemite", W: "Wellspring", X: "Xpert", Y: "Yardsign", Z: "Zircon"}
can_be_slot1 = []

for band_var, name in band_names.items():
    s = Solver()
    # Copy all base constraints
    for c in solver.assertions():
        s.add(c)
    # Add constraint that this band is in slot 1
    s.add(band_var == 1)
    if s.check() == sat:
        can_be_slot1.append(name)
        print(f"{name} CAN be in slot 1")
    else:
        print(f"{name} CANNOT be in slot 1")

print(f"\nBands that can be in slot 1: {can_be_slot1}")

# Now match to answer choices
# (A) Yardsign
# (B) Vegemite, Wellspring
# (C) Vegemite, Yardsign
# (D) Vegemite, Wellspring, Yardsign
# (E) Vegemite, Wellspring, Yardsign, Zircon

# The answer choices define which bands can be in slot 1
# We need to check: for each option, is the list EXACTLY the set of bands that can be in slot 1?

# First, let's determine which bands can be in slot 1 by testing each
options = {
    "A": ["Yardsign"],
    "B": ["Vegemite", "Wellspring"],
    "C": ["Vegemite", "Yardsign"],
    "D": ["Vegemite", "Wellspring", "Yardsign"],
    "E": ["Vegemite", "Wellspring", "Yardsign", "Zircon"]
}

# An option is correct if:
# 1. Every band in the option CAN be in slot 1
# 2. Every band NOT in the option CANNOT be in slot 1

found_options = []
for letter, band_list in options.items():
    option_set = set(band_list)
    # Check if this matches exactly the set of bands that can be in slot 1
    if option_set == set(can_be_slot1):
        found_options.append(letter)

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")