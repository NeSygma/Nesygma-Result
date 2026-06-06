from z3 import *

solver = Solver()

# Declare variables for slot numbers
U = Int('U')  # Uneasy
V = Int('V')  # Vegemite
W = Int('W')  # Wellspring
X = Int('X')  # Xpert
Y = Int('Y')  # Yardsign
Z = Int('Z')  # Zircon

# Domain constraints: slots 1 to 6
solver.add(U >= 1, U <= 6)
solver.add(V >= 1, V <= 6)
solver.add(W >= 1, W <= 6)
solver.add(X >= 1, X <= 6)
solver.add(Y >= 1, Y <= 6)
solver.add(Z >= 1, Z <= 6)

# All slots distinct
solver.add(Distinct([U, V, W, X, Y, Z]))

# Given: Vegemite performs in slot three
solver.add(V == 3)

# Constraint: Vegemite earlier than Zircon
solver.add(V < Z)

# Constraint: Wellspring and Zircon each earlier than Xpert
solver.add(W < X)
solver.add(Z < X)

# Constraint: Uneasy in last three slots (4,5,6)
solver.add(Or(U == 4, U == 5, U == 6))

# Constraint: Yardsign in first three slots (1,2,3) but slot 3 is taken by Vegemite
solver.add(Or(Y == 1, Y == 2))

# Define options as boolean expressions
opt_a = U < X
opt_b = W < Z
opt_c = X < U
opt_d = Y < W
opt_e = Z < U

# Use the skeleton to evaluate which option must be true
# We check for each option if its negation is unsatisfiable
found_options = []
for letter, constr in [("A", Not(opt_a)), ("B", Not(opt_b)), ("C", Not(opt_c)), ("D", Not(opt_d)), ("E", Not(opt_e))]:
    solver.push()
    solver.add(constr)
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