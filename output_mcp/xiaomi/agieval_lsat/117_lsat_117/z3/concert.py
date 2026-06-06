from z3 import *

solver = Solver()

# Bands: Uneasy, Vegemite, Wellspring, Xpert, Yardsign, Zircon
# Slots: 1-6 (earliest to latest)

U = Int('U')  # Uneasy
V = Int('V')  # Vegemite
W = Int('W')  # Wellspring
X = Int('X')  # Xpert
Y = Int('Y')  # Yardsign
Z = Int('Z')  # Zircon

bands = [U, V, W, X, Y, Z]

# Each band in a slot 1-6
for b in bands:
    solver.add(b >= 1, b <= 6)

# All different slots
solver.add(Distinct(bands))

# Vegemite performs in an earlier slot than Zircon
solver.add(V < Z)

# Wellspring and Zircon each perform in an earlier slot than Xpert
solver.add(W < X)
solver.add(Z < X)

# Uneasy performs in one of the last three slots (4, 5, or 6)
solver.add(Or(U == 4, U == 5, U == 6))

# Yardsign performs in one of the first three slots (1, 2, or 3)
solver.add(Or(Y == 1, Y == 2, Y == 3))

# Additional constraint: Zircon performs in an earlier slot than Yardsign
solver.add(Z < Y)

# Question: What is the earliest slot in which Wellspring could perform?
# We want to minimize W, so check each option from earliest to latest

found_options = []

# Option A: Wellspring in slot 2 (earliest possible is 1, but check 2 first per options)
# Actually, let's check if W can be 1 first, then check each option
# The options are: (A) two, (B) three, (C) four, (D) five, (E) six
# We need to find the earliest slot W could be in

# Let's check each option: can W be in that slot?
for letter, slot in [("A", 2), ("B", 3), ("C", 4), ("D", 5), ("E", 6)]:
    solver.push()
    solver.add(W == slot)
    if solver.check() == sat:
        found_options.append(letter)
    solver.pop()

# Also check if W can be in slot 1 (not an option but useful for understanding)
solver.push()
solver.add(W == 1)
can_be_1 = solver.check() == sat
solver.pop()

if can_be_1:
    # W can be in slot 1, but that's not an option. The earliest option is A (slot 2)
    # Since W can be 1, it can certainly be 2, so A should be valid
    pass

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    # Multiple options are possible - we need the EARLIEST
    # The question asks for the earliest slot W COULD perform in
    # So we pick the earliest among the valid options
    earliest = found_options[0]  # Already ordered A, B, C, D, E
    print("STATUS: sat")
    print(f"answer:{earliest}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")