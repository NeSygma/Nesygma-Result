from z3 import *

# Scientists: botanists (F, G, H), chemists (K, L, M), zoologists (P, Q, R)
F, G, H = Bools('F G H')
K, L, M = Bools('K L M')
P, Q, R = Bools('P Q R')

solver = Solver()

# At least one of each type
solver.add(Or(F, G, H))
solver.add(Or(K, L, M))
solver.add(Or(P, Q, R))

# If more than one botanist, then at most one zoologist
num_botanists = Sum([If(F, 1, 0), If(G, 1, 0), If(H, 1, 0)])
num_zoologists = Sum([If(P, 1, 0), If(Q, 1, 0), If(R, 1, 0)])
solver.add(Implies(num_botanists >= 2, num_zoologists <= 1))

# F and K cannot both be selected
solver.add(Not(And(F, K)))
# K and M cannot both be selected
solver.add(Not(And(K, M)))
# If M is selected, both P and R must be selected
solver.add(Implies(M, And(P, R)))

# Given: both G and H are selected
solver.add(And(G, H))

# The question asks: "the panel must include either ___ or else ___"
# This means: in EVERY valid panel (given G and H), at least one of the two must be selected.
# So we need to find which pair is forced (at least one of them must be in every panel).

# Let's check each option: is it true that in ALL valid panels, at least one of the two is selected?
# We check by seeing if there exists a valid panel where NEITHER is selected.

found_options = []

options = [
    ("A", F, K),
    ("B", F, M),
    ("C", K, M),
    ("D", M, Q),
    ("E", P, Q)
]

for letter, var1, var2 in options:
    s = Solver()
    # Add all base constraints
    s.add(Or(F, G, H))
    s.add(Or(K, L, M))
    s.add(Or(P, Q, R))
    s.add(Implies(num_botanists >= 2, num_zoologists <= 1))
    s.add(Not(And(F, K)))
    s.add(Not(And(K, M)))
    s.add(Implies(M, And(P, R)))
    s.add(And(G, H))
    # Try to find a panel where NEITHER var1 nor var2 is selected
    s.add(Not(var1))
    s.add(Not(var2))
    
    if s.check() == unsat:
        # No panel exists without at least one of them -> forced
        found_options.append(letter)
        print(f"Option {letter}: MUST include {var1} or {var2} (forced)")
    else:
        print(f"Option {letter}: NOT forced - counterexample exists")
        if s.check() == sat:
            m = s.model()
            selected = [v for v in [F,G,H,K,L,M,P,Q,R] if m.eval(v, model_completion=True) == True]
            print(f"  Counterexample panel: {selected}")

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")