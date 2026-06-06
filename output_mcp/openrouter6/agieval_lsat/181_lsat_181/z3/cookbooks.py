from z3 import *

solver = Solver()

# Declare variables for each cookbook (True = fall, False = spring)
K = Bool('K')
L = Bool('L')
M = Bool('M')
N = Bool('N')
O = Bool('O')
P = Bool('P')

# Base constraints
# 1. M and P cannot be published in the same season
solver.add(M != P)
# 2. K and N must be published in the same season
solver.add(K == N)
# 3. If K is published in the fall, O must also be published in the fall
solver.add(Implies(K, O))
# 4. If M is published in the fall, N must be published in the spring
solver.add(Implies(M, Not(N)))
# Given: M is published in the fall
solver.add(M == True)

# Evaluate each answer choice
found_options = []
for letter, constr in [
    ("A", [K == True, O == True]),
    ("B", [L == True, N == True]),
    ("C", [L == True, O == True]),
    ("D", [N == True, P == True]),
    ("E", [O == True, P == True])
]:
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