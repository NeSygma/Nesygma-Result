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

# Let's first check if the premises are satisfiable at all
print("Checking if premises are satisfiable...")
solver.push()
result = solver.check()
print(f"Premises check: {result}")
if result == sat:
    m = solver.model()
    for v in [F, G, H, K, L, M, P, Q, R]:
        print(f"  {v} = {m[v]}")
solver.pop()

# Now let's test each option differently.
# The question says: "the panel must include either X or else Y"
# This means: in every valid panel (satisfying all conditions including G and H),
# at least one of X or Y is selected.
# So we check: is there a valid panel where NEITHER X nor Y is selected?
# If no such panel exists, then the option is forced.

found_options = []

options = [
    ("A", Or(F, K)),
    ("B", Or(F, M)),
    ("C", Or(K, M)),
    ("D", Or(M, Q)),
    ("E", Or(P, Q))
]

for letter, constr in options:
    solver.push()
    # Try to find a model where the option is FALSE (neither X nor Y selected)
    solver.add(Not(constr))
    if solver.check() == unsat:
        # No model exists where the option is false -> option must be true in all models
        found_options.append(letter)
    solver.pop()

print(f"\nFound options (must be true): {found_options}")

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")