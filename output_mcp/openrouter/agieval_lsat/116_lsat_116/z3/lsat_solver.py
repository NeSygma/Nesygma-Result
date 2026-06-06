from z3 import *

# Base constraints
slots = range(1, 7)  # 1..6
bands = ['U', 'V', 'W', 'X', 'Y', 'Z']  # Uneasy, Vegemite, Wellspring, Xpert, Yardsign, Zircon
# Create an Int variable for each band representing its slot
U = Int('U')
V = Int('V')
W = Int('W')
X = Int('X')
Y = Int('Y')
Z = Int('Z')

solver = Solver()
# each band in 1..6
for var in [U, V, W, X, Y, Z]:
    solver.add(var >= 1, var <= 6)
# all different
solver.add(Distinct(U, V, W, X, Y, Z))
# constraints
solver.add(V < Z)          # Vegemite earlier than Zircon
solver.add(W < X)          # Wellspring earlier than Xpert
solver.add(Z < X)          # Zircon earlier than Xpert
solver.add(Or(U == 4, U == 5, U == 6))  # Uneasy in last three slots
solver.add(Or(Y == 1, Y == 2, Y == 3))  # Yardsign in first three slots

# Options mapping
options = {
    'A': U,  # Uneasy
    'B': V,  # Vegemite
    'C': W,  # Wellspring
    'D': X,  # Xpert
    'E': Z   # Zircon
}

found_options = []
for letter, var in options.items():
    solver.push()
    solver.add(var == 5)  # assume this band is in slot five
    if solver.check() == sat:
        found_options.append(letter)
    solver.pop()

all_letters = set(options.keys())
possible = set(found_options)
impossible = all_letters - possible
if len(impossible) == 1:
    ans = impossible.pop()
    print("STATUS: sat")
    print(f"answer:{ans}")
elif len(possible) == 1:
    # fallback if only one possible (unlikely for this problem)
    ans = possible.pop()
    print("STATUS: sat")
    print(f"answer:{ans}")
else:
    print("STATUS: unsat")
    print(f"Refine: possible options {sorted(possible)}, impossible options {sorted(impossible)}")