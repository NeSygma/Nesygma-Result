from z3 import *

solver = Solver()

# Scientists: botanists F, G, H; chemists K, L, M; zoologists P, Q, R
# Boolean variables: True means selected
F, G, H = Bools('F G H')
K, L, M = Bools('K L M')
P, Q, R = Bools('P Q R')

all_scientists = [F, G, H, K, L, M, P, Q, R]

# Condition 1: At least one of each type
solver.add(Or(F, G, H))  # at least one botanist
solver.add(Or(K, L, M))  # at least one chemist
solver.add(Or(P, Q, R))  # at least one zoologist

# Condition 2: If more than one botanist selected, then at most one zoologist selected
# More than one botanist: at least 2 of {F, G, H}
more_than_one_botanist = Sum([If(b, 1, 0) for b in [F, G, H]]) >= 2
at_most_one_zoologist = Sum([If(z, 1, 0) for z in [P, Q, R]]) <= 1
solver.add(Implies(more_than_one_botanist, at_most_one_zoologist))

# Condition 3: F and K cannot both be selected
solver.add(Not(And(F, K)))

# Condition 4: K and M cannot both be selected
solver.add(Not(And(K, M)))

# Condition 5: If M is selected, both P and R must be selected
solver.add(Implies(M, And(P, R)))

# Additional condition from the question: M is the ONLY chemist selected
solver.add(M)  # M is selected
# Only M is selected among chemists: K not selected, L not selected
solver.add(Not(K))
solver.add(Not(L))

# Now evaluate each option
# Option A: F and G are both selected
opt_a = And(F, G)

# Option B: G and H are both selected
opt_b = And(G, H)

# Option C: H and P are both selected
opt_c = And(H, P)

# Option D: F, G, and H are all selected
opt_d = And(F, G, H)

# Option E: P, Q, and R are all selected
opt_e = And(P, Q, R)

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