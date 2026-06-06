from z3 import *

solver = Solver()

# Variables: each cookbook is assigned a season (0 = fall, 1 = spring)
K, L, M, N, O, P = Ints('K L M N O P')
for var in [K, L, M, N, O, P]:
    solver.add(Or(var == 0, var == 1))  # 0 = fall, 1 = spring

# Base constraints
# 1. M and P cannot be published in the same season
solver.add(M != P)

# 2. K and N must be published in the same season
solver.add(K == N)

# 3. If K is published in the fall, O must also be published in the fall
solver.add(Implies(K == 0, O == 0))

# 4. If M is published in the fall, N must be published in the spring
solver.add(Implies(M == 0, N == 1))

# Given condition: M is published in the fall
solver.add(M == 0)

# Now evaluate each option: which pair could BOTH be in the fall along with M?
# Option A: K and O both in fall
opt_a = And(K == 0, O == 0)
# Option B: L and N both in fall
opt_b = And(L == 0, N == 0)
# Option C: L and O both in fall
opt_c = And(L == 0, O == 0)
# Option D: N and P both in fall
opt_d = And(N == 0, P == 0)
# Option E: O and P both in fall
opt_e = And(O == 0, P == 0)

found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
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