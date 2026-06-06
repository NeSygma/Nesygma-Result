from z3 import *

solver = Solver()

# Bands: Uneasy, Vegemite, Wellspring, Xpert, Yardsign, Zircon
U, V, W, X, Y, Z = Ints('U V W X Y Z')
bands = [U, V, W, X, Y, Z]
band_names = ['Uneasy', 'Vegemite', 'Wellspring', 'Xpert', 'Yardsign', 'Zircon']

# Each band assigned to a slot 1-6, all different
for b in bands:
    solver.add(b >= 1, b <= 6)
solver.add(Distinct(bands))

# Base constraints
solver.add(V < Z)       # Vegemite earlier than Zircon
solver.add(W < X)       # Wellspring earlier than Xpert
solver.add(Z < X)       # Zircon earlier than Xpert
solver.add(U >= 4)      # Uneasy in last three slots
solver.add(Y <= 3)      # Yardsign in first three slots

# Additional constraint: Vegemite performs in slot 3
solver.add(V == 3)

# Define the answer options
opt_a = (U < X)   # Uneasy earlier than Xpert
opt_b = (W < Z)   # Wellspring earlier than Zircon
opt_c = (X < U)   # Xpert earlier than Uneasy
opt_d = (Y < W)   # Yardsign earlier than Wellspring
opt_e = (Z < U)   # Zircon earlier than Uneasy

options = [
    ("A", opt_a),
    ("B", opt_b),
    ("C", opt_c),
    ("D", opt_d),
    ("E", opt_e),
]

found_options = []
for letter, constr in options:
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