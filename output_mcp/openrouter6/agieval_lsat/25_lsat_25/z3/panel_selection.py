from z3 import *

# Declare boolean variables for each scientist
F, G, H, K, L, M, P, Q, R = Bools('F G H K L M P Q R')

solver = Solver()

# Base constraints
# 1. At least one of each type
solver.add(Or(F, G, H))   # at least one botanist
solver.add(Or(K, L, M))   # at least one chemist
solver.add(Or(P, Q, R))   # at least one zoologist

# 2. If more than one botanist, then at most one zoologist
# Number of botanists
botanists = Sum([If(F, 1, 0), If(G, 1, 0), If(H, 1, 0)])
# Number of zoologists
zoologists = Sum([If(P, 1, 0), If(Q, 1, 0), If(R, 1, 0)])
# Condition: if botanists >= 2 then zoologists <= 1
solver.add(Implies(botanists >= 2, zoologists <= 1))

# 3. F and K cannot both be selected
solver.add(Not(And(F, K)))

# 4. K and M cannot both be selected
solver.add(Not(And(K, M)))

# 5. If M is selected, both P and R must be selected
solver.add(Implies(M, And(P, R)))

# 6. Exactly 5 scientists selected
total = Sum([If(F, 1, 0), If(G, 1, 0), If(H, 1, 0),
             If(K, 1, 0), If(L, 1, 0), If(M, 1, 0),
             If(P, 1, 0), If(Q, 1, 0), If(R, 1, 0)])
solver.add(total == 5)

# Define options as lists of scientists
options = [
    ("A", [F, G, K, P, Q]),
    ("B", [G, H, K, L, M]),
    ("C", [G, H, K, L, R]),
    ("D", [H, K, M, P, R]),
    ("E", [H, L, M, P, Q])
]

found_options = []
for letter, selected in options:
    solver.push()
    # For each scientist variable, set true if in selected list, else false
    # We'll create a list of all variables
    all_vars = [F, G, H, K, L, M, P, Q, R]
    for var in all_vars:
        if var in selected:
            solver.add(var == True)
        else:
            solver.add(var == False)
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