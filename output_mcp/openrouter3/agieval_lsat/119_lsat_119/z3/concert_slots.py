from z3 import *

# Create solver
solver = Solver()

# Define bands as integers 0-5 for slots 1-6
bands = ["Uneasy", "Vegemite", "Wellspring", "Xpert", "Yardsign", "Zircon"]
slot = {band: Int(f"slot_{band}") for band in bands}

# Each band gets a unique slot from 1 to 6
for band in bands:
    solver.add(slot[band] >= 1, slot[band] <= 6)

# All slots are distinct
solver.add(Distinct([slot[band] for band in bands]))

# Constraint 1: Vegemite < Zircon
solver.add(slot["Vegemite"] < slot["Zircon"])

# Constraint 2: Wellspring < Xpert and Zircon < Xpert
solver.add(slot["Wellspring"] < slot["Xpert"])
solver.add(slot["Zircon"] < slot["Xpert"])

# Constraint 3: Uneasy in slots 4, 5, or 6
solver.add(Or(slot["Uneasy"] == 4, slot["Uneasy"] == 5, slot["Uneasy"] == 6))

# Constraint 4: Yardsign in slots 1, 2, or 3
solver.add(Or(slot["Yardsign"] == 1, slot["Yardsign"] == 2, slot["Yardsign"] == 3))

# Additional condition: Zircon performs immediately before Wellspring
# This means Zircon's slot is exactly one less than Wellspring's slot
solver.add(slot["Zircon"] == slot["Wellspring"] - 1)

# Define the answer choices as constraints
opt_a_constr = slot["Uneasy"] == 5
opt_b_constr = slot["Vegemite"] == 1
opt_c_constr = slot["Xpert"] == 5
opt_d_constr = slot["Yardsign"] == 2
opt_e_constr = slot["Zircon"] == 3

# Test each option
found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), 
                       ("D", opt_d_constr), ("E", opt_e_constr)]:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
    solver.pop()

# Print results
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")