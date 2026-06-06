from z3 import *

# Seasons: 1 for Fall, 0 for Spring
K, L, M, N, O, P = Ints('K L M N O P')

solver = Solver()

# Domain constraints
for var in [K, L, M, N, O, P]:
    solver.add(Or(var == 0, var == 1))

# Conditions
# 1. M and P cannot be in the same season
solver.add(M != P)
# 2. K and N must be in the same season
solver.add(K == N)
# 3. If K is in the fall (1), O must be in the fall (1)
solver.add(Implies(K == 1, O == 1))
# 4. If M is in the fall (1), N must be in the spring (0)
solver.add(Implies(M == 1, N == 0))

# Question: If M is in the fall (1), which pair could be in the fall along with M?
# M = 1
solver.add(M == 1)

# Options (must be in the fall, i.e., value 1)
# (A) K and O: K=1, O=1
# (B) L and N: L=1, N=1
# (C) L and O: L=1, O=1
# (D) N and P: N=1, P=1
# (E) O and P: O=1, P=1

opt_a_constr = And(K == 1, O == 1)
opt_b_constr = And(L == 1, N == 1)
opt_c_constr = And(L == 1, O == 1)
opt_d_constr = And(N == 1, P == 1)
opt_e_constr = And(O == 1, P == 1)

found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
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