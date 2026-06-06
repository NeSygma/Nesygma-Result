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

# Let's first check if the base constraints are satisfiable
print("Base check:", solver.check())
if solver.check() == sat:
    m = solver.model()
    print(f"U={m[U]}, V={m[V]}, W={m[W]}, X={m[X]}, Y={m[Y]}, Z={m[Z]}")

# Now evaluate each option using the required skeleton
# But first, let's understand what MUST be true - we need to check if an option is NECESSARILY true
# i.e., it holds in ALL valid models. So we check if NOT(option) is unsatisfiable.

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
    # To check if something MUST be true, we check if its negation is UNSAT
    solver.add(Not(constr))
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