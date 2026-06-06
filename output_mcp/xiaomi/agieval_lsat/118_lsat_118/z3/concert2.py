from z3 import *

solver = Solver()

# Bands: Uneasy, Vegemite, Wellspring, Xpert, Yardsign, Zircon
# Slots: 1-6 (Int)
U, V, W, X, Y, Z = Ints('U V W X Y Z')
bands = [U, V, W, X, Y, Z]

# Each band in a unique slot 1-6
for b in bands:
    solver.add(b >= 1, b <= 6)
solver.add(Distinct(bands))

# Constraints
solver.add(V < Z)  # Vegemite earlier than Zircon
solver.add(W < X)  # Wellspring earlier than Xpert
solver.add(Z < X)  # Zircon earlier than Xpert
solver.add(Or(U == 4, U == 5, U == 6))  # Uneasy in last three
solver.add(Or(Y == 1, Y == 2, Y == 3))  # Yardsign in first three

# Additional constraint: Vegemite performs in slot 3
solver.add(V == 3)

# Define option constraints
# (A) Uneasy performs in an earlier slot than Xpert
opt_a = (U < X)
# (B) Wellspring performs in an earlier slot than Zircon
opt_b = (W < Z)
# (C) Xpert performs in an earlier slot than Uneasy
opt_c = (X < U)
# (D) Yardsign performs in an earlier slot than Wellspring
opt_d = (Y < W)
# (E) Zircon performs in an earlier slot than Uneasy
opt_e = (Z < U)

# Check which options MUST be true (i.e., are entailed by the constraints)
# An option must be true if its negation is unsatisfiable
must_be_true = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(Not(constr))
    if solver.check() == unsat:
        must_be_true.append(letter)
    solver.pop()

if len(must_be_true) == 1:
    print("STATUS: sat")
    print(f"answer:{must_be_true[0]}")
elif len(must_be_true) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options must be true {must_be_true}")
else:
    print("STATUS: unsat")
    print("Refine: No options must be true")