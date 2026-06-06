from z3 import *

solver = Solver()

# Variables: 0 = Not assigned, 1 = Silva, 2 = Thorne
F, G, H, K, L, M = Ints('F G H K L M')
names = {'F': F, 'G': G, 'H': H, 'K': K, 'L': L, 'M': M}

# Domain constraints: each must be 0, 1, or 2
for var in [F, G, H, K, L, M]:
    solver.add(Or(var == 0, var == 1, var == 2))

# At least 2 photographers at Silva
solver.add(Sum([If(var == 1, 1, 0) for var in [F, G, H, K, L, M]]) >= 2)

# At least 2 photographers at Thorne
solver.add(Sum([If(var == 2, 1, 0) for var in [F, G, H, K, L, M]]) >= 2)

# Frost and Heideck must be assigned together to one of the ceremonies
# Both assigned, and to the same ceremony
solver.add(F != 0)
solver.add(H != 0)
solver.add(F == H)

# If Lai and Mays are both assigned, they must be to different ceremonies
solver.add(Implies(And(L != 0, M != 0), L != M))

# If Gonzalez is assigned to Silva, then Lai must be assigned to Thorne
solver.add(Implies(G == 1, L == 2))

# If Knutson is not assigned to Thorne, then both Heideck and Mays must be assigned to it
solver.add(Implies(K != 2, And(H == 2, M == 2)))

# Additional condition for the question: Heideck and Lai are at the same ceremony
solver.add(H == L)

# Now evaluate each option using negation test (must be true = negation is unsat)
# Options:
# (A) Frost is assigned to Thorne: F == 2
# (B) Gonzalez is assigned to Silva: G == 1
# (C) Gonzalez is assigned to neither: G == 0
# (D) Knutson is assigned to Thorne: K == 2
# (E) Lai is assigned to Thorne: L == 2

options = [
    ("A", F == 2),
    ("B", G == 1),
    ("C", G == 0),
    ("D", K == 2),
    ("E", L == 2)
]

found_options = []

for letter, constr in options:
    solver.push()
    solver.add(Not(constr))  # try to find counterexample where option is false
    if solver.check() == unsat:
        # No counterexample -> option must be true
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