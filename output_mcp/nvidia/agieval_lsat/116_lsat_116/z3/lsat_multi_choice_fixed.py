from z3 import *

solver = Solver()

# Declare slot variables
U = Int('U')
V = Int('V')
W = Int('W')
X = Int('X')
Y = Int('Y')
Z = Int('Z')

# All different
solver.add(Distinct([U, V, W, X, Y, Z]))

# Ordering constraints
solver.add(V < Z)  # Vegemite earlier than Zircon
solver.add(W < X)  # Wellspring earlier than Xpert
solver.add(Z < X)  # Zircon earlier than Xpert

# Domain constraints: each slot is 1..6
solver.add(U >= 1, U <= 6)
solver.add(V >= 1, V <= 6)
solver.add(W >= 1, W <= 6)
solver.add(X >= 1, X <= 6)
solver.add(Y >= 1, Y <= 6)
solver.add(Z >= 1, Z <= 6)

# Additional constraints: Uneasy in last three slots (4-6), Yardsign in first three slots (1-3)
solver.add(U >= 4, U <= 6)
solver.add(Y >= 1, Y <= 3)

# Option constraints
opt_a_constr = (U == 5)  # Uneasy in slot five
opt_b_constr = (V == 5)  # Vegemite in slot five
opt_c_constr = (W == 5)  # Wellspring in slot five
opt_d_constr = (X == 5)  # Xpert in slot five
opt_e_constr = (Z == 5)  # Zircon in slot five

found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
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