from z3 import *

# Create solver
solver = Solver()

# Define bands and slots
bands = ["Uneasy", "Vegemite", "Wellspring", "Xpert", "Yardsign", "Zircon"]
slot = {band: Int(f"slot_{band}") for band in bands}

# Each band gets a unique slot from 1 to 6
for band in bands:
    solver.add(slot[band] >= 1, slot[band] <= 6)

# All bands in different slots
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

# First, find all possible bands that could be in slot 1
possible_slot1_bands = []
for band in bands:
    solver.push()
    solver.add(slot[band] == 1)
    if solver.check() == sat:
        possible_slot1_bands.append(band)
    solver.pop()

print("Possible bands for slot 1:", possible_slot1_bands)

# Now check each answer choice
# Option A: Yardsign only
opt_a = slot["Yardsign"] == 1

# Option B: Vegemite, Wellspring (either could be in slot 1)
opt_b = Or(slot["Vegemite"] == 1, slot["Wellspring"] == 1)

# Option C: Vegemite, Yardsign (either could be in slot 1)
opt_c = Or(slot["Vegemite"] == 1, slot["Yardsign"] == 1)

# Option D: Vegemite, Wellspring, Yardsign (any one could be in slot 1)
opt_d = Or(slot["Vegemite"] == 1, slot["Wellspring"] == 1, slot["Yardsign"] == 1)

# Option E: Vegemite, Wellspring, Yardsign, Zircon (any one could be in slot 1)
opt_e = Or(slot["Vegemite"] == 1, slot["Wellspring"] == 1, slot["Yardsign"] == 1, slot["Zircon"] == 1)

# Test each option
found_options = []

# Test A
solver.push()
solver.add(opt_a)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Test B
solver.push()
solver.add(opt_b)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Test C
solver.push()
solver.add(opt_c)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Test D
solver.push()
solver.add(opt_d)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Test E
solver.push()
solver.add(opt_e)
if solver.check() == sat:
    found_options.append("E")
solver.pop()

print("Found options:", found_options)

# Check which option is correct
# We need to verify that the option lists ALL possible bands for slot 1
# and NO other bands

# First, verify which bands can actually be in slot 1
actual_possible = []
for band in bands:
    solver.push()
    solver.add(slot[band] == 1)
    if solver.check() == sat:
        actual_possible.append(band)
    solver.pop()

print("Actual possible bands for slot 1:", actual_possible)

# Now check which option matches exactly
correct_option = None
if set(actual_possible) == {"Yardsign"} and "A" in found_options:
    correct_option = "A"
elif set(actual_possible) == {"Vegemite", "Wellspring"} and "B" in found_options:
    correct_option = "B"
elif set(actual_possible) == {"Vegemite", "Yardsign"} and "C" in found_options:
    correct_option = "C"
elif set(actual_possible) == {"Vegemite", "Wellspring", "Yardsign"} and "D" in found_options:
    correct_option = "D"
elif set(actual_possible) == {"Vegemite", "Wellspring", "Yardsign", "Zircon"} and "E" in found_options:
    correct_option = "E"

if correct_option:
    print("STATUS: sat")
    print(f"answer:{correct_option}")
else:
    print("STATUS: unsat")
    print("Refine: No correct option found")