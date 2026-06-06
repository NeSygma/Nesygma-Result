from z3 import *

# Create solver
solver = Solver()

# Define bands and slots
bands = ["Uneasy", "Vegemite", "Wellspring", "Xpert", "Yardsign", "Zircon"]
slots = [1, 2, 3, 4, 5, 6]

# Create mapping from band to slot (each band gets exactly one slot)
slot_of = {band: Int(f"slot_{band}") for band in bands}

# Each band gets a unique slot between 1 and 6
for band in bands:
    solver.add(slot_of[band] >= 1)
    solver.add(slot_of[band] <= 6)

# All bands must have distinct slots
solver.add(Distinct([slot_of[band] for band in bands]))

# Constraint 1: Vegemite performs in an earlier slot than Zircon
solver.add(slot_of["Vegemite"] < slot_of["Zircon"])

# Constraint 2: Wellspring and Zircon each perform in an earlier slot than Xpert
solver.add(slot_of["Wellspring"] < slot_of["Xpert"])
solver.add(slot_of["Zircon"] < slot_of["Xpert"])

# Constraint 3: Uneasy performs in one of the last three slots (4, 5, or 6)
solver.add(Or(slot_of["Uneasy"] == 4, slot_of["Uneasy"] == 5, slot_of["Uneasy"] == 6))

# Constraint 4: Yardsign performs in one of the first three slots (1, 2, or 3)
solver.add(Or(slot_of["Yardsign"] == 1, slot_of["Yardsign"] == 2, slot_of["Yardsign"] == 3))

# Additional constraint: Wellspring performs immediately before Xpert
# This means slot_of["Wellspring"] + 1 == slot_of["Xpert"]
solver.add(slot_of["Wellspring"] + 1 == slot_of["Xpert"])

# Now test each answer choice
found_options = []

# Option A: Uneasy performs in slot five
opt_a_constr = (slot_of["Uneasy"] == 5)

# Option B: Vegemite performs in slot three
opt_b_constr = (slot_of["Vegemite"] == 3)

# Option C: Wellspring performs in slot three
opt_c_constr = (slot_of["Wellspring"] == 3)

# Option D: Zircon performs in slot two
opt_d_constr = (slot_of["Zircon"] == 2)

# Option E: Zircon performs in slot four
opt_e_constr = (slot_of["Zircon"] == 4)

for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), 
                       ("D", opt_d_constr), ("E", opt_e_constr)]:
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