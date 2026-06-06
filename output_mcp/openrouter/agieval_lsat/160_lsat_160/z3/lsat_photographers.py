from z3 import *

# Decision variables: 0 = not assigned, 1 = Silva, 2 = Thorne
F = Int('F')
G = Int('G')
H = Int('H')
K = Int('K')
L = Int('L')
M = Int('M')
vars = [F, G, H, K, L, M]
solver = Solver()
# Domain constraints
for v in vars:
    solver.add(Or(v == 0, v == 1, v == 2))
# At least two at each ceremony
silva_cnt = Sum([If(v == 1, 1, 0) for v in vars])
thorne_cnt = Sum([If(v == 2, 1, 0) for v in vars])
solver.add(silva_cnt >= 2)
solver.add(thorne_cnt >= 2)
# Constraint 1: Frost and Heideck together at same ceremony and both assigned
solver.add(F != 0, H != 0, F == H)
# Constraint 2: If L and M both assigned, they must be at different ceremonies
solver.add(Implies(And(L != 0, M != 0), L != M))
# Constraint 3: If G at Silva then L at Thorne
solver.add(Implies(G == 1, L == 2))
# Constraint 4: If K not at Thorne then H and M must be at Thorne
solver.add(Implies(K != 2, And(H == 2, M == 2)))

# Helper to enforce a specific Thorne set
option_sets = {
    'A': ['F', 'G', 'H', 'M'],
    'B': ['F', 'H', 'K', 'M'],
    'C': ['G', 'K', 'L'],
    'D': ['G', 'K', 'M'],
    'E': ['K', 'M']
}

found_options = []  # will collect options that are IMPOSSIBLE (unsat)
for letter, names in option_sets.items():
    solver.push()
    # Enforce that exactly these photographers are at Thorne (value 2)
    for p in ['F','G','H','K','L','M']:
        var = eval(p)
        if p in names:
            solver.add(var == 2)
        else:
            solver.add(var != 2)  # can be 0 or 1
    # Check satisfiability
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