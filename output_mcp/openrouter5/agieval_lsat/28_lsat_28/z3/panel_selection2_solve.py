from z3 import *

# Scientists: botanists F, G, H; chemists K, L, M; zoologists P, Q, R
F, G, H = Bools('F G H')
K, L, M = Bools('K L M')
P, Q, R = Bools('P Q R')

solver = Solver()

# At least one of each type
solver.add(Or(F, G, H))
solver.add(Or(K, L, M))
solver.add(Or(P, Q, R))

# If more than one botanist, then at most one zoologist
count_botanists = Sum([If(F, 1, 0), If(G, 1, 0), If(H, 1, 0)])
count_zoologists = Sum([If(P, 1, 0), If(Q, 1, 0), If(R, 1, 0)])
solver.add(Implies(count_botanists >= 2, count_zoologists <= 1))

# F and K cannot both be selected
solver.add(Not(And(F, K)))

# K and M cannot both be selected
solver.add(Not(And(K, M)))

# If M is selected, both P and R must be selected
solver.add(Implies(M, And(P, R)))

# Question condition: P is the only zoologist selected
solver.add(P == True)
solver.add(Q == False)
solver.add(R == False)

# Since M => P and R, and R=False, M must be False
# Let's add that explicitly to be safe
solver.add(M == False)

# Now evaluate each option

# Option A: If K is selected, G cannot be selected.
# i.e., K => Not(G)
opt_a = Implies(K, Not(G))

# Option B: If L is selected, F cannot be selected.
# i.e., L => Not(F)
opt_b = Implies(L, Not(F))

# Option C: If exactly one chemist is selected, it must be K.
# exactly_one_chemist => K
count_chemists = Sum([If(K, 1, 0), If(L, 1, 0), If(M, 1, 0)])
opt_c = Implies(count_chemists == 1, K)

# Option D: If exactly two chemists are selected, F cannot be selected.
# exactly_two_chemists => Not(F)
opt_d = Implies(count_chemists == 2, Not(F))

# Option E: If exactly two chemists are selected, G cannot be selected.
# exactly_two_chemists => Not(G)
opt_e = Implies(count_chemists == 2, Not(G))

# For "must be true" questions, we need to check if the statement is NECESSARILY true
# under the given conditions. So we check if Not(statement) is satisfiable.
# If Not(statement) is UNSAT, then the statement MUST be true.

found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(Not(constr))  # Check if the negation is satisfiable
    if solver.check() == unsat:
        # The statement must be true (its negation is impossible)
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