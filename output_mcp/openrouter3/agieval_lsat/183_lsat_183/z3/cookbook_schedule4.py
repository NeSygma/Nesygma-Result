from z3 import *

# Declare Boolean variables: True = fall, False = spring
K, L, M, N, O, P = Bools('K L M N O P')

# Base constraints
base_constraints = [
    Not(And(M, P)),  # M and P cannot be in the same season
    K == N,          # K and N must be in the same season
    Implies(K, O),   # If K is in fall, O must be in fall
    Implies(M, Not(N))  # If M is in fall, N must be in spring (i.e., not fall)
]

# Define options
options = [
    ("A", [K == True, L == False]),  # K fall, L spring
    ("B", [O == True, P == False]),  # O fall, P spring
    ("C", [P == True, L == False]),  # P fall, L spring
    ("D", [K == False, L == False]),  # Both K and L spring
    ("E", [M == True, L == True])  # Both M and L fall
]

found_options = []
for letter, opt_constr in options:
    solver = Solver()
    solver.add(base_constraints)
    solver.add(opt_constr)
    
    # Count solutions
    s = Solver()
    s.add(solver.assertions())
    count = 0
    models = []
    while s.check() == sat:
        count += 1
        m = s.model()
        models.append(m)
        if count > 10:  # Safety limit
            break
        # Block this model
        block = Or([v != m.eval(v) for v in [K, L, M, N, O, P]])
        s.add(block)
    
    print(f"Option {letter}: {count} solutions")
    for i, m in enumerate(models):
        print(f"  Solution {i+1}: K={m[K]}, L={m[L]}, M={m[M]}, N={m[N]}, O={m[O]}, P={m[P]}")
    
    if count == 1:
        found_options.append(letter)

print()
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")