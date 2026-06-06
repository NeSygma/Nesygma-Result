from z3 import *

# Historians: F, G, H, J
# Topics: L, O, S, W
# Time slots: 1, 2, 3, 4

# Variables: Time of each historian and each topic
F, G, H, J = Ints('F G H J')
L, O, S, W = Ints('L O S W')

solver = Solver()

# Domain constraints
for var in [F, G, H, J, L, O, S, W]:
    solver.add(var >= 1, var <= 4)

# Distinctness
solver.add(Distinct(F, G, H, J))
solver.add(Distinct(L, O, S, W))

# Constraints
# 1. The oil paintings lecture and the watercolors lecture must both be earlier than the lithographs lecture.
solver.add(O < L)
solver.add(W < L)

# 2. Farley's lecture must be earlier than the oil paintings lecture.
solver.add(F < O)

# 3. Holden's lecture must be earlier than both Garcia's lecture and Jiang's lecture.
solver.add(H < G)
solver.add(H < J)

# Test each option
options = [
    ("A", F == L),
    ("B", G == S),
    ("C", G == W),
    ("D", H == O),
    ("E", J == W)
]

found_options = []
for letter, constr in options:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        # This option is possible, so it is NOT the answer to "CANNOT be true"
        pass
    else:
        # This option is impossible, so it IS the answer to "CANNOT be true"
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