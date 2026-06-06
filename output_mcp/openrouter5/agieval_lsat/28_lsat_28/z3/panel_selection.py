from z3 import *

# Scientists: botanists F, G, H; chemists K, L, M; zoologists P, Q, R
# Boolean variables: True if selected
F, G, H = Bools('F G H')
K, L, M = Bools('K L M')
P, Q, R = Bools('P Q R')

solver = Solver()

# The panel must include at least one scientist of each of the three types.
solver.add(Or(F, G, H))  # at least one botanist
solver.add(Or(K, L, M))  # at least one chemist
solver.add(Or(P, Q, R))  # at least one zoologist

# If more than one botanist is selected, then at most one zoologist is selected.
# More than one botanist: at least 2 of {F,G,H}
# At most one zoologist: not (two or more zoologists)
# Equivalent: (count_botanists >= 2) => (count_zoologists <= 1)
count_botanists = Sum([If(F, 1, 0), If(G, 1, 0), If(H, 1, 0)])
count_zoologists = Sum([If(P, 1, 0), If(Q, 1, 0), If(R, 1, 0)])
solver.add(Implies(count_botanists >= 2, count_zoologists <= 1))

# F and K cannot both be selected.
solver.add(Not(And(F, K)))

# K and M cannot both be selected.
solver.add(Not(And(K, M)))

# If M is selected, both P and R must be selected.
solver.add(Implies(M, And(P, R)))

# Additional condition from the question: P is the only zoologist selected.
# So P is selected, and Q and R are not selected.
solver.add(P == True)
solver.add(Q == False)
solver.add(R == False)

# Now evaluate each option under these constraints.

# Option A: If K is selected, G cannot be selected.
# i.e., K => Not(G)
opt_a = Implies(K, Not(G))

# Option B: If L is selected, F cannot be selected.
# i.e., L => Not(F)
opt_b = Implies(L, Not(F))

# Option C: If exactly one chemist is selected, it must be K.
# exactly one chemist: count_chemists == 1
count_chemists = Sum([If(K, 1, 0), If(L, 1, 0), If(M, 1, 0)])
# "it must be K" means: if exactly one chemist, then K is selected.
opt_c = Implies(count_chemists == 1, K)

# Option D: If exactly two chemists are selected, F cannot be selected.
# exactly two chemists: count_chemists == 2
opt_d = Implies(count_chemists == 2, Not(F))

# Option E: If exactly two chemists are selected, G cannot be selected.
opt_e = Implies(count_chemists == 2, Not(G))

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