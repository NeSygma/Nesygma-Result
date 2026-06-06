from z3 import *

# Boolean variables for each scientist
F, G, H = Bools('F G H')  # botanists
K, L, M = Bools('K L M')  # chemists
P, Q, R = Bools('P Q R')  # zoologists

solver = Solver()

# The panel consists of exactly 5 scientists
all_scientists = [F, G, H, K, L, M, P, Q, R]
solver.add(Sum([If(s, 1, 0) for s in all_scientists]) == 5)

# Condition 1: At least one of each type
solver.add(Or(F, G, H))  # at least one botanist
solver.add(Or(K, L, M))  # at least one chemist
solver.add(Or(P, Q, R))  # at least one zoologist

# Condition 2: If more than one botanist is selected, then at most one zoologist is selected
# More than one botanist: at least 2 botanists
more_than_one_botanist = Sum([If(F, 1, 0), If(G, 1, 0), If(H, 1, 0)]) >= 2
at_most_one_zoologist = Sum([If(P, 1, 0), If(Q, 1, 0), If(R, 1, 0)]) <= 1
solver.add(Implies(more_than_one_botanist, at_most_one_zoologist))

# Condition 3: F and K cannot both be selected
solver.add(Not(And(F, K)))

# Condition 4: K and M cannot both be selected
solver.add(Not(And(K, M)))

# Condition 5: If M is selected, both P and R must be selected
solver.add(Implies(M, And(P, R)))

# Now evaluate each option
# Option A: F, G, K, P, Q
opt_a = And(F, G, Not(H), K, Not(L), Not(M), P, Q, Not(R))

# Option B: G, H, K, L, M
opt_b = And(Not(F), G, H, K, L, M, Not(P), Not(Q), Not(R))

# Option C: G, H, K, L, R
opt_c = And(Not(F), G, H, K, L, Not(M), Not(P), Not(Q), R)

# Option D: H, K, M, P, R
opt_d = And(Not(F), Not(G), H, K, Not(L), M, P, Not(Q), R)

# Option E: H, L, M, P, Q
opt_e = And(Not(F), Not(G), H, Not(K), L, M, P, Q, Not(R))

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