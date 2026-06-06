from z3 import *

solver = Solver()

# Variables: slot for each band (1-6)
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

# All different
solver.add(Distinct(bands))

# Base constraints
solver.add(V < Z)                          # Vegemite earlier than Zircon
solver.add(W < X)                          # Wellspring earlier than Xpert
solver.add(Z < X)                          # Zircon earlier than Xpert
solver.add(Or(U == 4, U == 5, U == 6))    # Uneasy in last three slots
solver.add(Or(Y == 1, Y == 2, Y == 3))    # Yardsign in first three slots

# Additional constraint: Wellspring performs immediately before Xpert
solver.add(X == W + 1)

# Define option constraints
opt_a = (U == 5)                           # Uneasy performs in slot five
opt_b = (V == 3)                           # Vegemite performs in slot three
opt_c = (W == 3)                           # Wellspring performs in slot three
opt_d = (Z == 2)                           # Zircon performs in slot two
opt_e = (Z == 4)                           # Zircon performs in slot four

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