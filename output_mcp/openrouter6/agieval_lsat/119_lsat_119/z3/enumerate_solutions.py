from z3 import *

# Define variables
U, V, W, X, Y, Z = Ints('U V W X Y Z')

solver = Solver()

# All variables between 1 and 6
solver.add(U >= 1, U <= 6)
solver.add(V >= 1, V <= 6)
solver.add(W >= 1, W <= 6)
solver.add(X >= 1, X <= 6)
solver.add(Y >= 1, Y <= 6)
solver.add(Z >= 1, Z <= 6)

# All distinct
solver.add(Distinct([U, V, W, X, Y, Z]))

# Constraints
solver.add(V < Z)                     # Vegemite before Zircon
solver.add(W < X)                     # Wellspring before Xpert
solver.add(Z < X)                     # Zircon before Xpert
solver.add(Or([U == 4, U == 5, U == 6]))  # Uneasy in last three slots
solver.add(Or([Y == 1, Y == 2, Y == 3]))  # Yardsign in first three slots

# Additional condition: Zircon immediately before Wellspring
solver.add(Z == W - 1)

# Enumerate all solutions
solutions = []
while solver.check() == sat:
    m = solver.model()
    sol = (m[U], m[V], m[W], m[X], m[Y], m[Z])
    solutions.append(sol)
    # Block this solution
    solver.add(Or([U != m[U], V != m[V], W != m[W], X != m[X], Y != m[Y], Z != m[Z]]))

print(f"Total solutions: {len(solutions)}")
for sol in solutions:
    print(f"U={sol[0]}, V={sol[1]}, W={sol[2]}, X={sol[3]}, Y={sol[4]}, Z={sol[5]}")

# Check which options are true in all solutions
all_A = all(sol[0] == 5 for sol in solutions)  # Uneasy in slot 5
all_B = all(sol[1] == 1 for sol in solutions)  # Vegemite in slot 1
all_C = all(sol[3] == 5 for sol in solutions)  # Xpert in slot 5
all_D = all(sol[4] == 2 for sol in solutions)  # Yardsign in slot 2
all_E = all(sol[5] == 3 for sol in solutions)  # Zircon in slot 3

print("\nOptions that are always true:")
if all_A: print("A: Uneasy performs in slot five.")
if all_B: print("B: Vegemite performs in slot one.")
if all_C: print("C: Xpert performs in slot five.")
if all_D: print("D: Yardsign performs in slot two.")
if all_E: print("E: Zircon performs in slot three.")