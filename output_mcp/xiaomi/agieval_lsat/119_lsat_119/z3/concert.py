from z3 import *

solver = Solver()

# Bands: Uneasy, Vegemite, Wellspring, Xpert, Yardsign, Zircon
# Slots: 1-6

U = Int('U')  # Uneasy
V = Int('V')  # Vegemite
W = Int('W')  # Wellspring
X = Int('X')  # Xpert
Y = Int('Y')  # Yardsign
Z = Int('Z')  # Zircon

bands = [U, V, W, X, Y, Z]

# Each band in a slot 1-6, all different
for b in bands:
    solver.add(b >= 1, b <= 6)
solver.add(Distinct(bands))

# Vegemite performs in an earlier slot than Zircon
solver.add(V < Z)

# Wellspring and Zircon each perform in an earlier slot than Xpert
solver.add(W < X)
solver.add(Z < X)

# Uneasy performs in one of the last three slots (4, 5, 6)
solver.add(U >= 4)

# Yardsign performs in one of the first three slots (1, 2, 3)
solver.add(Y <= 3)

# Additional constraint: Zircon performs immediately before Wellspring
solver.add(Z + 1 == W)

# Now evaluate each option
found_options = []

# (A) Uneasy performs in slot five
opt_a = (U == 5)
# (B) Vegemite performs in slot one
opt_b = (V == 1)
# (C) Xpert performs in slot five
opt_c = (X == 5)
# (D) Yardsign performs in slot two
opt_d = (Y == 2)
# (E) Zircon performs in slot three
opt_e = (Z == 3)

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