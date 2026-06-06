from z3 import *

solver = Solver()

# Bands: Uneasy, Vegemite, Wellspring, Xpert, Yardsign, Zircon
# Each assigned to a slot 1-6, all different
U, V, W, X, Y, Z = Ints('U V W X Y Z')
bands = [U, V, W, X, Y, Z]

# Each band in a slot 1-6
for b in bands:
    solver.add(b >= 1, b <= 6)

# All different
solver.add(Distinct(bands))

# Vegemite earlier than Zircon
solver.add(V < Z)

# Wellspring earlier than Xpert
solver.add(W < X)

# Zircon earlier than Xpert
solver.add(Z < X)

# Uneasy in last three slots (4, 5, or 6)
solver.add(Or(U == 4, U == 5, U == 6))

# Yardsign in first three slots (1, 2, or 3)
solver.add(Or(Y == 1, Y == 2, Y == 3))

# Now test each option: which band CANNOT be in slot 5?
options = [
    ("A", U == 5),  # Uneasy
    ("B", V == 5),  # Vegemite
    ("C", W == 5),  # Wellspring
    ("D", X == 5),  # Xpert
    ("E", Z == 5),  # Zircon
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