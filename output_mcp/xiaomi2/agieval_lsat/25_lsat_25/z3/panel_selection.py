from z3 import *

solver = Solver()

# Boolean variables for each scientist
F, G, H = Bools('F G H')  # Botanists
K, L, M = Bools('K L M')  # Chemists
P, Q, R = Bools('P Q R')  # Zoologists

botanists = [F, G, H]
chemists = [K, L, M]
zoologists = [P, Q, R]
all_scientists = botanists + chemists + zoologists

# Exactly 5 selected
solver.add(Sum([If(s, 1, 0) for s in all_scientists]) == 5)

# Constraint 1: At least one of each type
solver.add(Sum([If(s, 1, 0) for s in botanists]) >= 1)
solver.add(Sum([If(s, 1, 0) for s in chemists]) >= 1)
solver.add(Sum([If(s, 1, 0) for s in zoologists]) >= 1)

# Constraint 2: If more than one botanist, then at most one zoologist
num_bot = Sum([If(s, 1, 0) for s in botanists])
num_zoo = Sum([If(s, 1, 0) for s in zoologists])
solver.add(Implies(num_bot > 1, num_zoo <= 1))

# Constraint 3: F and K cannot both be selected
solver.add(Not(And(F, K)))

# Constraint 4: K and M cannot both be selected
solver.add(Not(And(K, M)))

# Constraint 5: If M is selected, both P and R must be selected
solver.add(Implies(M, And(P, R)))

# Define each option as a constraint
options = {
    "A": [F, G, K, P, Q, Not(H), Not(L), Not(M), Not(R)],
    "B": [G, H, K, L, M, Not(F), Not(P), Not(Q), Not(R)],
    "C": [G, H, K, L, R, Not(F), Not(M), Not(P), Not(Q)],
    "D": [H, K, M, P, R, Not(F), Not(G), Not(L), Not(Q)],
    "E": [H, L, M, P, Q, Not(F), Not(G), Not(K), Not(R)],
}

found_options = []
for letter, constr in options.items():
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