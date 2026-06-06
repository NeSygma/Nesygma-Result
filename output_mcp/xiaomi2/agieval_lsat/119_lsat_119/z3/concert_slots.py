from z3 import *

solver = Solver()

# Define slot positions for each band (1-6)
U = Int('U')  # Uneasy
V = Int('V')  # Vegemite
W = Int('W')  # Wellspring
X = Int('X')  # Xpert
Y = Int('Y')  # Yardsign
Z = Int('Z')  # Zircon

bands = [U, V, W, X, Y, Z]

# Each band in a slot 1-6
for b in bands:
    solver.add(b >= 1, b <= 6)

# All bands in different slots
solver.add(Distinct(bands))

# Base constraints from problem
solver.add(V < Z)           # Vegemite earlier than Zircon
solver.add(W < X)           # Wellspring earlier than Xpert
solver.add(Z < X)           # Zircon earlier than Xpert
solver.add(Or(U == 4, U == 5, U == 6))  # Uneasy in last three slots
solver.add(Or(Y == 1, Y == 2, Y == 3))  # Yardsign in first three slots

# Additional condition: Zircon performs immediately before Wellspring
solver.add(Z + 1 == W)

# Define answer choice constraints
opt_a = (U == 5)            # Uneasy performs in slot five
opt_b = (V == 1)            # Vegemite performs in slot one
opt_c = (X == 5)            # Xpert performs in slot five
opt_d = (Y == 2)            # Yardsign performs in slot two
opt_e = (Z == 3)            # Zircon performs in slot three

found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
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