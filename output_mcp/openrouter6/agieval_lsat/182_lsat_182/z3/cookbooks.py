from z3 import *

# Define boolean variables for each cookbook
K = Bool('K')
L = Bool('L')
M = Bool('M')
N = Bool('N')
O = Bool('O')
P = Bool('P')

solver = Solver()

# Base constraints
# 1. M and P cannot be published in the same season
solver.add(M != P)
# 2. K and N must be published in the same season
solver.add(K == N)
# 3. If K is published in the fall, O must also be published in the fall
solver.add(Implies(K, O))
# 4. If M is published in the fall, N must be published in the spring
solver.add(Implies(M, Not(N)))

# Given: N is published in the fall
solver.add(N == True)

# Define options as constraints
opt_a = (K == False)   # K is spring
opt_b = (L == True)    # L is fall
opt_c = (M == True)    # M is fall
opt_d = (O == False)   # O is spring
opt_e = (P == False)   # P is spring

found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
        # Optional: print model for debugging
        # m = solver.model()
        # print(f"Option {letter} is possible. Model: {m}")
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