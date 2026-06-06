from z3 import *

# Boolean variables: True if scientist is selected
F, G, H = Bools('F G H')  # Botanists
K, L, M = Bools('K L M')  # Chemists
P, Q, R = Bools('P Q R')  # Zoologists

all_scientists = [F, G, H, K, L, M, P, Q, R]
botanists = [F, G, H]
chemists = [K, L, M]
zoologists = [P, Q, R]

# Base constraints
solver = Solver()

# Panel of exactly 5
solver.add(Sum([If(s, 1, 0) for s in all_scientists]) == 5)

# At least one of each type
solver.add(Sum([If(s, 1, 0) for s in botanists]) >= 1)
solver.add(Sum([If(s, 1, 0) for s in chemists]) >= 1)
solver.add(Sum([If(s, 1, 0) for s in zoologists]) >= 1)

# If more than one botanist, at most one zoologist
num_bot = Sum([If(s, 1, 0) for s in botanists])
num_zoo = Sum([If(s, 1, 0) for s in zoologists])
solver.add(Implies(num_bot > 1, num_zoo <= 1))

# F and K cannot both be selected
solver.add(Not(And(F, K)))

# K and M cannot both be selected
solver.add(Not(And(K, M)))

# If M is selected, both P and R must be selected
solver.add(Implies(M, And(P, R)))

# PREMISE: Both G and H are selected
solver.add(G)
solver.add(H)

# Define answer choice constraints
# Each choice says "the panel must include either X or else Y"
# We check: is it ALWAYS true (entailed by the premises)?
# To check entailment, we try to find a model where premises hold but the choice is FALSE.
# If unsat, the choice is necessarily true.

options = {
    "A": Or(F, K),        # F or else K
    "B": Or(F, M),        # F or else M
    "C": Or(K, M),        # K or else M
    "D": Or(M, Q),        # M or else Q
    "E": Or(P, Q),        # P or else Q
}

found_options = []
for letter, choice_constr in options.items():
    solver.push()
    solver.add(Not(choice_constr))  # Try to find a counterexample
    if solver.check() == unsat:
        # No counterexample exists → choice is necessarily true
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

# Also enumerate all valid panels for verification
print("\n--- All valid panels when G and H are selected ---")
solver2 = Solver()
solver2.add(solver.assertions())  # won't work, need to re-add
# Rebuild
solver2.add(Sum([If(s, 1, 0) for s in all_scientists]) == 5)
solver2.add(Sum([If(s, 1, 0) for s in botanists]) >= 1)
solver2.add(Sum([If(s, 1, 0) for s in chemists]) >= 1)
solver2.add(Sum([If(s, 1, 0) for s in zoologists]) >= 1)
solver2.add(Implies(num_bot > 1, num_zoo <= 1))
solver2.add(Not(And(F, K)))
solver2.add(Not(And(K, M)))
solver2.add(Implies(M, And(P, R)))
solver2.add(G)
solver2.add(H)

panel_count = 0
while solver2.check() == sat:
    m = solver2.model()
    selected = [str(s) for s in all_scientists if m.evaluate(s, model_completion=True)]
    print(f"  Panel {panel_count+1}: {selected}")
    panel_count += 1
    solver2.add(Or([s != m.evaluate(s, model_completion=True) for s in all_scientists]))
print(f"Total valid panels: {panel_count}")