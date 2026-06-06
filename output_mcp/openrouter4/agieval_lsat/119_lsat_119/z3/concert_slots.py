from z3 import *

# Six slots 1-6, six bands
solver = Solver()

# Variables for each band's slot position (1-6)
U = Int('U')  # Uneasy
V = Int('V')  # Vegemite
W = Int('W')  # Wellspring
X = Int('X')  # Xpert
Y = Int('Y')  # Yardsign
Z = Int('Z')  # Zircon

bands = [U, V, W, X, Y, Z]

# Domain: each band in exactly one slot 1-6
for b in bands:
    solver.add(b >= 1, b <= 6)

# All slots distinct (permutation)
solver.add(Distinct(bands))

# Constraints:
# 1. Vegemite performs in an earlier slot than Zircon
solver.add(V < Z)

# 2. Wellspring and Zircon each perform in an earlier slot than Xpert
solver.add(W < X)
solver.add(Z < X)

# 3. Uneasy performs in one of the last three slots
solver.add(Or(U == 4, U == 5, U == 6))

# 4. Yardsign performs in one of the first three slots
solver.add(Or(Y == 1, Y == 2, Y == 3))

# Extra condition: Zircon performs immediately before Wellspring
solver.add(Z + 1 == W)

# For "must be true" (MBT), we test each option:
# If adding the NEGATION of an option makes the system unsatisfiable,
# then that option must be true in all models.

found_options = []

for letter, neg_constr in [
    ("A", Not(U == 5)),        # Negation of "Uneasy performs in slot five"
    ("B", Not(V == 1)),        # Negation of "Vegemite performs in slot one"
    ("C", Not(X == 5)),        # Negation of "Xpert performs in slot five"
    ("D", Not(Y == 2)),        # Negation of "Yardsign performs in slot two"
    ("E", Not(Z == 3))         # Negation of "Zircon performs in slot three"
]:
    solver.push()
    solver.add(neg_constr)
    if solver.check() == unsat:
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