from z3 import *

# Declare Boolean variables: True = fall, False = spring
K, L, M, N, O, P = Bools('K L M N O P')

# Base constraints
solver = Solver()
solver.add(Not(And(M, P)))  # M and P cannot be in the same season
solver.add(K == N)          # K and N must be in the same season
solver.add(Implies(K, O))   # If K is in fall, O must be in fall
solver.add(Implies(M, Not(N)))  # If M is in fall, N must be in spring (i.e., not fall)

# Function to count number of satisfying models
def count_models(solver, variables):
    s = Solver()
    s.add(solver.assertions())
    count = 0
    models = []
    while s.check() == sat:
        count += 1
        m = s.model()
        models.append(m)
        # Block this model
        block = Or([v != m.eval(v) for v in variables])
        s.add(block)
    return count, models

# Test each option
options = [
    ("A", And(K, Not(L))),  # K is fall, L is spring
    ("B", And(O, Not(P))),  # O is fall, P is spring (note: option says "0" but likely means O)
    ("C", And(P, Not(L))),  # P is fall, L is spring
    ("D", And(Not(K), Not(L))),  # Both K and L are spring
    ("E", And(M, L))  # Both M and L are fall
]

found_options = []
for letter, constr in options:
    solver.push()
    solver.add(constr)
    count, models = count_models(solver, [K, L, M, N, O, P])
    if count == 1:
        found_options.append(letter)
        print(f"Option {letter}: Schedule is fully determined (1 model)")
        # Print the unique model
        m = models[0]
        print(f"  K={m[K]}, L={m[L]}, M={m[M]}, N={m[N]}, O={m[O]}, P={m[P]}")
    else:
        print(f"Option {letter}: Schedule is NOT fully determined ({count} models)")
    solver.pop()

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