from z3 import *

# Create solver
solver = Solver()

# Declare variables for each band's slot (1-6)
Uneasy = Int('Uneasy')
Vegemite = Int('Vegemite')
Wellspring = Int('Wellspring')
Xpert = Int('Xpert')
Yardsign = Int('Yardsign')
Zircon = Int('Zircon')

# All bands in different slots (1-6)
bands = [Uneasy, Vegemite, Wellspring, Xpert, Yardsign, Zircon]
solver.add(Distinct(bands))
for band in bands:
    solver.add(band >= 1, band <= 6)

# Base constraints
# 1. Vegemite < Zircon
solver.add(Vegemite < Zircon)
# 2. Wellspring < Xpert and Zircon < Xpert
solver.add(Wellspring < Xpert)
solver.add(Zircon < Xpert)
# 3. Uneasy in last three slots (4,5,6)
solver.add(Or([Uneasy == 4, Uneasy == 5, Uneasy == 6]))
# 4. Yardsign in first three slots (1,2,3)
solver.add(Or([Yardsign == 1, Yardsign == 2, Yardsign == 3]))
# Additional condition: Vegemite performs in slot 3
solver.add(Vegemite == 3)

# Define options as constraints
opt_a = Uneasy < Xpert
opt_b = Wellspring < Zircon
opt_c = Xpert < Uneasy
opt_d = Yardsign < Wellspring
opt_e = Zircon < Uneasy

# Test each option: check if its negation is UNSAT (must be true)
must_be_true_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(Not(constr))  # Check if option can be false
    result = solver.check()
    solver.pop()
    if result == unsat:
        must_be_true_options.append(letter)

# Print results
if len(must_be_true_options) == 1:
    print("STATUS: sat")
    print(f"answer:{must_be_true_options[0]}")
elif len(must_be_true_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options must be true {must_be_true_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options must be true")