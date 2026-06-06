from z3 import *

solver = Solver()

# Six cookbooks: K, L, M, N, O, P
# Two seasons: 0 = Fall, 1 = Spring
K, L, M, N, O, P = Ints('K L M N O P')
books = [K, L, M, N, O, P]

# Domain: each book is 0 (fall) or 1 (spring)
for b in books:
    solver.add(Or(b == 0, b == 1))

# Constraint 1: M and P cannot be in the same season
solver.add(M != P)

# Constraint 2: K and N must be in the same season
solver.add(K == N)

# Constraint 3: If K is in fall, O must be in fall
solver.add(Implies(K == 0, O == 0))

# Constraint 4: If M is in fall, N must be in spring
solver.add(Implies(M == 0, N == 1))

# Given: N is published in the fall
solver.add(N == 0)

# Define each answer option
opt_a = (K == 1)       # K is published in the spring
opt_b = (L == 0)       # L is published in the fall
opt_c = (M == 0)       # M is published in the fall
opt_d = (O == 1)       # O is published in the spring
opt_e = (P == 1)       # P is published in the spring

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