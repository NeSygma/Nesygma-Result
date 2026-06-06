from z3 import *

solver = Solver()

# Bands: Uneasy, Vegemite, Wellspring, Xpert, Yardsign, Zircon
U, V, W, X, Y, Z = Ints('U V W X Y Z')
bands = [U, V, W, X, Y, Z]

# Each band in a slot 1-6, all different
for b in bands:
    solver.add(b >= 1, b <= 6)
solver.add(Distinct(bands))

# Vegemite performs earlier than Zircon
solver.add(V < Z)

# Wellspring and Zircon each perform earlier than Xpert
solver.add(W < X)
solver.add(Z < X)

# Uneasy performs in one of the last three slots
solver.add(Or(U == 4, U == 5, U == 6))

# Yardsign performs in one of the first three slots
solver.add(Or(Y == 1, Y == 2, Y == 3))

# Additional constraint: Wellspring performs immediately before Xpert
solver.add(X == W + 1)

# Define option constraints
opt_a = (U == 5)
opt_b = (V == 3)
opt_c = (W == 3)
opt_d = (Z == 2)
opt_e = (Z == 4)

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