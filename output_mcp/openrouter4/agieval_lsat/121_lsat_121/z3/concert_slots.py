from z3 import *

solver = Solver()

# Variables for each band's slot (1-indexed)
U, V, W, X, Y, Z = Ints('U V W X Y Z')

# Each slot is between 1 and 6
for var in [U, V, W, X, Y, Z]:
    solver.add(var >= 1, var <= 6)

# All distinct slots
solver.add(Distinct(U, V, W, X, Y, Z))

# Constraint: Vegemite earlier than Zircon
solver.add(V < Z)

# Constraint: Wellspring and Zircon earlier than Xpert
solver.add(W < X)
solver.add(Z < X)

# Constraint: Uneasy in one of the last three slots (4,5,6)
solver.add(U >= 4)

# Constraint: Yardsign in one of the first three slots (1,2,3)
solver.add(Y <= 3)

# Additional condition: Wellspring immediately before Xpert
solver.add(W + 1 == X)

# Now test each option
options = [
    ("A", U == 5),      # Uneasy in slot five
    ("B", V == 3),      # Vegemite in slot three
    ("C", W == 3),      # Wellspring in slot three
    ("D", Z == 2),      # Zircon in slot two
    ("E", Z == 4)       # Zircon in slot four
]

found_options = []
for letter, constr in options:
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