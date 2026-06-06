from z3 import *

solver = Solver()

# Slots 1-6, bands: Uneasy, Vegemite, Wellspring, Xpert, Yardsign, Zircon
U, V, W, X, Y, Z = Ints('U V W X Y Z')
bands = [U, V, W, X, Y, Z]

# Each band in a distinct slot 1-6
for b in bands:
    solver.add(b >= 1, b <= 6)
solver.add(Distinct(bands))

# Constraints:
# Vegemite performs in an earlier slot than Zircon.
solver.add(V < Z)

# Wellspring and Zircon each perform in an earlier slot than Xpert.
solver.add(W < X)
solver.add(Z < X)

# Uneasy performs in one of the last three slots.
solver.add(Or([U == i for i in [4, 5, 6]]))

# Yardsign performs in one of the first three slots.
solver.add(Or([Y == i for i in [1, 2, 3]]))

# Additional condition: Vegemite performs in slot three.
solver.add(V == 3)

# Now evaluate each option using the required skeleton
found_options = []

# Option A: Uneasy performs in an earlier slot than Xpert.
opt_a = (U < X)

# Option B: Wellspring performs in an earlier slot than Zircon.
opt_b = (W < Z)

# Option C: Xpert performs in an earlier slot than Uneasy.
opt_c = (X < U)

# Option D: Yardsign performs in an earlier slot than Wellspring.
opt_d = (Y < W)

# Option E: Zircon performs in an earlier slot than Uneasy.
opt_e = (Z < U)

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