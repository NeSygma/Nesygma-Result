from z3 import *

# Variables: each cookbook's season (0 = spring, 1 = fall)
K, L, M, N, O, P = Bools('K L M N O P')
# True = fall, False = spring

# Base constraints
base_constraints = [
    M != P,           # M and P cannot be in same season
    K == N,           # K and N must be in same season
    Implies(K, O),    # If K is fall, O must be fall
    Implies(M, Not(N)) # If M is fall, N must be spring
]

# Let's first understand the solution space without any option
s = Solver()
s.add(base_constraints)
print("Total solutions without any option:")
vars_list = [K, L, M, N, O, P]
count = 0
while s.check() == sat:
    count += 1
    m = s.model()
    s.add(Or([v != m.eval(v) for v in vars_list]))
print(f"Count: {count}")

# Now evaluate each option
options = [
    ("A", And(K, Not(L))),  # K is fall, L is spring
    ("B", And(O, Not(P))),  # O is fall, P is spring
    ("C", And(P, Not(L))),  # P is fall, L is spring
    ("D", And(Not(K), Not(L))),  # Both K and L are spring
    ("E", And(M, L))  # Both M and L are fall
]

for letter, constr in options:
    s2 = Solver()
    s2.add(base_constraints)
    s2.add(constr)
    count = 0
    while s2.check() == sat:
        count += 1
        m = s2.model()
        s2.add(Or([v != m.eval(v) for v in vars_list]))
    print(f"Option {letter}: {count} solutions")
    if count == 1:
        m = s2.model()  # This won't work since we exhausted it. Let's redo.
        # Actually let's just print the single solution for the correct one