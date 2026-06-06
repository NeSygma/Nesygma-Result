from z3 import *

# Slots 1-6, bands: Uneasy, Vegemite, Wellspring, Xpert, Yardsign, Zircon
# We'll use integer variables for each band's slot position (1-6)
U, V, W, X, Y, Z = Ints('U V W X Y Z')
bands = [U, V, W, X, Y, Z]

solver = Solver()

# Each band in a distinct slot 1-6
for b in bands:
    solver.add(b >= 1, b <= 6)
solver.add(Distinct(bands))

# Constraints:
# 1. Vegemite earlier than Zircon: V < Z
solver.add(V < Z)

# 2. Wellspring and Zircon each earlier than Xpert: W < X, Z < X
solver.add(W < X)
solver.add(Z < X)

# 3. Uneasy in one of the last three slots: U in {4,5,6}
solver.add(Or([U == i for i in [4,5,6]]))

# 4. Yardsign in one of the first three slots: Y in {1,2,3}
solver.add(Or([Y == i for i in [1,2,3]]))

# Now test each option: "X CANNOT be the band that performs in slot five"
# We test: can the band be in slot 5? If sat, it's possible (so NOT the answer).
# If unsat, it's impossible (so it IS the answer).

found_options = []

# Option A: Uneasy in slot 5
solver.push()
solver.add(U == 5)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: Vegemite in slot 5
solver.push()
solver.add(V == 5)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: Wellspring in slot 5
solver.push()
solver.add(W == 5)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: Xpert in slot 5
solver.push()
solver.add(X == 5)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: Zircon in slot 5
solver.push()
solver.add(Z == 5)
if solver.check() == sat:
    found_options.append("E")
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