from z3 import *

# Buildings and their classes
# Garza Tower: class 1, Yates House: class 3, Zimmer House: class 3
# Flores Tower: class 1, Lynch Building: class 2
# King Building: class 2, Meyer Building: class 2, Ortiz Building: class 2

# We model this using the invariant approach.
# Each trade preserves the total "value" where class 1 = 4, class 2 = 2, class 3 = 1 (ratio 4:2:1)
# because 1 class 1 = 2 class 2 (so class1:class2 = 2:1) and 1 class 2 = 2 class 3 (so class2:class3 = 2:1)
# Therefore class1:class2:class3 = 4:2:1

# Initial value per company:
# RealProp: Garza(4) + Yates(1) + Zimmer(1) = 6
# Southco: Flores(4) + Lynch(2) = 6
# Trustcorp: King(2) + Meyer(2) + Ortiz(2) = 6

# Each company always has exactly 6 points.
# Also, the total number of buildings of each class is conserved.

# Let's model the final ownership of each building.
# Companies: 0=RealProp, 1=Southco, 2=Trustcorp

solver = Solver()

# Variables: which company owns each building
G = Int('G')  # Garza Tower (class 1)
Y = Int('Y')  # Yates House (class 3)
Z = Int('Z')  # Zimmer House (class 3)
F = Int('F')  # Flores Tower (class 1)
L = Int('L')  # Lynch Building (class 2)
K = Int('K')  # King Building (class 2)
M = Int('M')  # Meyer Building (class 2)
O = Int('O')  # Ortiz Building (class 2)

buildings = [G, Y, Z, F, L, K, M, O]

# Each building is owned by exactly one company (0, 1, or 2)
for b in buildings:
    solver.add(Or([b == c for c in [0, 1, 2]]))

# Class values for point calculation
# Class 1 = 4, Class 2 = 2, Class 3 = 1
# Each company must have exactly 6 points
# RealProp (company 0): Garza(4 if owned), Yates(1), Zimmer(1) + any others
# Southco (company 1): Flores(4), Lynch(2) + any others
# Trustcorp (company 2): King(2), Meyer(2), Ortiz(2) + any others

# Point values for each building
# G(class 1): 4, F(class 1): 4
# L(class 2): 2, K(class 2): 2, M(class 2): 2, O(class 2): 2
# Y(class 3): 1, Z(class 3): 1

def owned_by_company(var, company):
    return var == company

# Total points for each company must be 6
# RealProp (company 0)
realprop_points = Sum([
    If(G == 0, 4, 0),
    If(F == 0, 4, 0),
    If(L == 0, 2, 0),
    If(K == 0, 2, 0),
    If(M == 0, 2, 0),
    If(O == 0, 2, 0),
    If(Y == 0, 1, 0),
    If(Z == 0, 1, 0)
])
solver.add(realprop_points == 6)

# Southco (company 1)
southco_points = Sum([
    If(G == 1, 4, 0),
    If(F == 1, 4, 0),
    If(L == 1, 2, 0),
    If(K == 1, 2, 0),
    If(M == 1, 2, 0),
    If(O == 1, 2, 0),
    If(Y == 1, 1, 0),
    If(Z == 1, 1, 0)
])
solver.add(southco_points == 6)

# Trustcorp (company 2)
trustcorp_points = Sum([
    If(G == 2, 4, 0),
    If(F == 2, 4, 0),
    If(L == 2, 2, 0),
    If(K == 2, 2, 0),
    If(M == 2, 2, 0),
    If(O == 2, 2, 0),
    If(Y == 2, 1, 0),
    If(Z == 2, 1, 0)
])
solver.add(trustcorp_points == 6)

# Also need to ensure total counts of each class are preserved
# Initially: 2 class 1 buildings, 4 class 2 buildings, 2 class 3 buildings
# This is automatically satisfied since each building has a fixed class.

# Now check each option
# Option A: RealProp owns Flores Tower and Garza Tower
opt_a = And(F == 0, G == 0)

# Option B: Southco owns Flores Tower and Meyer Building
opt_b = And(F == 1, M == 1)

# Option C: Southco owns Garza Tower and Lynch Building
opt_c = And(G == 1, L == 1)

# Option D: Trustcorp owns Flores Tower and Ortiz Building
opt_d = And(F == 2, O == 2)

# Option E: Trustcorp owns Garza Tower and Meyer Building
opt_e = And(G == 2, M == 2)

found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
        m = solver.model()
        print(f"Option {letter} is SAT. Model:")
        print(f"  G={m[G]}, F={m[F]}, L={m[L]}, K={m[K]}, M={m[M]}, O={m[O]}, Y={m[Y]}, Z={m[Z]}")
    else:
        print(f"Option {letter} is UNSAT")
    solver.pop()

print()
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")