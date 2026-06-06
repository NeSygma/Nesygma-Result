from z3 import *

solver = Solver()

# Declare variables for each band's slot
U = Int('U')  # Uneasy
V = Int('V')  # Vegemite
W = Int('W')  # Wellspring
X = Int('X')  # Xpert
Y = Int('Y')  # Yardsign
Z = Int('Z')  # Zircon

# Base constraints
# All slots are between 1 and 6
solver.add(1 <= U, U <= 6)
solver.add(1 <= V, V <= 6)
solver.add(1 <= W, W <= 6)
solver.add(1 <= X, X <= 6)
solver.add(1 <= Y, Y <= 6)
solver.add(1 <= Z, Z <= 6)

# All bands in distinct slots
solver.add(Distinct([U, V, W, X, Y, Z]))

# Vegemite earlier than Zircon
solver.add(V < Z)

# Wellspring and Zircon earlier than Xpert
solver.add(W < X)
solver.add(Z < X)

# Uneasy in last three slots (4,5,6)
solver.add(U >= 4)

# Yardsign in first three slots (1,2,3)
solver.add(Y <= 3)

# Additional condition: Wellspring immediately before Xpert
solver.add(W + 1 == X)

# Now test each answer choice
found_options = []

# Option A: Uneasy performs in slot five
opt_a = (U == 5)
solver.push()
solver.add(opt_a)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: Vegemite performs in slot three
opt_b = (V == 3)
solver.push()
solver.add(opt_b)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: Wellspring performs in slot three
opt_c = (W == 3)
solver.push()
solver.add(opt_c)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: Zircon performs in slot two
opt_d = (Z == 2)
solver.push()
solver.add(opt_d)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: Zircon performs in slot four
opt_e = (Z == 4)
solver.push()
solver.add(opt_e)
if solver.check() == sat:
    found_options.append("E")
solver.pop()

# Output according to the required skeleton
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")