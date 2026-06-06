from z3 import *

# Variables for slots (1-6)
V, W, X, Y, Z, U = Ints('V W X Y Z U')

def get_base_solver():
    solver = Solver()
    # All distinct, each in 1..6
    solver.add(Distinct(V, W, X, Y, Z, U))
    for var in [V, W, X, Y, Z, U]:
        solver.add(var >= 1, var <= 6)
    # Constraints
    solver.add(V < Z)          # Vegemite earlier than Zircon
    solver.add(W < X)          # Wellspring earlier than Xpert
    solver.add(Z < X)          # Zircon earlier than Xpert
    solver.add(U >= 4, U <= 6) # Uneasy in last three slots
    solver.add(Y >= 1, Y <= 3) # Yardsign in first three slots
    solver.add(Z < Y)          # Given: Zircon earlier than Yardsign
    return solver

# Check each option from earliest to latest.
# The first one that is satisfiable is the earliest possible slot.
found_options = []
slot_map = [("A", 2), ("B", 3), ("C", 4), ("D", 5), ("E", 6)]

for letter, slot in slot_map:
    solver = get_base_solver()
    solver.add(W == slot)
    if solver.check() == sat:
        found_options.append(letter)
        break  # earliest found

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")