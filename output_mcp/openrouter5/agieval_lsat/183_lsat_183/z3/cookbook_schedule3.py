from z3 import *

# Variables: each cookbook's season (True = fall, False = spring)
K, L, M, N, O, P = Bools('K L M N O P')

# Base constraints
base_constraints = [
    M != P,           # M and P cannot be in same season
    K == N,           # K and N must be in same season
    Implies(K, O),    # If K is fall, O must be fall
    Implies(M, Not(N)) # If M is fall, N must be spring
]

# Evaluate each option - check if it FULLY DETERMINES the schedule
# i.e., exactly 1 solution exists when we add the option constraint

options = [
    ("A", And(K, Not(L))),  # K is fall, L is spring
    ("B", And(O, Not(P))),  # O is fall, P is spring
    ("C", And(P, Not(L))),  # P is fall, L is spring
    ("D", And(Not(K), Not(L))),  # Both K and L are spring
    ("E", And(M, L))  # Both M and L are fall
]

found_options = []
for letter, constr in options:
    s = Solver()
    s.add(base_constraints)
    s.add(constr)
    
    # Count solutions
    count = 0
    vars_list = [K, L, M, N, O, P]
    while s.check() == sat:
        count += 1
        m = s.model()
        s.add(Or([v != m.eval(v) for v in vars_list]))
    
    print(f"Option {letter}: {count} solutions")
    if count == 1:
        found_options.append(letter)

print(f"\nFound options: {found_options}")

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")