from z3 import *

# Bands
bands = ['U', 'V', 'W', 'X', 'Y', 'Z']
# Slot variables for each band
slot = {b: Int(f'slot_{b}') for b in bands}

solver = Solver()

# Each band in exactly one slot (1-6)
for b in bands:
    solver.add(slot[b] >= 1, slot[b] <= 6)
solver.add(Distinct([slot[b] for b in bands]))

# Constraints
# 1. Vegemite performs in an earlier slot than Zircon.
solver.add(slot['V'] < slot['Z'])
# 2. Wellspring and Zircon each perform in an earlier slot than Xpert.
solver.add(slot['W'] < slot['X'])
solver.add(slot['Z'] < slot['X'])
# 3. Uneasy performs in one of the last three slots.
solver.add(slot['U'] >= 4)
# 4. Yardsign performs in one of the first three slots.
solver.add(slot['Y'] <= 3)

# Check which bands can be in slot 1
possible_in_slot_1 = []
for b in bands:
    solver.push()
    solver.add(slot[b] == 1)
    if solver.check() == sat:
        possible_in_slot_1.append(b)
    solver.pop()

print(f"Possible in slot 1: {possible_in_slot_1}")

# Map bands to names for clarity
# V: Vegemite, W: Wellspring, Y: Yardsign, Z: Zircon, U: Uneasy, X: Xpert
# Possible: V, W, Y

# Test options
# (A)Yardsign
# (B)Vegemite, Wellspring
# (C)Vegemite, Yardsign
# (D)Vegemite, Wellspring, Yardsign
# (E)Vegemite, Wellspring, Yardsign, Zircon

options = {
    "A": ["Y"],
    "B": ["V", "W"],
    "C": ["V", "Y"],
    "D": ["V", "W", "Y"],
    "E": ["V", "W", "Y", "Z"]
}

found_options = []
for letter, bands_list in options.items():
    # Check if the set of bands in the option is exactly the set of bands that can be in slot 1
    # We need to verify that:
    # 1. Every band in the option CAN be in slot 1.
    # 2. Every band NOT in the option CANNOT be in slot 1.
    
    is_valid = True
    # Check 1: All bands in option can be in slot 1
    for b in bands_list:
        if b not in possible_in_slot_1:
            is_valid = False
            break
    
    # Check 2: All bands not in option cannot be in slot 1
    if is_valid:
        for b in bands:
            if b not in bands_list and b in possible_in_slot_1:
                is_valid = False
                break
    
    if is_valid:
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