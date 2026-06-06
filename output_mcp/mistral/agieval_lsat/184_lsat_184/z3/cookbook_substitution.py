from z3 import *

solver = Solver()

# Variables: 0 = fall, 1 = spring
K, L, M, N, O, P = Ints('K L M N O P')
seasons = [K, L, M, N, O, P]

# Each variable is either 0 (fall) or 1 (spring)
for s in seasons:
    solver.add(Or(s == 0, s == 1))

# Base constraints
# 1. M and P cannot be in the same season
solver.add(M != P)
# 2. K and N must be in the same season
solver.add(K == N)
# 3. If K is in fall, O must be in fall
solver.add(Implies(K == 0, O == 0))

# Option A: If L is in fall, M must be in spring
opt_a_constr = Implies(L == 0, M == 1)

# Option B: If N is in fall, P must also be in fall
opt_b_constr = Implies(N == 0, P == 0)

# Option C: If M is in spring, P must be in fall
opt_c_constr = Implies(M == 1, P == 0)

# Option D: If N is in spring, M must also be in spring
opt_d_constr = Implies(N == 1, M == 1)

# Option E: If O is in spring, N must also be in spring
opt_e_constr = Implies(O == 1, N == 1)

# Evaluate each option
found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
    solver.push()
    # Add the option's constraint
    solver.add(constr)
    # Check if the constraints are satisfiable
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