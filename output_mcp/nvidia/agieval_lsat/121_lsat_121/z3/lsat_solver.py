from z3 import *

solver = Solver()

# Declare variables
u = Int('Uneasy')
v = Int('Vegemite')
w = Int('Wellspring')
x = Int('Xpert')
y = Int('Yardsign')
z = Int('Zircon')

# All different
solver.add(Distinct([u, v, w, x, y, z]))

# Domain 1-6
for var in [u, v, w, x, y, z]:
    solver.add(var >= 1, var <= 6)

# Constraints
solver.add(v < z)  # Vegemite earlier than Zircon
solver.add(w < x)  # Wellspring earlier than Xpert
solver.add(z < x)  # Zircon earlier than Xpert
solver.add(Or(u == 4, u == 5, u == 6))  # Uneasy in last three
solver.add(Or(y == 1, y == 2, y == 3))  # Yardsign in first three
solver.add(w + 1 == x)  # Wellspring immediately before Xpert

# Option constraints
opt_a_constr = (u == 5)
opt_b_constr = (v == 3)
opt_c_constr = (w == 3)
opt_d_constr = (z == 2)
opt_e_constr = (z == 4)

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