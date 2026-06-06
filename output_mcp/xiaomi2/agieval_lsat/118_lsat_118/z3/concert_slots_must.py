from z3 import *

solver = Solver()

# Bands: Uneasy, Vegemite, Wellspring, Xpert, Yardsign, Zircon
U, V, W, X, Y, Z = Ints('U V W X Y Z')
bands = [U, V, W, X, Y, Z]

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
options = [
    ("A", U < X),   # Uneasy earlier than Xpert
    ("B", W < Z),   # Wellspring earlier than Zircon
    ("C", X < U),   # Xpert earlier than Uneasy
    ("D", Y < W),   # Yardsign earlier than Wellspring
    ("E", Z < U),   # Zircon earlier than Uneasy
]

# For "must be true" questions: check if negation is UNSAT
must_be_true = []
for letter, constr in options:
    s = Solver()
    # Add all base constraints
    for b in bands:
        s.add(b >= 1, b <= 6)
    s.add(Distinct(bands))
    s.add(V < Z)
    s.add(W < X)
    s.add(Z < X)
    s.add(U >= 4)
    s.add(Y <= 3)
    s.add(V == 3)
    # Add negation of the option
    s.add(Not(constr))
    if s.check() == unsat:
        must_be_true.append(letter)

if len(must_be_true) == 1:
    print("STATUS: sat")
    print(f"answer:{must_be_true[0]}")
elif len(must_be_true) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple must-be-true options found {must_be_true}")
else:
    print("STATUS: unsat")
    print("Refine: No must-be-true options found")