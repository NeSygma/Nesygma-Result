from z3 import *

# Bands: Uneasy, Vegemite, Wellspring, Xpert, Yardsign, Zircon
# Slots: 1-6

U = Int('U')  # Uneasy
V = Int('V')  # Vegemite
W = Int('W')  # Wellspring
X = Int('X')  # Xpert
Y = Int('Y')  # Yardsign
Z = Int('Z')  # Zircon

bands = [U, V, W, X, Y, Z]

def make_base():
    s = Solver()
    for b in bands:
        s.add(b >= 1, b <= 6)
    s.add(Distinct(bands))
    s.add(V < Z)          # Vegemite earlier than Zircon
    s.add(W < X)          # Wellspring earlier than Xpert
    s.add(Z < X)          # Zircon earlier than Xpert
    s.add(U >= 4)         # Uneasy in last three slots
    s.add(Y <= 3)         # Yardsign in first three slots
    s.add(Z + 1 == W)     # Zircon immediately before Wellspring
    return s

# To find what MUST be true, check if negation of each option is unsat
options = {
    "A": (U == 5),
    "B": (V == 1),
    "C": (X == 5),
    "D": (Y == 2),
    "E": (Z == 3),
}

must_be_true = []
for letter, prop in options.items():
    s = make_base()
    s.add(Not(prop))
    if s.check() == unsat:
        must_be_true.append(letter)

print(f"Options that MUST be true: {must_be_true}")

if len(must_be_true) == 1:
    print("STATUS: sat")
    print(f"answer:{must_be_true[0]}")
elif len(must_be_true) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple must-be-true options {must_be_true}")
else:
    print("STATUS: unsat")
    print("Refine: No must-be-true options found")