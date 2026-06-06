from z3 import *

solver = Solver()

# Define Boolean variables for each scientist
F, G, H = Bools('F G H')  # Botanists
K, L, M = Bools('K L M')  # Chemists
P, Q, R = Bools('P Q R')  # Zoologists

# Panel size constraint: exactly 5 scientists
solver.add(Sum([If(x, 1, 0) for x in [F, G, H, K, L, M, P, Q, R]]) == 5)

# At least one of each type
solver.add(Or(F, G, H))  # At least one botanist
solver.add(Or(K, L, M))  # At least one chemist
solver.add(Or(P, Q, R))  # At least one zoologist

# If more than one botanist is selected, then at most one zoologist is selected
botanist_count = Sum([If(x, 1, 0) for x in [F, G, H]])
zoologist_count = Sum([If(x, 1, 0) for x in [P, Q, R]])
solver.add(Implies(botanist_count > 1, zoologist_count <= 1))

# F and K cannot both be selected
solver.add(Not(And(F, K)))

# K and M cannot both be selected
solver.add(Not(And(K, M)))

# If M is selected, both P and R must be selected
solver.add(Implies(M, And(P, R)))

# Additional condition: P is the only zoologist selected
solver.add(P == True)
solver.add(Q == False)
solver.add(R == False)

# Define the answer choices as constraints
# (A) If K is selected, G cannot be selected.
opt_a = Implies(K, Not(G))

# (B) If L is selected, F cannot be selected.
opt_b = Implies(L, Not(F))

# (C) If exactly one chemist is selected, it must be K.
chemist_count = Sum([If(x, 1, 0) for x in [K, L, M]])
opt_c = Implies(chemist_count == 1, K)

# (D) If exactly two chemists are selected, F cannot be selected.
opt_d = Implies(chemist_count == 2, Not(F))

# (E) If exactly two chemists are selected, G cannot be selected.
opt_e = Implies(chemist_count == 2, Not(G))

# Test each option: check if the option MUST be true (i.e., its negation is unsatisfiable)
found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(Not(constr))  # Try to find a counterexample
    if solver.check() == unsat:
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