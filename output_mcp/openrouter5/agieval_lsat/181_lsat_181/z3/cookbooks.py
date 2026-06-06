from z3 import *

solver = Solver()

# Variables: each cookbook's season (True = fall, False = spring)
K, L, M, N, O, P = Bools('K L M N O P')

# M and P cannot be in the same season
solver.add(M != P)

# K and N must be in the same season
solver.add(K == N)

# If K is fall, O must be fall
solver.add(Implies(K, O))

# If M is fall, N must be spring
solver.add(Implies(M, Not(N)))

# Additional condition from the question: M is published in the fall
solver.add(M == True)

# Now evaluate each option: which pair could both be published in the fall along with M?
# Each option says: both X and Y are in the fall (True)
options = [
    ("A", And(K == True, O == True)),
    ("B", And(L == True, N == True)),
    ("C", And(L == True, O == True)),
    ("D", And(N == True, P == True)),
    ("E", And(O == True, P == True))
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