from z3 import *

# Define variables
F, G, H = Bools('F G H')
K, L, M = Bools('K L M')
P, Q, R = Bools('P Q R')
scientists = [F, G, H, K, L, M, P, Q, R]

def get_base_constraints():
    constraints = []
    # Panel size = 5
    constraints.append(Sum([If(s, 1, 0) for s in scientists]) == 5)
    # At least one of each type
    constraints.append(Sum([If(s, 1, 0) for s in [F, G, H]]) >= 1)
    constraints.append(Sum([If(s, 1, 0) for s in [K, L, M]]) >= 1)
    constraints.append(Sum([If(s, 1, 0) for s in [P, Q, R]]) >= 1)
    # If > 1 botanist, then <= 1 zoologist
    constraints.append(Implies(Sum([If(s, 1, 0) for s in [F, G, H]]) > 1, Sum([If(s, 1, 0) for s in [P, Q, R]]) <= 1))
    # F and K cannot both be selected
    constraints.append(Not(And(F, K)))
    # K and M cannot both be selected
    constraints.append(Not(And(K, M)))
    # If M is selected, both P and R must be selected
    constraints.append(Implies(M, And(P, R)))
    return constraints

# Re-check all options to be sure
options = [
    ("A", Or(F, K)),
    ("B", Or(F, M)),
    ("C", Or(K, M)),
    ("D", Or(M, Q)),
    ("E", Or(P, Q))
]

valid_options = []
for label, option in options:
    solver = Solver()
    for c in get_base_constraints():
        solver.add(c)
    
    # Condition: G and H are selected
    solver.add(G, H)
    # Condition: Option is NOT selected
    solver.add(Not(option))
    
    if solver.check() == unsat:
        valid_options.append(label)

if len(valid_options) == 1:
    print("STATUS: sat")
    print(f"answer:{valid_options[0]}")
elif len(valid_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {valid_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")