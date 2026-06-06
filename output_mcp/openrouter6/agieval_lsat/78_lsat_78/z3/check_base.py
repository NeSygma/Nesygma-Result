from z3 import *

solver = Solver()

# Declare variables for each business's space (1-7)
O = Int('Optometrist')
P = Int('Pharmacy')
R1 = Int('Restaurant1')
R2 = Int('Restaurant2')
S = Int('ShoeStore')
T = Int('ToyStore')
V = Int('Veterinarian')

# Base constraints
# All spaces are distinct
solver.add(Distinct([O, P, R1, R2, S, T, V]))
# Veterinarian is in space 5
solver.add(V == 5)

# Pharmacy at one end, restaurant at the other end
solver.add(Or(P == 1, P == 7))
solver.add(Or(
    And(P == 1, Or(R1 == 7, R2 == 7)),
    And(P == 7, Or(R1 == 1, R2 == 1))
))

# Two restaurants separated by at least two other businesses
solver.add(Abs(R1 - R2) >= 3)

# Pharmacy next to optometrist or veterinarian
solver.add(Or(
    Abs(P - O) == 1,
    Abs(P - V) == 1
))

# Toy store not next to veterinarian
solver.add(Abs(T - V) != 1)

result = solver.check()
print("Base constraints satisfiability:", result)
if result == sat:
    m = solver.model()
    print("Example model:")
    print("Optometrist:", m[O])
    print("Pharmacy:", m[P])
    print("Restaurant1:", m[R1])
    print("Restaurant2:", m[R2])
    print("ShoeStore:", m[S])
    print("ToyStore:", m[T])
    print("Veterinarian:", m[V])
else:
    print("No solution exists.")