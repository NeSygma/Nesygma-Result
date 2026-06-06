from z3 import *

# Define boolean variables for each scientist
F, G, H = Bools('F G H')  # botanists
K, L, M = Bools('K L M')  # chemists
P, Q, R = Bools('P Q R')  # zoologists

solver = Solver()

# The panel must include at least one scientist of each of the three types.
solver.add(Or(F, G, H))  # at least one botanist
solver.add(Or(K, L, M))  # at least one chemist
solver.add(Or(P, Q, R))  # at least one zoologist

# If more than one botanist is selected, then at most one zoologist is selected.
# More than one botanist: at least 2 of F,G,H are selected.
more_than_one_botanist = Or(
    And(F, G), And(F, H), And(G, H)
)
# At most one zoologist: not (two or more zoologists selected)
# i.e., at most one of P,Q,R is selected.
at_most_one_zoologist = Not(Or(
    And(P, Q), And(P, R), And(Q, R)
))
solver.add(Implies(more_than_one_botanist, at_most_one_zoologist))

# F and K cannot both be selected.
solver.add(Not(And(F, K)))

# K and M cannot both be selected.
solver.add(Not(And(K, M)))

# If M is selected, both P and R must be selected.
solver.add(Implies(M, And(P, R)))

# Now evaluate each option
# Option A: F, G, K, P, Q
opt_a = And(F, G, K, P, Q, Not(H), Not(L), Not(M), Not(R))

# Option B: G, H, K, L, M
opt_b = And(G, H, K, L, M, Not(F), Not(P), Not(Q), Not(R))

# Option C: G, H, K, L, R
opt_c = And(G, H, K, L, R, Not(F), Not(M), Not(P), Not(Q))

# Option D: H, K, M, P, R
opt_d = And(H, K, M, P, R, Not(F), Not(G), Not(L), Not(Q))

# Option E: H, L, M, P, Q
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