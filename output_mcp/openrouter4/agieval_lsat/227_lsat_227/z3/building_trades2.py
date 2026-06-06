from z3 import *

# Buildings and their classes
# Garza Tower: class 1, Yates House: class 3, Zimmer House: class 3
# Flores Tower: class 1, Lynch Building: class 2
# King Building: class 2, Meyer Building: class 2, Ortiz Building: class 2

# Each trade preserves total value where class1:class2:class3 = 4:2:1
# because 1 class1 = 2 class2 and 1 class2 = 2 class3
# So class1=4, class2=2, class3=1

# Initial value per company = 6 points each
# RealProp: Garza(4) + Yates(1) + Zimmer(1) = 6
# Southco: Flores(4) + Lynch(2) = 6
# Trustcorp: King(2) + Meyer(2) + Ortiz(2) = 6

# Each company always has exactly 6 points.

solver = Solver()

# Variables: which company owns each building (0=RealProp, 1=Southco, 2=Trustcorp)
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

# Point values: class1=4, class2=2, class3=1
# Each company must have exactly 6 points

# RealProp (company 0)
realprop_points = Sum([
    If(G == 0, 4, 0), If(F == 0, 4, 0),
    If(L == 0, 2, 0), If(K == 0, 2, 0), If(M == 0, 2, 0), If(O == 0, 2, 0),
    If(Y == 0, 1, 0), If(Z == 0, 1, 0)
])
solver.add(realprop_points == 6)

# Southco (company 1)
southco_points = Sum([
    If(G == 1, 4, 0), If(F == 1, 4, 0),
    If(L == 1, 2, 0), If(K == 1, 2, 0), If(M == 1, 2, 0), If(O == 1, 2, 0),
    If(Y == 1, 1, 0), If(Z == 1, 1, 0)
])
solver.add(southco_points == 6)

# Trustcorp (company 2)
trustcorp_points = Sum([
    If(G == 2, 4, 0), If(F == 2, 4, 0),
    If(L == 2, 2, 0), If(K == 2, 2, 0), If(M == 2, 2, 0), If(O == 2, 2, 0),
    If(Y == 2, 1, 0), If(Z == 2, 1, 0)
])
solver.add(trustcorp_points == 6)

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

# Find the option that CANNOT be true (i.e., is UNSAT)
unsat_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(constr)
    res = solver.check()
    if res == unsat:
        unsat_options.append(letter)
    # else: sat - it can be true
    solver.pop()

# Exactly one option should be impossible (UNSAT)
if len(unsat_options) == 1:
    print("STATUS: sat")
    print(f"answer:{unsat_options[0]}")
else:
    print("STATUS: unsat")
    print(f"Refine: Expected exactly 1 impossible option, found {unsat_options}")