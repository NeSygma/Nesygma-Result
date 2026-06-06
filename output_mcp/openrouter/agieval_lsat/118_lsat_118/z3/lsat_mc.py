from z3 import *

solver = Solver()
# Variables: slot numbers for each band (1..6)
U = Int('U')  # Uneasy
V = Int('V')  # Vegemite
W = Int('W')  # Wellspring
X = Int('X')  # Xpert
Y = Int('Y')  # Yardsign
Z = Int('Z')  # Zircon
bands = [U, V, W, X, Y, Z]
# Domain constraints
for b in bands:
    solver.add(b >= 1, b <= 6)
# All distinct
solver.add(Distinct(bands))
# Given constraints
solver.add(V < Z)          # Vegemite earlier than Zircon
solver.add(W < X)          # Wellspring earlier than Xpert
solver.add(Z < X)          # Zircon earlier than Xpert
solver.add(U >= 4)        # Uneasy in last three slots (4,5,6)
solver.add(Y <= 3)        # Yardsign in first three slots (1,2,3)
solver.add(V == 3)        # Vegemite in slot 3

# Define option expressions
opt_A = U < X          # Uneasy earlier than Xpert
opt_B = W < Z          # Wellspring earlier than Zircon
opt_C = X < U          # Xpert earlier than Uneasy
opt_D = Y < W          # Yardsign earlier than Wellspring
opt_E = Z < U          # Zircon earlier than Uneasy

options = [
    ("A", opt_A),
    ("B", opt_B),
    ("C", opt_C),
    ("D", opt_D),
    ("E", opt_E)
]

forced_options = []
for letter, opt in options:
    solver.push()
    # Add negation of the option; if unsat, then option must be true
    solver.add(Not(opt))
    if solver.check() == unsat:
        forced_options.append(letter)
    solver.pop()

if len(forced_options) == 1:
    print("STATUS: sat")
    print(f"answer:{forced_options[0]}")
elif len(forced_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple forced options found {forced_options}")
else:
    print("STATUS: unsat")
    print("Refine: No forced options found")