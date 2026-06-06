from z3 import *

solver = Solver()

# Boolean variables: True = fall, False = spring
K = Bool('K')
L = Bool('L')
M = Bool('M')
N = Bool('N')
O = Bool('O')
P = Bool('P')

# Base constraints
# 1. M and P cannot be published in the same season
solver.add(Not(M == P))

# 2. K and N must be published in the same season
solver.add(K == N)

# 3. If K is published in the fall, O must also be published in the fall
solver.add(Implies(K, O))

# 4. If M is published in the fall, N must be published in the spring
solver.add(Implies(M, Not(N)))

# Given condition: M is published in the fall
solver.add(M == True)

# Now test each answer choice
# The question asks: which pair could BOTH be published in the fall along with M?
# So we test: M is fall AND both cookbooks in the pair are fall

found_options = []

# (A) K and O both in fall
opt_a = And(K, O)
# (B) L and N both in fall
opt_b = And(L, N)
# (C) L and O both in fall
opt_c = And(L, O)
# (D) N and P both in fall
opt_d = And(N, P)
# (E) O and P both in fall
opt_e = And(O, P)

for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
        m = solver.model()
        print(f"Option {letter} is SAT: K={m[K]}, L={m[L]}, M={m[M]}, N={m[N]}, O={m[O]}, P={m[P]}")
    else:
        print(f"Option {letter} is UNSAT")
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