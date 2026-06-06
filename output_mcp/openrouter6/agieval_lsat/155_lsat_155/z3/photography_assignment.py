from z3 import *

# Define variables for each photographer: 0 = unassigned, 1 = Silva, 2 = Thorne
F, G, H, K, L, M = Ints('F G H K L M')

solver = Solver()

# Domain constraints: each variable in {0,1,2}
solver.add(0 <= F, F <= 2)
solver.add(0 <= G, G <= 2)
solver.add(0 <= H, H <= 2)
solver.add(0 <= K, K <= 2)
solver.add(0 <= L, L <= 2)
solver.add(0 <= M, M <= 2)

# At least two photographers assigned to each ceremony
silva_count = Sum([If(F == 1, 1, 0), If(G == 1, 1, 0), If(H == 1, 1, 0),
                   If(K == 1, 1, 0), If(L == 1, 1, 0), If(M == 1, 1, 0)])
thorne_count = Sum([If(F == 2, 1, 0), If(G == 2, 1, 0), If(H == 2, 1, 0),
                    If(K == 2, 1, 0), If(L == 2, 1, 0), If(M == 2, 1, 0)])
solver.add(silva_count >= 2)
solver.add(thorne_count >= 2)

# Frost and Heideck together: either both unassigned, or both assigned to same ceremony
solver.add(Or(
    And(F == 0, H == 0),
    And(F == 1, H == 1),
    And(F == 2, H == 2)
))

# If Lai and Mays are both assigned, they must be to different ceremonies
solver.add(Implies(And(L != 0, M != 0), L != M))

# If Gonzalez is assigned to Silva, then Lai must be assigned to Thorne
solver.add(Implies(G == 1, L == 2))

# If Knutson is not assigned to Thorne, then both Heideck and Mays must be assigned to Thorne
solver.add(Implies(K != 2, And(H == 2, M == 2)))

# Now define the options as constraints
options = [
    ("A", [G == 1, L == 1, F == 2, H == 2, M == 2, K == 0]),
    ("B", [G == 1, M == 1, K == 2, L == 2, F == 0, H == 0]),
    ("C", [F == 1, G == 1, H == 1, K == 2, L == 2, M == 2]),
    ("D", [F == 1, H == 1, M == 1, G == 2, L == 2, K == 0]),
    ("E", [F == 1, H == 1, M == 1, G == 2, K == 2, L == 2])
]

found_options = []
for letter, constr in options:
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