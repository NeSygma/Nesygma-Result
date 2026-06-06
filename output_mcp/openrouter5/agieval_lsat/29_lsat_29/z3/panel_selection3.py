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

# Let's enumerate all valid panels to see what's forced
print("Enumerating all valid panels...")
solutions = []
decision_vars = [F, G, H, K, L, M, P, Q, R]

while solver.check() == sat:
    m = solver.model()
    sol = {str(v): m.eval(v, model_completion=True) for v in decision_vars}
    solutions.append(sol)
    # Block this solution
    solver.add(Or([v != m.eval(v, model_completion=True) for v in decision_vars]))

print(f"Total valid panels: {len(solutions)}")
for i, sol in enumerate(solutions):
    selected = [v for v in sol if sol[v] == True]
    print(f"  Panel {i+1}: {selected}")

# Now check each option: is it true in ALL valid panels?
print("\nChecking which options are forced in all panels...")
found_options = []

options = [
    ("A", Or(F, K)),
    ("B", Or(F, M)),
    ("C", Or(K, M)),
    ("D", Or(M, Q)),
    ("E", Or(P, Q))
]

for letter, constr in options:
    # Check if constr holds in all solutions
    all_true = True
    for sol in solutions:
        # Evaluate the constraint in this solution
        # We need to check if the constraint is satisfied
        # Build a temporary solver with this assignment
        tmp = Solver()
        for v in decision_vars:
            tmp.add(v == (sol[str(v)] == True))
        tmp.add(Not(constr))
        if tmp.check() == sat:
            all_true = False
            break
    
    if all_true:
        found_options.append(letter)
        print(f"  Option {letter} ({constr}) is forced in ALL panels")
    else:
        print(f"  Option {letter} ({constr}) is NOT forced")

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")