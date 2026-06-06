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
solver.add(slot["Zircon"] == slot["Wellspring"] - 1)

# Now we need to check which statement MUST be true
# We'll check each option by seeing if its negation leads to unsat
# If negating an option makes the problem unsat, then the option must be true

options = [
    ("A", slot["Uneasy"] == 5),
    ("B", slot["Vegemite"] == 1),
    ("C", slot["Xpert"] == 5),
    ("D", slot["Yardsign"] == 2),
    ("E", slot["Zircon"] == 3)
]

must_be_true = []

for letter, option_constr in options:
    # Create a new solver to test if option must be true
    test_solver = Solver()
    
    # Add all base constraints
    for band in bands:
        test_solver.add(slot[band] >= 1, slot[band] <= 6)
    test_solver.add(Distinct([slot[band] for band in bands]))
    test_solver.add(slot["Vegemite"] < slot["Zircon"])
    test_solver.add(slot["Wellspring"] < slot["Xpert"])
    test_solver.add(slot["Zircon"] < slot["Xpert"])
    test_solver.add(Or(slot["Uneasy"] == 4, slot["Uneasy"] == 5, slot["Uneasy"] == 6))
    test_solver.add(Or(slot["Yardsign"] == 1, slot["Yardsign"] == 2, slot["Yardsign"] == 3))
    test_solver.add(slot["Zircon"] == slot["Wellspring"] - 1)
    
    # Add the NEGATION of the option
    test_solver.add(Not(option_constr))
    
    # Check if this is satisfiable
    if test_solver.check() == unsat:
        # If negation is unsat, then the option must be true
        must_be_true.append(letter)

print(f"Options that must be true: {must_be_true}")

if len(must_be_true) == 1:
    print("STATUS: sat")
    print(f"answer:{must_be_true[0]}")
elif len(must_be_true) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options must be true {must_be_true}")
else:
    print("STATUS: unsat")
    print("Refine: No options must be true")