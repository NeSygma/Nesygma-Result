from z3 import *

solver = Solver()

# Slots 1-6, bands: Uneasy, Vegemite, Wellspring, Xpert, Yardsign, Zircon
U, V, W, X, Y, Z = Ints('U V W X Y Z')

bands = [U, V, W, X, Y, Z]
for b in bands:
    solver.add(b >= 1, b <= 6)
solver.add(Distinct(bands))

# Constraints:
solver.add(V < Z)  # Vegemite earlier than Zircon
solver.add(W < X)  # Wellspring earlier than Xpert
solver.add(Z < X)  # Zircon earlier than Xpert
solver.add(U >= 4) # Uneasy in last three slots
solver.add(Y <= 3) # Yardsign in first three slots

# Additional condition: Zircon earlier than Yardsign
solver.add(Z < Y)

# The question asks for the EARLIEST slot Wellspring could be in.
# Let's find the minimum possible value for W.
# We can use optimization, or we can test each slot from earliest to latest.

# Let's try to find the minimum W by checking if W can be 1, then 2, etc.
for slot in range(1, 7):
    solver.push()
    solver.add(W == slot)
    if solver.check() == sat:
        m = solver.model()
        print(f"W can be slot {slot}")
        print(f"  U={m[U]}, V={m[V]}, W={m[W]}, X={m[X]}, Y={m[Y]}, Z={m[Z]}")
        solver.pop()
        break
    solver.pop()

# Now let's also check each option systematically
found_options = []
for letter, constr in [("A", W == 2), ("B", W == 3), ("C", W == 4), ("D", W == 5), ("E", W == 6)]:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
    solver.pop()

print(f"Found options: {found_options}")

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    # Multiple options found - we need the earliest one
    # The earliest slot among the found options
    slot_map = {"A": 2, "B": 3, "C": 4, "D": 5, "E": 6}
    earliest = min(found_options, key=lambda x: slot_map[x])
    print("STATUS: sat")
    print(f"answer:{earliest}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")