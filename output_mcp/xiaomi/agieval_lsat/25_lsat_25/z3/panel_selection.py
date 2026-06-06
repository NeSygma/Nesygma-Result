from z3 import *

# Create Boolean variables for each scientist
F, G, H = Bools('F G H')  # Botanists
K, L, M = Bools('K L M')  # Chemists
P, Q, R = Bools('P Q R')  # Zoologists

solver = Solver()

# Base constraints from the problem statement
# 1. Panel must have exactly 5 scientists
solver.add(Sum([If(s, 1, 0) for s in [F, G, H, K, L, M, P, Q, R]]) == 5)

# 2. At least one of each type
solver.add(Or(F, G, H))  # At least one botanist
solver.add(Or(K, L, M))  # At least one chemist
solver.add(Or(P, Q, R))  # At least one zoologist

# 3. If more than one botanist is selected, then at most one zoologist is selected
botanist_count = Sum([If(F, 1, 0), If(G, 1, 0), If(H, 1, 0)])
zoologist_count = Sum([If(P, 1, 0), If(Q, 1, 0), If(R, 1, 0)])
solver.add(Implies(botanist_count > 1, zoologist_count <= 1))

# 4. F and K cannot both be selected
solver.add(Not(And(F, K)))

# 5. K and M cannot both be selected
solver.add(Not(And(K, M)))

# 6. If M is selected, both P and R must be selected
solver.add(Implies(M, And(P, R)))

# Define constraints for each answer option
opt_a = And(F, G, K, P, Q, Not(H), Not(L), Not(M), Not(R))
opt_b = And(G, H, K, L, M, Not(F), Not(P), Not(Q), Not(R))
opt_c = And(G, H, K, L, R, Not(F), Not(M), Not(P), Not(Q))
opt_d = And(H, K, M, P, R, Not(F), Not(G), Not(L), Not(Q))
opt_e = And(H, L, M, P, Q, Not(F), Not(G), Not(K), Not(R))

found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
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