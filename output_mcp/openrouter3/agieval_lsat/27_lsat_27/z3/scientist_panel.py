from z3 import *

solver = Solver()

# Declare boolean variables for each scientist
F, G, H = Bools('F G H')  # botanists
K, L, M = Bools('K L M')  # chemists
P, Q, R = Bools('P Q R')  # zoologists

# Base constraints
# 1. Panel must have exactly 5 scientists
solver.add(Sum([If(s, 1, 0) for s in [F, G, H, K, L, M, P, Q, R]]) == 5)

# 2. At least one of each type
solver.add(Or(F, G, H))  # at least one botanist
solver.add(Or(K, L, M))  # at least one chemist
solver.add(Or(P, Q, R))  # at least one zoologist

# 3. If more than one botanist, then at most one zoologist
# More than one botanist: (F and G) or (F and H) or (G and H) or all three
# At most one zoologist: not (P and Q) and not (P and R) and not (Q and R)
botanist_count = Sum([If(F, 1, 0), If(G, 1, 0), If(H, 1, 0)])
zoologist_count = Sum([If(P, 1, 0), If(Q, 1, 0), If(R, 1, 0)])
solver.add(Implies(botanist_count > 1, zoologist_count <= 1))

# 4. F and K cannot both be selected
solver.add(Not(And(F, K)))

# 5. K and M cannot both be selected
solver.add(Not(And(K, M)))

# 6. If M is selected, both P and R must be selected
solver.add(Implies(M, And(P, R)))

# Given: F, L, Q, R are selected
solver.add(F)
solver.add(L)
solver.add(Q)
solver.add(R)

# Now test each option as the fifth scientist
# Options: (A)G (B)H (C)K (D)M (E)P
found_options = []

# Option A: G
solver.push()
solver.add(G)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: H
solver.push()
solver.add(H)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: K
solver.push()
solver.add(K)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: M
solver.push()
solver.add(M)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: P
solver.push()
solver.add(P)
if solver.check() == sat:
    found_options.append("E")
solver.pop()

# Output results
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")