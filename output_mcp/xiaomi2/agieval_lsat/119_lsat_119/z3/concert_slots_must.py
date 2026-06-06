from z3 import *

# Define base constraints
def add_base_constraints(solver):
    U = Int('U')  # Uneasy
    V = Int('V')  # Vegemite
    W = Int('W')  # Wellspring
    X = Int('X')  # Xpert
    Y = Int('Y')  # Yardsign
    Z = Int('Z')  # Zircon

    bands = [U, V, W, X, Y, Z]

    for b in bands:
        solver.add(b >= 1, b <= 6)

    solver.add(Distinct(bands))

    solver.add(V < Z)           # Vegemite earlier than Zircon
    solver.add(W < X)           # Wellspring earlier than Xpert
    solver.add(Z < X)           # Zircon earlier than Xpert
    solver.add(Or(U == 4, U == 5, U == 6))  # Uneasy in last three slots
    solver.add(Or(Y == 1, Y == 2, Y == 3))  # Yardsign in first three slots
    solver.add(Z + 1 == W)      # Zircon immediately before Wellspring

    return U, V, W, X, Y, Z

# For each option, try to find a model where the option is FALSE
# If UNSAT, the option MUST be true

options = {
    "A": "Uneasy performs in slot five",
    "B": "Vegemite performs in slot one",
    "C": "Xpert performs in slot five",
    "D": "Yardsign performs in slot two",
    "E": "Zircon performs in slot three"
}

neg_options = {
    "A": lambda U, V, W, X, Y, Z: U != 5,
    "B": lambda U, V, W, X, Y, Z: V != 1,
    "C": lambda U, V, W, X, Y, Z: X != 5,
    "D": lambda U, V, W, X, Y, Z: Y != 2,
    "E": lambda U, V, W, X, Y, Z: Z != 3,
}

must_be_true = []

for letter in ["A", "B", "C", "D", "E"]:
    s = Solver()
    U, V, W, X, Y, Z = add_base_constraints(s)
    s.add(neg_options[letter](U, V, W, X, Y, Z))
    result = s.check()
    if result == unsat:
        must_be_true.append(letter)
        print(f"Option {letter}: MUST BE TRUE (negation is UNSAT)")
    elif result == sat:
        m = s.model()
        print(f"Option {letter}: NOT necessarily true (counterexample: U={m[U]}, V={m[V]}, W={m[W]}, X={m[X]}, Y={m[Y]}, Z={m[Z]})")
    else:
        print(f"Option {letter}: UNKNOWN")

print()
if len(must_be_true) == 1:
    print("STATUS: sat")
    print(f"answer:{must_be_true[0]}")
elif len(must_be_true) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple must-be-true options found {must_be_true}")
else:
    print("STATUS: unsat")
    print("Refine: No must-be-true options found")