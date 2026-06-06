from z3 import *

# Define variables for each band
U = Int('U')  # Uneasy
V = Int('V')  # Vegemite
W = Int('W')  # Wellspring
X = Int('X')  # Xpert
Y = Int('Y')  # Yardsign
Z = Int('Z')  # Zircon

bands = [U, V, W, X, Y, Z]

# Base constraints
base = []
# Slots are 1..6
for b in bands:
    base.append(And(b >= 1, b <= 6))
# All distinct
base.append(Distinct(bands))
# Given ordering constraints
base.append(V < Z)          # Vegemite earlier than Zircon
base.append(W < X)          # Wellspring earlier than Xpert
base.append(Z < X)          # Zircon earlier than Xpert
base.append(Or(U == 4, U == 5, U == 6))  # Uneasy in last three slots
base.append(Or(Y == 1, Y == 2, Y == 3))  # Yardsign in first three slots
# Additional condition for the question: Zircon earlier than Yardsign
base.append(Z < Y)

# First, compute the earliest possible slot for Wellspring using Optimize
opt = Optimize()
opt.add(base)
opt.minimize(W)
if opt.check() == sat:
    minW = opt.model()[W].as_long()
else:
    # Should not happen in benchmark mode
    print("STATUS: unsat")
    exit()

# Now evaluate each multiple-choice option using the required skeleton
solver = Solver()
solver.add(base)

options = [
    ("A", 2),
    ("B", 3),
    ("C", 4),
    ("D", 5),
    ("E", 6)
]

found_options = []
for letter, slot_val in options:
    solver.push()
    # Constrain Wellspring to this slot and also enforce it equals the minimal slot found
    solver.add(W == slot_val)
    solver.add(W == minW)
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