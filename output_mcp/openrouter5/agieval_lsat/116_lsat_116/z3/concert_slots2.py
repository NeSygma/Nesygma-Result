from z3 import *

# Slots 1-6, bands: Uneasy, Vegemite, Wellspring, Xpert, Yardsign, Zircon
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

# Let's first see what valid assignments exist to understand the constraints better
print("Checking all valid assignments...")
solutions = []
while solver.check() == sat:
    m = solver.model()
    sol = {b: m.eval(b, model_completion=True).as_long() for b in bands}
    solutions.append(sol)
    solver.add(Or([b != m.eval(b, model_completion=True).as_long() for b in bands]))

print(f"Total valid assignments: {len(solutions)}")
for s in solutions:
    # Create a list of (band_name, slot) sorted by slot
    slot_map = {s[U]: "U", s[V]: "V", s[W]: "W", s[X]: "X", s[Y]: "Y", s[Z]: "Z"}
    order = [slot_map[i] for i in range(1, 7)]
    print(f"  Slots 1-6: {order}")

# Now let's think about which band CANNOT be in slot 5.
# Let's check each option more carefully.

# Reset solver
solver2 = Solver()
for b in bands:
    solver2.add(b >= 1, b <= 6)
solver2.add(Distinct(bands))
solver2.add(V < Z)
solver2.add(W < X)
solver2.add(Z < X)
solver2.add(Or([U == i for i in [4,5,6]]))
solver2.add(Or([Y == i for i in [1,2,3]]))

found_options = []

# Option A: Uneasy in slot 5
solver2.push()
solver2.add(U == 5)
if solver2.check() == sat:
    m = solver2.model()
    print(f"\nA (U=5) is SAT. Example: U={m[U]}, V={m[V]}, W={m[W]}, X={m[X]}, Y={m[Y]}, Z={m[Z]}")
    found_options.append("A")
else:
    print(f"\nA (U=5) is UNSAT")
solver2.pop()

# Option B: Vegemite in slot 5
solver2.push()
solver2.add(V == 5)
if solver2.check() == sat:
    m = solver2.model()
    print(f"B (V=5) is SAT. Example: U={m[U]}, V={m[V]}, W={m[W]}, X={m[X]}, Y={m[Y]}, Z={m[Z]}")
    found_options.append("B")
else:
    print(f"B (V=5) is UNSAT")
solver2.pop()

# Option C: Wellspring in slot 5
solver2.push()
solver2.add(W == 5)
if solver2.check() == sat:
    m = solver2.model()
    print(f"C (W=5) is SAT. Example: U={m[U]}, V={m[V]}, W={m[W]}, X={m[X]}, Y={m[Y]}, Z={m[Z]}")
    found_options.append("C")
else:
    print(f"C (W=5) is UNSAT")
solver2.pop()

# Option D: Xpert in slot 5
solver2.push()
solver2.add(X == 5)
if solver2.check() == sat:
    m = solver2.model()
    print(f"D (X=5) is SAT. Example: U={m[U]}, V={m[V]}, W={m[W]}, X={m[X]}, Y={m[Y]}, Z={m[Z]}")
    found_options.append("D")
else:
    print(f"D (X=5) is UNSAT")
solver2.pop()

# Option E: Zircon in slot 5
solver2.push()
solver2.add(Z == 5)
if solver2.check() == sat:
    m = solver2.model()
    print(f"E (Z=5) is SAT. Example: U={m[U]}, V={m[V]}, W={m[W]}, X={m[X]}, Y={m[Y]}, Z={m[Z]}")
    found_options.append("E")
else:
    print(f"E (Z=5) is UNSAT")
solver2.pop()

print(f"\nFound options: {found_options}")

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")